import struct
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import BinaryIO

STATIC = 0
SIMPLE = 1
FREE = 2


class DataColor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def write_to_file(self, fp: BinaryIO):
        pass


# 颜色不变
class DataColorStatic(DataColor):

    def __init__(self, color: int):
        self.color = color

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', STATIC))
        fp.write(struct.pack('>I', self.color))


# 在多个颜色之间匀速变化
class DataColorSimple(DataColor):

    def __init__(self, colors: list[int]):
        self.colors = colors

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', SIMPLE))
        fp.write(struct.pack('>I', len(self.colors)))
        for color in self.colors:
            fp.write(struct.pack('>I', color))


# 为每一个tick设置颜色
class DataColorFree(DataColor):

    def __init__(self, colors: list[int]):
        self.colors = colors

    def write_to_file(self, fp: BinaryIO) -> None:
        fp.write(struct.pack('>B', FREE))
        fp.write(struct.pack('>I', len(self.colors)))
        for color in self.colors:
            fp.write(struct.pack('>I', color))
