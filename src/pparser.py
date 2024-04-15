from __future__ import annotations
from ptoken import TokenType, Token
from expr import Expr, Binary, Unary, Literal, Grouping, Ternary, Variable, Assignment
from typing import Callable, Self
from stmt import Stmt, Print, Expression, Var


class ParseError(Exception):
    pass


class Parser:
    tokens: list[Token]
    current: int
    plam: object

    def __init__(self, tokens: list[Token], plam):
        self.current = 0
        self.tokens = tokens
        self.plam = plam

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def isAtEnd(self) -> bool:
        return self.peek().t == TokenType.EOF

    def check(self, t: TokenType) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().t == t

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def match(self, *types: TokenType) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True

        return False

    def error(self, token: Token, message: str) -> ParseError:
        self.plam.tok_error(token, message)
        return ParseError()

    def consume(self, t: TokenType, message: str) -> Token:
        if self.check(t):
            return self.advance()
        raise self.error(self.peek(), message)

    def synchronise(self):
        self.advance()

        while not self.isAtEnd():
            if self.previous().t == TokenType.SEMICOLON:
                return

            match self.peek().t:
                case (
                    TokenType.CLASS
                    | TokenType.FN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    return

            self.advance()

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except ParseError as e:
            self.synchronise()
            return None
    
    def varDeclaration(self) -> Stmt:
        name: Token = self.consume(TokenType.IDENTIFIER, "Expected variable name.")

        initializer: Expr = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.printStatement()
        return self.expressionStatement()

    def printStatement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return Print(value)

    def expressionStatement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return Expression(expr)

    def expression(self) -> Expr:
        return self.assignment()
    
    def assignment(self) -> Expr:
        expr = self.equality()

        if self.match(TokenType.EQUAL):
            equals: Token = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assignment(name, value)
            
            self.error(equals, "Invalid assignment target.")
        
        return expr

    # def ternary(self) -> Expr:
    #     expr = self.equality()
    #     if self.match(TokenType.QMARK):
    #         first = self.equality()
    #         self.consume(TokenType.COLON, "Expected ':' after '?'")
    #         second = self.equality()
    #         expr = Ternary(expr, first, second)
    #     if self.match(TokenType.COLON):
    #         raise self.error(self.peek(), "Unexpected ':'.")

    #     return expr

    def _create_left_assoc_binary(
        self, types: list[TokenType], expr: Callable[[Self], Expr]
    ):
        e = expr(self)

        while self.match(*types):
            op = self.previous()
            right = expr(self)
            e = Binary(e, op, right)

        return e

    def equality(self) -> Expr:
        return self._create_left_assoc_binary(
            [TokenType.BANGEQ, TokenType.EQUALEQ], Parser.comparison
        )

    # def equality(self) -> Expr:
    #     expr = self.comparison()

    #     while self.match(TokenType.BANGEQ, TokenType.EQUALEQ):
    #         op = self.previous()
    #         right = self.comparison()
    #         expr = Binary(expr, op, right)

    #     return expr

    def comparison(self) -> Expr:
        return self._create_left_assoc_binary(
            [TokenType.GREATER, TokenType.GREATEREQ, TokenType.LESS, TokenType.LESSEQ],
            Parser.term,
        )

    # def comparison(self) -> Expr:
    #     expr = self.term()

    #     while self.match(TokenType.GREATER, TokenType.GREATEREQ, TokenType.LESS, TokenType.LESSEQ):
    #         op = self.previous()
    #         right = self.term()
    #         expr = Binary(expr, op, right)

    #     return expr

    def term(self) -> Expr:
        return self._create_left_assoc_binary(
            [TokenType.MINUS, TokenType.PLUS],
            Parser.factor,
        )

    def factor(self) -> Expr:
        return self._create_left_assoc_binary(
            [TokenType.SLASH, TokenType.STAR],
            Parser.unary,
        )

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.previous()
            right = self.unary()
            return Unary(op, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NULL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expected expression.")

    def parse(self) -> list[Stmt]:
        stmts: list[Stmt] = []
        while not self.isAtEnd():
            stmts.append(self.declaration())
        return stmts
