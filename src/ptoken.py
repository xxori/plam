from enum import Enum


class TokenType(Enum):
    EOF = 0
    LPAREN = 1
    RPAREN = 2
    LBRACE = 3
    RBRACE = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SLASH = 9
    STAR = 10
    SEMICOLON = 11

    BANG = 12
    BANGEQ = 13
    EQUAL = 14
    EQUALEQ = 15
    GREATER = 16
    GREATEREQ = 17
    LESS = 18
    LESSEQ = 19

    IDENTIFIER = 20
    STRING = 21
    NUMBER = 22

    AND = 23
    CLASS = 24
    ELSE = 25
    FALSE = 26
    FN = 27
    FOR = 28
    IF = 29
    NULL = 30
    OR = 31
    PRINT = 32
    RETURN = 33
    SUPER = 34
    THIS = 35
    TRUE = 36
    VAR = 37
    WHILE = 38

    # QMARK = 39
    # COLON = 40


class Token:
    t: TokenType
    lexeme: str
    literal: object
    line: int

    def __init__(self, t: TokenType, lexeme: str, literal: object, line: int):
        self.t = t
        self.lexeme = lexeme
        self.object = object
        self.literal = literal
        self.line = line

    def toString(self) -> str:
        return str(self.t) + " " + self.lexeme + " " + str(self.literal)
