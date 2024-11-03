# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from protos import images_pb2 as protos_dot_images__pb2

GRPC_GENERATED_VERSION = '1.67.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in protos/images_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ImageProcessorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UploadImage = channel.stream_unary(
                '/images.ImageProcessor/UploadImage',
                request_serializer=protos_dot_images__pb2.UploadImageRequest.SerializeToString,
                response_deserializer=protos_dot_images__pb2.UploadImageResponse.FromString,
                _registered_method=True)
        self.GetImages = channel.unary_unary(
                '/images.ImageProcessor/GetImages',
                request_serializer=protos_dot_images__pb2.GetImagesRequest.SerializeToString,
                response_deserializer=protos_dot_images__pb2.GetImagesResponse.FromString,
                _registered_method=True)
        self.GetImage = channel.unary_unary(
                '/images.ImageProcessor/GetImage',
                request_serializer=protos_dot_images__pb2.GetImageRequest.SerializeToString,
                response_deserializer=protos_dot_images__pb2.GetImageResponse.FromString,
                _registered_method=True)
        self.DeleteImages = channel.unary_unary(
                '/images.ImageProcessor/DeleteImages',
                request_serializer=protos_dot_images__pb2.DeleteImagesRequest.SerializeToString,
                response_deserializer=protos_dot_images__pb2.DeleteImagesResponse.FromString,
                _registered_method=True)
        self.UpdateImages = channel.unary_unary(
                '/images.ImageProcessor/UpdateImages',
                request_serializer=protos_dot_images__pb2.UpdateImagesRequest.SerializeToString,
                response_deserializer=protos_dot_images__pb2.UpdateImagesResponse.FromString,
                _registered_method=True)


class ImageProcessorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def UploadImage(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetImages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetImage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteImages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateImages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ImageProcessorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UploadImage': grpc.stream_unary_rpc_method_handler(
                    servicer.UploadImage,
                    request_deserializer=protos_dot_images__pb2.UploadImageRequest.FromString,
                    response_serializer=protos_dot_images__pb2.UploadImageResponse.SerializeToString,
            ),
            'GetImages': grpc.unary_unary_rpc_method_handler(
                    servicer.GetImages,
                    request_deserializer=protos_dot_images__pb2.GetImagesRequest.FromString,
                    response_serializer=protos_dot_images__pb2.GetImagesResponse.SerializeToString,
            ),
            'GetImage': grpc.unary_unary_rpc_method_handler(
                    servicer.GetImage,
                    request_deserializer=protos_dot_images__pb2.GetImageRequest.FromString,
                    response_serializer=protos_dot_images__pb2.GetImageResponse.SerializeToString,
            ),
            'DeleteImages': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteImages,
                    request_deserializer=protos_dot_images__pb2.DeleteImagesRequest.FromString,
                    response_serializer=protos_dot_images__pb2.DeleteImagesResponse.SerializeToString,
            ),
            'UpdateImages': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateImages,
                    request_deserializer=protos_dot_images__pb2.UpdateImagesRequest.FromString,
                    response_serializer=protos_dot_images__pb2.UpdateImagesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'images.ImageProcessor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('images.ImageProcessor', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ImageProcessor(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def UploadImage(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            '/images.ImageProcessor/UploadImage',
            protos_dot_images__pb2.UploadImageRequest.SerializeToString,
            protos_dot_images__pb2.UploadImageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetImages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/images.ImageProcessor/GetImages',
            protos_dot_images__pb2.GetImagesRequest.SerializeToString,
            protos_dot_images__pb2.GetImagesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetImage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/images.ImageProcessor/GetImage',
            protos_dot_images__pb2.GetImageRequest.SerializeToString,
            protos_dot_images__pb2.GetImageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteImages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/images.ImageProcessor/DeleteImages',
            protos_dot_images__pb2.DeleteImagesRequest.SerializeToString,
            protos_dot_images__pb2.DeleteImagesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateImages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/images.ImageProcessor/UpdateImages',
            protos_dot_images__pb2.UpdateImagesRequest.SerializeToString,
            protos_dot_images__pb2.UpdateImagesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
