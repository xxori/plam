#!/usr/bin/env python

import sys
from scanner import Scanner
from ptoken import Token, TokenType
from stmt import Stmt
from pparser import Parser
from ast_printer import AstPrinter
from interpreter import Interpreter, PlamRuntimeError

class Plam:
    hadError = False
    hadRuntimeError = False
    interpreter: Interpreter

    def __init__(self):
        Plam.interpreter = Interpreter(Plam)

    def main(self):
        args = sys.argv[1::]
        if len(args) > 1:
            print("Usage: plam [script]")
            exit(64)
        elif len(args) == 1:
            self.runFile(args[0])
        else:
            self.runPrompt()

    def run(self, source: str):
        scanner = Scanner(source, Plam)
        toks: list[Token] = scanner.scanTokens()
        # for t in toks:
        #     print(f"({t.t} {t.lexeme})", end=" ")
        # print()
        # print()
        parser = Parser(toks, Plam)
        statements: list[Stmt] = parser.parse()

        if Plam.hadError: return

        self.interpreter.interpret(statements)

    def error(line: int, message: str):
        Plam.report(line, "", message)
    
    def runtimeError(e: PlamRuntimeError):
        print(f"{e}\n[line {e.token.line}]",file=sys.stderr)
        Plam.hadRuntimeError = True

    def tok_error(token: Token, message: str):
        if token.t == TokenType.EOF:
            Plam.report(token.line, " at end", message)
        else:
            Plam.report(token.line, " at '" + token.lexeme + "'", message)

    def report(line: int, where: str, message: str):
        print("[line " + str(line) + "] Error" + where + ": " + message, file=sys.stderr)
        Plam.hadError = True

    def runFile(self, filename: str):
        with open(filename, "r") as f:
            self.run(f.read())

        if Plam.hadError:
            exit(65)
        if Plam.hadRuntimeError:
            exit(70)

    def runPrompt(self):
        while True:
            try:
                line = input("plam> ")
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            self.run(line)
            Plam.hadError = False


if __name__ == "__main__":
    r = Plam()
    r.main()
