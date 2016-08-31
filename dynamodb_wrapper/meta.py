import inspect
import time

from botocore.exceptions import ClientError

from dynamodb_wrapper.fields import Field


class ModelMetadata(object):
    def __init__(self, model):
        self.model = model
        self.name = model.__name__

        self.hash_key = None
        self.range_key = None

        self.attribute_definitions = []
        self.key_schema = []

        for name, field in inspect.getmembers(self.model):
            if isinstance(field, Field):
                if name.startswith('__') or name.endswith('_'):
                    raise ValueError('Field "%s" cannot begin with "__" or end with "_"' % name)

                if not field.name:
                    field.name = name

                if field.hash_key:
                    if self.hash_key:
                        raise ValueError('Only one hash_key is supported!')
                    self.hash_key = field
                elif field.range_key:
                    if self.range_key:
                        raise ValueError('Only one range_key is supported!')
                    self.range_key = field

        if not self.hash_key:
            raise ValueError('Table must have one hash_key!')
        self.__add_attribute_definitions(self.hash_key)
        self.__add_key_schema_attribute(self.hash_key, 'HASH')

        if self.range_key:
            self.__add_attribute_definitions(self.range_key)
            self.__add_key_schema_attribute(self.range_key, 'RANGE')

    def __add_attribute_definitions(self, field):
        self.attribute_definitions.append({
            'AttributeName': field.name,
            'AttributeType': field.type
        })

    def __add_key_schema_attribute(self, field, type_):
        self.key_schema.append({
            'AttributeName': field.name,
            'KeyType': type_
        })

    def create_table(self, connection, provisioned_throughput, wait=False):
        existing_stables = set(connection.list_tables()['TableNames'])

        if self.name in existing_stables:
            return None

        connection.create_table(AttributeDefinitions=self.attribute_definitions, TableName=self.name,
                                KeySchema=self.key_schema, ProvisionedThroughput=provisioned_throughput)

        if wait:
            while True:
                try:
                    table_describe = connection.describe_table(TableName=self.name)
                    if table_describe['Table']['TableStatus'] == 'ACTIVE':
                        break
                    time.sleep(1)
                except ClientError:
                    pass
