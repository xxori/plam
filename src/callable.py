from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpreter import Interpreter


class Callable(ABC):
    def call(self, interpreter: Interpreter, args: list[object]) -> object: ...

    def arity(self) -> int: ...

    def __str__(self) -> str:
        return "<base fn>"
