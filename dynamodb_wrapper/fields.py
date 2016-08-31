class Field(object):
    def __init__(self, type_='S', hash_key=False, range_key=False, name=None):
        if hash_key and range_key:
            raise ValueError('hash_key and range_key are mutually exclusive!')

        if all(attribute_type != type_ for attribute_type in ['S', 'N', 'B']):
            raise ValueError('Type must be one of: "S", "N" or "B"!')

        self.type = type_
        self.hash_key = hash_key
        self.range_key = range_key
        self.name = name
