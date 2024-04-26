import grpc
from concurrent import futures
import time
import chat_private_pb2
import chat_private_pb2_grpc

class PrivateChatServicer(chat_private_pb2_grpc.PrivateChatServicer):
    def ConnectChat(self, request_iterator, context):
        for new_message in request_iterator:
            print(f"Received message from {new_message.sender}: {new_message.content}")
            yield new_message  # Echo the received message back to the client

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_private_pb2_grpc.add_PrivateChatServicer_to_server(PrivateChatServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()