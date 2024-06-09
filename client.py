import grpc
import chat_pb2
import chat_pb2_grpc
import pika
from concurrent import futures
import threading

class ChatClient(chat_pb2_grpc.ChatClientServicer):
    def __init__(self, username):
        self.username = username
        self.server_channel = grpc.insecure_channel('localhost:50051')
        self.server_stub = chat_pb2_grpc.ChatServiceStub(self.server_channel)
        self.ip = None
        self.port = None

        self.user_channel = None
        self.user_stub = None

        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
        self.rabbitmq_exchange = None

        self.thread_stop = threading.Event()
        self.thread_discovery = threading.Event()

    def check_server_connection(self):
        try:
            grpc.channel_ready_future(self.server_channel).result(timeout=5)
            print("Connected to the server")
        except grpc.FutureTimeoutError:
            print("Fail: It can't be connected to the server")
            exit(1)

    def login(self):
        request = chat_pb2.LoginRequest(username=self.username)
        try:
            response = self.server_stub.Login(request)
            if response.success:
                print(f"{response.message}: {response.ip}:{response.port}")
                self.ip = response.ip
                self.port = response.port
                return response.port
            else:
                print(f"{response.message}")
        except grpc.RpcError as e:
            print(f"Fail of gRPC")
            return None

    def connect_to_chat(self, chat_id):
        request = chat_pb2.ConnectionRequest(username=self.username, chat_id=chat_id)
        try:
            response = self.server_stub.Connection(request)
            if response.success:
                print(f"\t Conversation with:  {chat_id}")
                print(f"{response.message}")
                self.user_channel = grpc.insecure_channel(f'{response.ip}:{response.port}')
                self.user_stub = chat_pb2_grpc.ChatClientStub(self.user_channel)
                return True
            else:
                print(f'{response.message}')
                return False
        except grpc.RpcError as e:
            print(f"Fail of gRPC")

    def send_messages(self, chat_id, message):
        request = chat_pb2.MessageRequest(sender=self.username, message=message)
        try:
            response = self.user_stub.ReceiveMessage(request)
            if not response.success:
                print("The other person is not connected")
        except grpc.RpcError as e:
            print(f"Fail of gRPC")

    def ReceiveMessage(self, request, context):
        print(f"{request.sender}: {request.message}")
        return chat_pb2.Response(success=True)

    def start(self, client, port_client, chat_id):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        chat_pb2_grpc.add_ChatClientServicer_to_server(client, self.server)
        self.server.add_insecure_port(f'[::]:{port_client}')
        self.server.start()

        print("Write 'exit' to leave the chat")
        while True:
            message = input("")
            if message.lower() == "exit":
                request = chat_pb2.ConnectionRequest(username=self.username, chat_id=chat_id)
                response = self.server_stub.Disconnected(request)
                break
            client.send_messages(chat_id, message)
            request = chat_pb2.ConnectionRequest(username=self.username, chat_id=chat_id)
            response = self.server_stub.UserDisconnected(request)
            if response.success:
                break

        self.server.stop(0)

    def setup_rabbitmq(self, chat_id):
        try:
            self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.rabbitmq_channel = self.rabbitmq_connection.channel()
            self.rabbitmq_exchange = chat_id
            self.rabbitmq_channel.exchange_declare(exchange=self.rabbitmq_exchange, exchange_type='fanout')
        except pika.exceptions.AMQPError as e:
            print(f"Fail of RabbitMQ")

    def subscribe_to_group_chat(self, chat_id):
        self.setup_rabbitmq(chat_id)
        self.thread = threading.Thread(target=self.message_listener, args=(chat_id,))
        self.thread.start()

    def message_listener(self, chat_id):
        if self.rabbitmq_connection:
            result = self.rabbitmq_channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            self.rabbitmq_channel.queue_bind(exchange=self.rabbitmq_exchange, queue=queue_name)

            def callback(ch, method, properties, body):
                message = body.decode('utf-8')
                print(f"{message}")

            self.rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            print(f"Subscrit a {chat_id}. Waiting messages...")
            while not self.thread_stop.is_set():
                self.rabbitmq_channel.connection.process_data_events()
        else:
            print("No connection with Rabbit")

    def send_group_message(self, chat_id):
        if not self.rabbitmq_connection:
            print("No connection with Rabbit")
            return
        while True:
            message = input("")
            if message.lower() == "exit":
                print("Connection closed")
                self.thread_stop.set()
                break
            message = f"{self.username}: {message}"
            self.rabbitmq_channel.basic_publish(exchange=self.rabbitmq_exchange, routing_key='', body=message.encode('utf-8'))

        self.rabbitmq_connection.close()

    def Discover_Chats(self):
        self.setup_rabbitmq('discovery')
        self.publish_discovery_event()
        self.discover = threading.Thread(target=self.discovery_listener)
        self.discover.start()
        self.thread_discovery.wait()

    def publish_discovery_event(self):
        self.rabbitmq_channel.exchange_declare(exchange='discovery', exchange_type='fanout')
        discovery_message = f"{self.username}: {self.ip}:{self.port}"
        self.rabbitmq_channel.basic_publish(exchange='discovery', routing_key='', body=discovery_message.encode('utf-8'))
        request = chat_pb2.LoginRequest(username=self.username)
        response = self.server_stub.Discovery(request)

    def discovery_listener(self):
        result = self.rabbitmq_channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.rabbitmq_channel.queue_bind(exchange='discovery', queue=queue_name)

        def callback(ch, method, properties, body):
            print("Active Chats:")
            response = body.decode('utf-8')
            users = response.split('\n')
            for user in users:
                print(user)
            self.thread_discovery.set()

        self.rabbitmq_channel.basic_consume(queue_name, on_message_callback=callback, auto_ack=True)
        while not self.thread_discovery.is_set():
            self.rabbitmq_channel.connection.process_data_events()

    def setup_rabbitmq_queue(self, queue_name):
        try:
            self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            self.rabbitmq_channel = self.rabbitmq_connection.channel()
            self.rabbitmq_channel.queue_declare(queue=queue_name)
        except pika.exceptions.AMQPError as e:
            print(f"Fail of RabbitMQ")

    def subscribe_to_insult_queue(self, queue_name):
        self.setup_rabbitmq_queue(queue_name)
        self.thread = threading.Thread(target=self.insult_listener, args=(queue_name,))
        self.thread.start()

    def insult_listener(self, queue_name):
        if self.rabbitmq_connection:
            def callback(ch, method, properties, body):
                message = body.decode('utf-8')
                print(f"{message}")

            self.rabbitmq_channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            while not self.thread_stop.is_set():
                self.rabbitmq_channel.connection.process_data_events()
        else:
            print("No connection")

    def send_insult(self, queue_name):
        if not self.rabbitmq_connection:
            print("No connection")
            return
        while True:
            message = input("")
            if message.lower() == "exit":
                print("Connection closed")
                self.thread_stop.set()
                break
            message = f"{self.username}: {message}"
            self.rabbitmq_channel.basic_publish(exchange='', routing_key=queue_name, body=message.encode('utf-8'))

        self.rabbitmq_connection.close()

if __name__ == "__main__":
    username = input("Intrdouce your name: ")
    client = ChatClient(username)
    client.check_server_connection()
    port_client = client.login()
    client.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    client.rabbitmq_channel = client.rabbitmq_connection.channel()
    if port_client:
        while True:
            print("\n1. Connect To Chat")
            print("2. Subscribe to chat")
            print("3. Discover Chats")
            print("4. Insult Channel")
            print("5. Exit")
            choice = input("Select an option: ")

            if choice == "1":
                chat_id = input("Introduce the name of the person you want to chat with: ")
                if client.connect_to_chat(chat_id):
                    client.start(client, port_client, chat_id)
            elif choice == "2":
                chat_id = input("Group you want to suscribe ")
                client.subscribe_to_group_chat(chat_id)
                client.send_group_message(chat_id)
            elif choice == "3":
                client.Discover_Chats()
            elif choice == "4":
                queue_name = "insult_channel"
                client.subscribe_to_insult_queue(queue_name)
                client.send_insult(queue_name)
            elif choice == "5":
                print("Ending the system")
                break
            else:
                print("Introduce a valid option.")
