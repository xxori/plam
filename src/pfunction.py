from __future__ import annotations
from environment import Environment
from callable import Callable
from typing import TYPE_CHECKING
from exceptions import ReturnException

if TYPE_CHECKING:
    from interpreter import Interpreter
    from stmt import Function


class PFunction(Callable):
    declaration: Function
    closure: Environment

    def __init__(self, declaration: Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter: Interpreter, args: list[object]) -> object:
        env = Environment(self.closure)
        for param, arg in zip(self.declaration.params, args):
            env.define(param.lexeme, arg)
        try:
            interpreter.executeBlock(self.declaration.body, env)
        except ReturnException as e:
            return e.value
        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"
