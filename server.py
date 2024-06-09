import grpc
import chat_pb2
import chat_pb2_grpc
from concurrent import futures
import time
import pika
from name_server import NameServer


class ChatService(chat_pb2_grpc.ChatServiceServicer):

    """
    Initialize the ChatService class by creating instances of NameServer and MessageBroker.
    If an exception occurs during the initialization process, the method will print an error message and exit the program.
    """
    def __init__(self):
        try:
            self.name_server = NameServer()
            self.message_broker = MessageBroker()
        except Exception as e:
            print(f"Fail: The server can't be executed")
            exit()

    """
    Authenticate the user by checking if the provided username is registered in the name server.
    If the username is registered, set the user status to not connected, retrieve the user's IP address and port,
    and return a success response with a welcome message and the user's IP and port.
    If the username is not registered, return a failure response indicating that the user is not registered.
    """
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

    """
    Check if the user with the provided chat_id is disconnected.
    If the user is disconnected, return a success response.
    If the user is still connected, return a failure response.
    """
    def UserDisconnected(self, request, context):
        chat_id = request.chat_id
        if not self.name_server.get_user_status(chat_id):
            return chat_pb2.Response(success=True)
        else:
            return chat_pb2.Response(success=False)

    """
    Set the user status to disconnected for the provided username and chat_id.
    Parameters:
        - request: The request object containing the username and chat_id.
    Returns:
        - Empty response indicating the successful disconnection of the user.
    """
    
    def Disconnected(self, request, context):
        username = request.username
        chat_id = request.chat_id
        self.name_server.set_user_status(username, False)
        self.name_server.set_user_status(chat_id, False)
        response = chat_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response
    
    """
    Discover connected users by retrieving their IP addresses and ports from the name server.
    For each connected user, publish a message to the message broker for discovery purposes.
    Returns:
        chat_pb2.Response: A response indicating the success of the discovery process.
    """
    def Discovery(self, request, context):
        connected_users = self.name_server.get_connected_users()
        for user in connected_users:
            ip_port = self.name_server.get_user_address(user)
            response_message = f"{user}:{ip_port}"
            self.message_broker.channel.basic_publish(exchange='discovery', routing_key='', body=response_message.encode('utf-8'))
        return chat_pb2.Response(success=True)

    """
    Check the status of the user with the provided chat_id and establish a connection if the user is available.
    Parameters:
        - request: The request object containing the username and chat_id.
    Returns:
        - chat_pb2.Response: A response indicating the success or failure of the connection attempt, along with relevant messages and connection details.
    """
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

class MessageBroker:
    """
    Initialize the MessageBroker class by establishing a connection to the RabbitMQ server running on 'localhost'.
    Create a channel for communication with the RabbitMQ server and declare an exchange named 'group_chat' with the exchange type 'fanout'.
    """
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='group_chat', exchange_type='fanout')

    def publish_message(self, message):
        self.channel.basic_publish(exchange='group_chat', routing_key='', body=message)

    """
    Run the gRPC server for the chat application.

    This function initializes a gRPC server with a ThreadPoolExecutor of 10 workers, adds the ChatService servicer to the server, starts the server on port 50051, and then enters a loop to keep the server running. The server will listen on all available interfaces (0.0.0.0).

    Returns:
        None
    """
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
