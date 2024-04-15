from __future__ import annotations
from interpreter import PlamRuntimeError
from ptoken import Token
from typing import Optional

class Environment:
    enclosing: Optional[Environment]
    _values: dict[str, object] = {}

    def __init__(self, enclosing: Optional[Environment] = None):
        self.enclosing = enclosing

    def define(self, name: str, value: object):
        self._values[name] = value
    
    def get(self, name: Token) -> object:
        if name.lexeme in self._values.keys():
            return self._values[name.lexeme]
        
        if self.enclosing != None:
            return self.enclosing.get(name)
        
        raise PlamRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
    
    def assign(self, name: Token, value: object):
        if name.lexeme in self._values.keys():
            self._values[name.lexeme] = value
            return

        raise PlamRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
        
        