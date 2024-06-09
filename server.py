import grpc
import chat_pb2
import chat_pb2_grpc
import redis
from concurrent import futures
import time
import pika

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        try:
            self.name_server = NameServer()
            self.message_broker = MessageBroker()
        except Exception as e:
            print(f"Fail: The server can't be executed")
            exit()

    def Login(self, request, context):
        username = request.username
        if self.name_server.isSign(username):
            print(f"User {username} has been connected")
            username_address = self.name_server.get_user_address(username)
            ip, port = username_address.split(':')
            self.name_server.set_user_status(username, False)
            return chat_pb2.Response(success=True, message="Welcome!", ip=ip, port=int(port))
        else:
            return chat_pb2.Response(success=False, message="You are not registered!")

    def Connection(self, request, context):
        username = request.username
        chat_id = request.chat_id
        if self.name_server.get_user_status(chat_id):
            return chat_pb2.Response(success=False, message="User connected with another chat")
        else:
            chat_id_address = self.name_server.get_user_address(chat_id)
            if chat_id_address:
                self.name_server.set_user_status(chat_id, True)
                ip, port = chat_id_address.split(':')
                return chat_pb2.Response(success=True, message="You are now connected!", ip=ip, port=int(port))
            else:
                return chat_pb2.Response(success=False, message="Error!")

    def UserDisconnected(self, request, context):
        chat_id = request.chat_id
        if not self.name_server.get_user_status(chat_id):
            return chat_pb2.Response(success=True)
        else:
            return chat_pb2.Response(success=False)

    def Disconnected(self, request, context):
        username = request.username
        chat_id = request.chat_id
        self.name_server.set_user_status(username, False)
        self.name_server.set_user_status(chat_id, False)
        response = chat_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def Discovery(self, request, context):
        connected_users = self.name_server.get_connected_users()
        for user in connected_users:
            ip_port = self.name_server.get_user_address(user)
            response_message = f"{user}:{ip_port}"
            self.message_broker.channel.basic_publish(exchange='discovery', routing_key='', body=response_message.encode('utf-8'))
        return chat_pb2.Response(success=True)


class NameServer:
    def __init__(self):
        self.error_occurred = False

        try:
            self.redis_client = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)
            self.redis_client.set("usr:Paco", "127.0.0.1:15830")
            self.redis_client.set("usr:Paca", "127.0.0.1:35733")
        except Exception as e:
            if not self.error_occurred:
                print(f"Error of connection with Redis")
                self.error_occurred = True
            raise

    def isSign(self, username):
       return self.redis_client.exists(f"usr:{username}")

    def get_user_address(self, username):
        return self.redis_client.get(f"usr:{username}")

    def set_user_status(self, username, status):
        status_str = "connected" if status else "disconnected"
        self.redis_client.set(f"usr:{username}:status", status_str)

    def get_user_status(self, username):
        status_str = self.redis_client.get(f"usr:{username}:status")
        return status_str == "connected"

    def get_connected_users(self):
        connected_users = []
        for key in self.redis_client.keys("usr:*:status"):
            username = key.split(":")[1]
            if self.get_user_status(username):
                connected_users.append(username)
        return connected_users

class MessageBroker:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='group_chat', exchange_type='fanout')

    def publish_message(self, message):
        self.channel.basic_publish(exchange='group_chat', routing_key='', body=message)

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run_server()
