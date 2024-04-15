#!/usr/bin/env python

import sys
from scanner import Scanner
from ptoken import Token, TokenType
from stmt import Stmt, Expression
from pparser import Parser
from ast_printer import AstPrinter
from interpreter import Interpreter, PlamRuntimeError

class Plam:
    hadError = False
    hadRuntimeError = False
    interpreter: Interpreter

    def __init__(self):
        Plam.interpreter = Interpreter(self)

    def main(self):
        args = sys.argv[1::]
        if len(args) > 1:
            print("Usage: plam [script]")
            exit(64)
        elif len(args) == 1:
            self.runFile(args[0])
        else:
            self.runPrompt()

    def run(self, source: str, repl: bool = False):
        scanner = Scanner(source, self)
        toks: list[Token] = scanner.scanTokens()
        # for t in toks:
        #     print(f"({t.t} {t.lexeme})", end=" ")
        # print()
        # print()
        parser = Parser(toks, self)
        statements: list[Stmt] = parser.parse()

        if Plam.hadError: return

        # for stmt in statements:
        #     if isinstance(stmt, Expression):
        #         print(AstPrinter().print(stmt.expression))


        if repl:
            for s in statements:
                if isinstance(s, Expression):
                    try:
                        print(self.interpreter.stringify(self.interpreter.evaluate(s.expression)))
                    except PlamRuntimeError as e:
                        print("error")
                else:
                    self.interpreter.interpret([s])
        else:
            self.interpreter.interpret(statements)

    def error(self, line: int, message: str):
        self.report(line, "", message)
    
    def runtimeError(self, e: PlamRuntimeError):
        print(f"{e}\n[line {e.token.line}]",file=sys.stderr)
        Plam.hadRuntimeError = True

    def tok_error(self, token: Token, message: str):
        if token.t == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", message)

    def report(self, line: int, where: str, message: str):
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
                self.run(line, True)
                Plam.hadError = False
            except EOFError:
                break
            except KeyboardInterrupt:
                print()
                continue


if __name__ == "__main__":
    r = Plam()
    r.main()
