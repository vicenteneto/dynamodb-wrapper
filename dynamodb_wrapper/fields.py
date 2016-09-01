class FieldType:
    STRING = 'S'
    NUMBER = 'N'
    BINARY = 'B'


class Field(object):
    def __init__(self, type_=FieldType.STRING, hash_key=False, range_key=False, auto_generated=False, name=None):
        if hash_key and range_key:
            raise ValueError('hash_key and range_key are mutually exclusive!')

        if all(attribute_type != type_ for attribute_type in [FieldType.STRING, FieldType.NUMBER, FieldType.BINARY]):
            raise ValueError('Type must be one of: "S", "N" or "B"!')

        if type_ != 'S' and auto_generated:
            raise ValueError('Only string fields can be auto generated!')

        self.type = type_
        self.hash_key = hash_key
        self.range_key = range_key
        self.auto_generated = auto_generated
        self.name = name
