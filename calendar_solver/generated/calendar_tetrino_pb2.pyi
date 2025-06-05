from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class PuzzleRequest(_message.Message):
    __slots__ = ("date",)
    DATE_FIELD_NUMBER: _ClassVar[int]
    date: _timestamp_pb2.Timestamp
    def __init__(self, date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class PuzzleSolution(_message.Message):
    __slots__ = ("solution_pieces",)
    SOLUTION_PIECES_FIELD_NUMBER: _ClassVar[int]
    solution_pieces: _containers.RepeatedCompositeFieldContainer[Piece]
    def __init__(self, solution_pieces: _Optional[_Iterable[_Union[Piece, _Mapping]]] = ...) -> None: ...

class PuzzleSolutions(_message.Message):
    __slots__ = ("solutions",)
    SOLUTIONS_FIELD_NUMBER: _ClassVar[int]
    solutions: _containers.RepeatedCompositeFieldContainer[PuzzleSolution]
    def __init__(self, solutions: _Optional[_Iterable[_Union[PuzzleSolution, _Mapping]]] = ...) -> None: ...

class Piece(_message.Message):
    __slots__ = ("tetromino_name", "cells")
    TETROMINO_NAME_FIELD_NUMBER: _ClassVar[int]
    CELLS_FIELD_NUMBER: _ClassVar[int]
    tetromino_name: str
    cells: _containers.RepeatedCompositeFieldContainer[Cell]
    def __init__(self, tetromino_name: _Optional[str] = ..., cells: _Optional[_Iterable[_Union[Cell, _Mapping]]] = ...) -> None: ...

class Cell(_message.Message):
    __slots__ = ("row", "col")
    ROW_FIELD_NUMBER: _ClassVar[int]
    COL_FIELD_NUMBER: _ClassVar[int]
    row: str
    col: str
    def __init__(self, row: _Optional[str] = ..., col: _Optional[str] = ...) -> None: ...
