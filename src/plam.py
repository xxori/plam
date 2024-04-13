#!/usr/bin/env python

import sys
from scanner import Scanner
from ptoken import Token

class Plam:
    hadError = False

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
        for token in toks:
            print("(" + str(token.t), token.lexeme + ")")
    
    def error(line: int, message: str):
        Plam.report(line, "", message)
    
    def report(line: int, where: str, message: str):
        print("[line " + str(line) + "] Error" + where + ": " + message)
        Plam.hadError = True

    def runFile(self, filename: str):
        with open(filename, "r") as f:
            self.run(f.read())
        
        if (Plam.hadError): exit(65)
    
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