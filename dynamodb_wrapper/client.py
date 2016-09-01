import uuid

from dynamodb_wrapper.meta import ModelMetadata


class Client(object):
    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def __generate_uuid():
        return str(uuid.uuid1()).replace('-', '')

    def create_schema(self, model, provisioned_throughput=None, wait=False):
        meta = ModelMetadata(model)

        if not provisioned_throughput:
            provisioned_throughput = {
                'ReadCapacityUnits': 25,
                'WriteCapacityUnits': 25
            }

        meta.create_table(self.connection, provisioned_throughput, wait)

    def delete_schema(self, model, wait=False):
        meta = ModelMetadata(model)

        meta.delete_table(self.connection, wait)

    def save(self, item):
        meta = ModelMetadata(type(item))

        if meta.hash_key.auto_generated:
            setattr(item, meta.hash_key.name, self.__generate_uuid())

        self.connection.Table(meta.name).put_item(Item=item.to_json())
