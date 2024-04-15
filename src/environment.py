from __future__ import annotations
from interpreter import PlamRuntimeError
from ptoken import Token
from typing import Optional

UNINITIALIZED = object()
class Environment:
    enclosing: Optional[Environment]
    _values: dict[str, object]

    def __init__(self, enclosing: Optional[Environment] = None):
        self.enclosing = enclosing
        self._values = {}

    def define(self, name: str, value: object):
        self._values[name] = value

    def get(self, name: Token) -> object:
        if name.lexeme in self._values.keys():
            if self._values[name.lexeme] is UNINITIALIZED:
                raise PlamRuntimeError(name, f"Attempted to access uninitialized variable '{name.lexeme}'.")
            return self._values[name.lexeme]

        if self.enclosing != None:
            return self.enclosing.get(name)

        raise PlamRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: object):
        if name.lexeme in self._values.keys():
            self._values[name.lexeme] = value
            return

        if self.enclosing != None:
            self.enclosing.assign(name, value)
            return

        raise PlamRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
