from google.protobuf.json_format import MessageToDict
from google.protobuf import message as _message


class Converter:
    def proto_to_basemodel(self, instance, model):
        dict_request = self.proto_to_dict(instance)
        return model(**dict_request)

    @staticmethod
    def basemodel_to_proto(instance, proto_model):
        return proto_model(**instance.model_dump(mode="json"))

    @staticmethod
    def proto_to_dict(instance: _message.Message) -> dict:
        return MessageToDict(
            message=instance,
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True,
        )
