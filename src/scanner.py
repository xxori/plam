from ptoken import Token, TokenType


class Scanner:
    source: str
    tokens: list[Token]
    plam: object  # Super object ref

    start: int
    current: int
    line: int

    keywords: dict[str, TokenType] = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fn": TokenType.FN,
        "if": TokenType.IF,
        "null": TokenType.NULL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str, plam):
        self.tokens = []
        self.source = source
        self.plam = plam

        self.start = 0
        self.current = 0
        self.line = 1

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)

    def scanTokens(self) -> list[Token]:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def addToken(self, t: TokenType, literal: object = None):
        self.tokens.append(
            Token(t, self.source[self.start : self.current], literal, self.line)
        )

    def scanToken(self):
        c: str = self.advance()
        match c:
            case "(":
                self.addToken(TokenType.LPAREN)
            case ")":
                self.addToken(TokenType.RPAREN)
            case "{":
                self.addToken(TokenType.LBRACE)
            case "}":
                self.addToken(TokenType.RBRACE)
            case ",":
                self.addToken(TokenType.COMMA)
            case ".":
                self.addToken(TokenType.DOT)
            case "-":
                self.addToken(TokenType.MINUS)
            case "+":
                self.addToken(TokenType.PLUS)
            case ";":
                self.addToken(TokenType.SEMICOLON)
            # case ":":
            #     self.addToken(TokenType.COLON)
            # case "?":
            #     self.addToken(TokenType.QMARK)
            case "*":
                self.addToken(TokenType.STAR)

            case "!":
                self.addToken(TokenType.BANGEQ if self.match("=") else TokenType.BANG)
            case "=":
                self.addToken(TokenType.EQUALEQ if self.match("=") else TokenType.EQUAL)
            case "<":
                self.addToken(TokenType.LESSEQ if self.match("=") else TokenType.LESS)
            case ">":
                self.addToken(
                    TokenType.GREATEREQ if self.match("=") else TokenType.GREATER
                )

            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.isAtEnd():
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)

            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1

            case '"':
                self.string()
            case _:
                if self.isDigit(c):
                    self.number()
                elif self.isAlpha(c):
                    self.identifier()
                else:
                    self.plam.error(self.line, "Unexpected character '" + c + "'.")

    def match(self, expected: str) -> bool:
        if self.isAtEnd() or self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]

    def peekNext(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.isAtEnd():
            self.plam.error(self.line, "Unterminated string.")
            return
        self.advance()
        self.addToken(TokenType.STRING, self.source[self.start + 1 : self.current - 1])

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()
        if self.peek() == "." and self.isDigit(self.peekNext()):
            self.advance()
            while self.isDigit(self.peek()):
                self.advance()
        self.addToken(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        text = self.source[self.start : self.current]
        t = self.keywords.get(text, TokenType.IDENTIFIER)
        self.addToken(t)

    def isAlpha(self, c: str) -> bool:
        if len(c) != 1:
            raise ValueError("Multicharacter string passed to isAlpha")
        return (c >= "A" and c <= "Z") or (c >= "a" and c <= "z") or (c == "_")

    def isAlphaNumeric(self, c: str) -> bool:
        return self.isDigit(c) or self.isAlpha(c)

    def isDigit(self, c: str) -> bool:
        if len(c) != 1:
            raise ValueError("Multicharacter string passed to isDigit")
        return "0" <= c and c <= "9"
