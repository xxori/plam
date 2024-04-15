from __future__ import annotations
from ptoken import TokenType, Token
from expr import (
    Expr,
    Binary,
    Unary,
    Literal,
    Grouping,
    Ternary,
    Logical,
    Variable,
    Assignment,
)
from typing import Callable, Self, Optional, cast, Any
from stmt import Stmt, Print, Expression, Var, Block, If, While, Break, Continue


class ParseError(Exception):
    pass


class BreakOutsideLoop(Exception):
    pass


class Parser:
    tokens: list[Token]
    current: int
    plam: Any

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

    def declaration(self) -> Optional[Stmt]:
        try:
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except ParseError:
            self.synchronise()
            return None

    def varDeclaration(self) -> Stmt:
        name: Token = self.consume(TokenType.IDENTIFIER, "Expected variable name.")

        initializer: Optional[Expr] = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration.")
        return Var(name, initializer)

    def statement(self) -> Stmt:
        if self.match(TokenType.FOR):
            return self.forStatement()
        if self.match(TokenType.IF):
            return self.ifStatement()
        if self.match(TokenType.PRINT):
            return self.printStatement()
        if self.match(TokenType.WHILE):
            return self.whileStatement()
        if self.match(TokenType.LBRACE):
            return Block(self.block())

        if self.match(TokenType.BREAK):
            self.consume(TokenType.SEMICOLON, "Expected ';' after 'break'.")
            return Break(self.previous())
        if self.match(TokenType.CONTINUE):
            self.consume(TokenType.SEMICOLON, "Expected ';' after 'continue'.")
            return Continue(self.previous())

        return self.expressionStatement()

    def block(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self.check(TokenType.RBRACE) and not self.isAtEnd():
            statements.append(cast(Stmt, self.declaration()))

        self.consume(TokenType.RBRACE, "Expected '}' after block.")
        return statements

    def forStatement(self) -> Stmt:
        self.consume(TokenType.LPAREN, "Expected '(' after 'for'.")

        initializer: Optional[Stmt]
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()

        condition: Optional[Expr] = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after loop condition.")

        increment: Optional[Expr] = None
        if not self.check(TokenType.SEMICOLON):
            increment = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after for clauses.")

        body = self.statement()
        if condition == None:
            condition = Literal(True)
        body = While(
            condition, body, Expression(increment) if increment != None else None
        )
        if initializer != None:
            body = Block([initializer, body])

        return body

    def ifStatement(self) -> Stmt:
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'.")
        expr = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after if condition.")

        thenBranch = self.statement()
        elseBranch = None
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()

        return If(expr, thenBranch, elseBranch)

    def printStatement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return Print(value)

    def whileStatement(self) -> Stmt:
        self.consume(TokenType.LPAREN, "Expected '(' after 'while'.")
        cond = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after while condition.")
        body = self.statement()

        return While(cond, body)

    def expressionStatement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return Expression(expr)

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.ternary()

        if self.match(
            TokenType.EQUAL,
            TokenType.PLUSEQ,
            TokenType.MINUSEQ,
            TokenType.STAREQ,
            TokenType.SLASHEQ,
        ):
            equals: Token = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                match equals.t:
                    case TokenType.EQUAL:
                        return Assignment(name, value)
                    case TokenType.PLUSEQ:
                        return Assignment(
                            name,
                            Binary(
                                expr,
                                Token(TokenType.PLUS, "+=", None, name.line),
                                value,
                            ),
                        )
                    case TokenType.MINUSEQ:
                        return Assignment(
                            name,
                            Binary(
                                expr,
                                Token(TokenType.MINUS, "-=", None, name.line),
                                value,
                            ),
                        )
                    case TokenType.STAREQ:
                        return Assignment(
                            name,
                            Binary(
                                expr,
                                Token(TokenType.STAR, "*=", None, name.line),
                                value,
                            ),
                        )
                    case TokenType.SLASHEQ:
                        return Assignment(
                            name,
                            Binary(
                                expr,
                                Token(TokenType.SLASH, "/=", None, name.line),
                                value,
                            ),
                        )

            self.error(equals, "Invalid assignment target.")

        if self.match(TokenType.PLUSEQ):
            peq: Token = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assignment(
                    name,
                    Binary(expr, Token(TokenType.PLUS, "+=", None, name.line), value),
                )

        return expr

    def ternary(self) -> Expr:
        expr = self.logic_or()
        if self.match(TokenType.QMARK):
            first = self.ternary()
            self.consume(TokenType.COLON, "Expected ':' after '?'")
            second = self.ternary()
            expr = Ternary(expr, first, second)

        return expr

    def logic_or(self) -> Expr:
        expr = self.logic_and()

        while self.match(TokenType.OR):
            op = self.previous()
            right = self.logic_and()
            expr = Logical(expr, op, right)

        return expr

    def logic_and(self) -> Expr:
        expr = self.equality()

        while self.match(TokenType.AND):
            op = self.previous()
            right = self.equality()
            expr = Logical(expr, op, right)

        return expr

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

    def comparison(self) -> Expr:
        return self._create_left_assoc_binary(
            [TokenType.GREATER, TokenType.GREATEREQ, TokenType.LESS, TokenType.LESSEQ],
            Parser.term,
        )

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
        if self.match(TokenType.MINUSMINUS):
            if self.match(TokenType.IDENTIFIER):
                return Assignment(
                    self.previous(),
                    Binary(
                        Variable(self.previous()),
                        Token(TokenType.MINUS, "-", None, self.previous().line),
                        Literal(1.0),
                    ),
                )
            else:
                raise self.error(self.peek(), "Expected identified after '--'.")

        elif self.match(TokenType.PLUSPLUS):
            if self.match(TokenType.IDENTIFIER):
                return Assignment(
                    self.previous(),
                    Binary(
                        Variable(self.previous()),
                        Token(TokenType.PLUS, "+", None, self.previous().line),
                        Literal(1.0),
                    ),
                )
            else:
                raise self.error(self.peek(), "Expected identified after '++'.")

        elif self.match(TokenType.BANG, TokenType.MINUS):
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
            stmts.append(cast(Stmt, self.declaration()))
        return stmts
