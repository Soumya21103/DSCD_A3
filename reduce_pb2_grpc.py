# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import reduce_pb2 as reduce__pb2


class ReducerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.invokeReducer = channel.unary_unary(
                '/Reducer.Reducer/invokeReducer',
                request_serializer=reduce__pb2.invocationRequest.SerializeToString,
                response_deserializer=reduce__pb2.invocationResponse.FromString,
                )
        self.HeartBeat = channel.unary_unary(
                '/Reducer.Reducer/HeartBeat',
                request_serializer=reduce__pb2.HeartBeatRequest.SerializeToString,
                response_deserializer=reduce__pb2.HeartBeatResponse.FromString,
                )
        self.getOutputFile = channel.unary_unary(
                '/Reducer.Reducer/getOutputFile',
                request_serializer=reduce__pb2.OutputFileRequest.SerializeToString,
                response_deserializer=reduce__pb2.OutputFileResponse.FromString,
                )


class ReducerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def invokeReducer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HeartBeat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getOutputFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReducerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'invokeReducer': grpc.unary_unary_rpc_method_handler(
                    servicer.invokeReducer,
                    request_deserializer=reduce__pb2.invocationRequest.FromString,
                    response_serializer=reduce__pb2.invocationResponse.SerializeToString,
            ),
            'HeartBeat': grpc.unary_unary_rpc_method_handler(
                    servicer.HeartBeat,
                    request_deserializer=reduce__pb2.HeartBeatRequest.FromString,
                    response_serializer=reduce__pb2.HeartBeatResponse.SerializeToString,
            ),
            'getOutputFile': grpc.unary_unary_rpc_method_handler(
                    servicer.getOutputFile,
                    request_deserializer=reduce__pb2.OutputFileRequest.FromString,
                    response_serializer=reduce__pb2.OutputFileResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Reducer.Reducer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Reducer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def invokeReducer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Reducer.Reducer/invokeReducer',
            reduce__pb2.invocationRequest.SerializeToString,
            reduce__pb2.invocationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def HeartBeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Reducer.Reducer/HeartBeat',
            reduce__pb2.HeartBeatRequest.SerializeToString,
            reduce__pb2.HeartBeatResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getOutputFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Reducer.Reducer/getOutputFile',
            reduce__pb2.OutputFileRequest.SerializeToString,
            reduce__pb2.OutputFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
