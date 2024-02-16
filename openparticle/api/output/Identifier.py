from __future__ import annotations
import string
import struct
from typing import BinaryIO


class Identifier:
    canCreateIdentifier = False
    identifier_list = list()
    nextId = 0

    def __init__(self, namespace: string, value: string):
        if not Identifier.canCreateIdentifier:
            raise "请不要在createParticle()方法以外的地方创建Identifier对象"
        self.namespace = namespace
        self.value = value
        self.id = Identifier.nextId
        Identifier.nextId += 1
        Identifier.identifier_list.append(self)

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

    @classmethod
    def clearCache(cls):
        cls.identifier_list.clear()
        cls.nextId = 0
