from __future__ import annotations
import time
from callable import Callable
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from interpreter import Interpreter


class BUILTIN(NamedTuple):
    fn: Callable
    name: str


class Clock(Callable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter: Interpreter, args: list[object]) -> object:
        return time.time()

    def __str__(self) -> str:
        return "<native fn clock>"


class Print(Callable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter: Interpreter, args: list[object]) -> object:
        print(interpreter.stringify(args[0]))
        return None

    def __str__(self) -> str:
        return "<native fn print>"


class Input(Callable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter: Interpreter, args: list[object]) -> object:
        return input(interpreter.stringify(args[0]))

    def __str__(self) -> str:
        return "<native fn input>"


BUILTINS: list[BUILTIN] = [
    BUILTIN(Clock(), "clock"),
    BUILTIN(Print(), "print"),
    BUILTIN(Input(), "input"),
]
