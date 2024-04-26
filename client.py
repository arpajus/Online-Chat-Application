import grpc
import chat_private_pb2
import chat_private_pb2_grpc
import time

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = chat_private_pb2_grpc.PrivateChatStub(channel)
    username = input("Enter your username: ")
    try:
        responses = stub.ConnectChat(generate_messages(username))
        for response in responses:
            print(f"Received message from {response.sender}: {response.content}")
    except grpc.RpcError as e:
        print(f"RPC failed: {str(e)}")

def generate_messages(username):
    while True:
        content = input("Enter message: ")
        yield chat_private_pb2.Message(sender=username, content=content, timestamp=int(time.time()))

if __name__ == '__main__':
    run()