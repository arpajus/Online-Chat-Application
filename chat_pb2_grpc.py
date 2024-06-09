# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chat_pb2 as chat__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class ChatServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Login = channel.unary_unary(
                '/ChatService/Login',
                request_serializer=chat__pb2.LoginRequest.SerializeToString,
                response_deserializer=chat__pb2.Response.FromString,
                )
        self.Connection = channel.unary_unary(
                '/ChatService/Connection',
                request_serializer=chat__pb2.ConnectionRequest.SerializeToString,
                response_deserializer=chat__pb2.Response.FromString,
                )
        self.UserDisconnected = channel.unary_unary(
                '/ChatService/UserDisconnected',
                request_serializer=chat__pb2.ConnectionRequest.SerializeToString,
                response_deserializer=chat__pb2.Response.FromString,
                )
        self.Disconnected = channel.unary_unary(
                '/ChatService/Disconnected',
                request_serializer=chat__pb2.ConnectionRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.Subscribe_group = channel.unary_unary(
                '/ChatService/Subscribe_group',
                request_serializer=chat__pb2.Subscribe.SerializeToString,
                response_deserializer=chat__pb2.Response.FromString,
                )
        self.SendMessageGroup = channel.unary_unary(
                '/ChatService/SendMessageGroup',
                request_serializer=chat__pb2.MessageRequest.SerializeToString,
                response_deserializer=chat__pb2.Response.FromString,
                )
        self.Discovery = channel.unary_unary(
                '/ChatService/Discovery',
                request_serializer=chat__pb2.LoginRequest.SerializeToString,
                response_deserializer=chat__pb2.Response.FromString,
                )


class ChatServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Login(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Connection(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UserDisconnected(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Disconnected(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Subscribe_group(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMessageGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Discovery(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Login': grpc.unary_unary_rpc_method_handler(
                    servicer.Login,
                    request_deserializer=chat__pb2.LoginRequest.FromString,
                    response_serializer=chat__pb2.Response.SerializeToString,
            ),
            'Connection': grpc.unary_unary_rpc_method_handler(
                    servicer.Connection,
                    request_deserializer=chat__pb2.ConnectionRequest.FromString,
                    response_serializer=chat__pb2.Response.SerializeToString,
            ),
            'UserDisconnected': grpc.unary_unary_rpc_method_handler(
                    servicer.UserDisconnected,
                    request_deserializer=chat__pb2.ConnectionRequest.FromString,
                    response_serializer=chat__pb2.Response.SerializeToString,
            ),
            'Disconnected': grpc.unary_unary_rpc_method_handler(
                    servicer.Disconnected,
                    request_deserializer=chat__pb2.ConnectionRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'Subscribe_group': grpc.unary_unary_rpc_method_handler(
                    servicer.Subscribe_group,
                    request_deserializer=chat__pb2.Subscribe.FromString,
                    response_serializer=chat__pb2.Response.SerializeToString,
            ),
            'SendMessageGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessageGroup,
                    request_deserializer=chat__pb2.MessageRequest.FromString,
                    response_serializer=chat__pb2.Response.SerializeToString,
            ),
            'Discovery': grpc.unary_unary_rpc_method_handler(
                    servicer.Discovery,
                    request_deserializer=chat__pb2.LoginRequest.FromString,
                    response_serializer=chat__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ChatService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Login(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/Login',
            chat__pb2.LoginRequest.SerializeToString,
            chat__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Connection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/Connection',
            chat__pb2.ConnectionRequest.SerializeToString,
            chat__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UserDisconnected(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/UserDisconnected',
            chat__pb2.ConnectionRequest.SerializeToString,
            chat__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Disconnected(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/Disconnected',
            chat__pb2.ConnectionRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Subscribe_group(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/Subscribe_group',
            chat__pb2.Subscribe.SerializeToString,
            chat__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendMessageGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/SendMessageGroup',
            chat__pb2.MessageRequest.SerializeToString,
            chat__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Discovery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/Discovery',
            chat__pb2.LoginRequest.SerializeToString,
            chat__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ChatClientStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ReceiveMessage = channel.unary_unary(
                '/ChatClient/ReceiveMessage',
                request_serializer=chat__pb2.MessageRequest.SerializeToString,
                response_deserializer=chat__pb2.Response.FromString,
                )


class ChatClientServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ReceiveMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatClientServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ReceiveMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.ReceiveMessage,
                    request_deserializer=chat__pb2.MessageRequest.FromString,
                    response_serializer=chat__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ChatClient', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatClient(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ReceiveMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatClient/ReceiveMessage',
            chat__pb2.MessageRequest.SerializeToString,
            chat__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
