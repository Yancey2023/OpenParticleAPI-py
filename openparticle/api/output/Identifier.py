from __future__ import annotations
import string
import struct
from typing import BinaryIO


class Identifier:

    def __init__(self, namespace: string, value: string):
        self.namespace = namespace
        self.value = value
        self.id = -1

    @classmethod
    def create(cls, namespace: string, value: string) -> Identifier:
        return cls(namespace, value)

    @classmethod
    def create_minecraft(cls, value: string) -> Identifier:
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
