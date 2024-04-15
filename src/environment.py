from interpreter import PlamRuntimeError
from ptoken import Token

class Environment:
    _values: dict[str, object] = {}

    def define(self, name: str, value: object):
        self._values[name] = value
    
    def get(self, name: Token) -> object:
        if name.lexeme in self._values.keys():
            return self._values[name.lexeme]
        
        raise PlamRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
    
    def assign(self, name: Token, value: object):
        if name.lexeme in self._values.keys():
            self._values[name.lexeme] = value
            return

        raise PlamRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
        
        