from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ptoken import Token


class PlamRuntimeError(RuntimeError):
    token: Token

    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token


class ReturnException(Exception):
    value: object

    def __init__(self, value: object):
        self.value = value


class ParseError(Exception):
    pass


class BreakOutsideLoop(Exception):
    pass
