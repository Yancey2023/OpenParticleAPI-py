import string
import struct
from typing import BinaryIO


class Identifier:
    def __init__(self, namespace: string, value: string):
        self.namespace = namespace
        self.value = value

    @classmethod
    def create(cls, namespace: string, value: string):
        return cls(namespace, value)

    @classmethod
    def create_minecraft(cls, value: string):
        return cls("minecraft", value)

    def write_to_file(self, fp: BinaryIO) -> None:
        if self.namespace == "minecraft":
            fp.write(struct.pack('?', True))
        else:
            fp.write(struct.pack('?', False))
            fp.write(struct.pack('>H', len(self.namespace)))
            fp.write(self.namespace.encode('utf-8'))
        fp.write(struct.pack('>H', len(self.value)))
        fp.write(self.value.encode('utf-8'))


class IdentifierCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IdentifierCache, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.identifier_list: list[Identifier] = list()

    def add(self, identifier: Identifier) -> None:
        if identifier not in self.identifier_list:
            self.identifier_list.append(identifier)

    def getId(self, identifier: Identifier) -> int:
        return self.identifier_list.index(identifier)

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>I', len(self.identifier_list)))
        for identifier in self.identifier_list:
            identifier.write_to_file(fp)
