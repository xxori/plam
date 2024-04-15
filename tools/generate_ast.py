import sys
import os


def defineAst(outdir: str, basename: str, types: list[str]):
    path = os.path.join(outdir, basename.lower() + ".py")
    with open(path, "w+") as f:
        f.write(
            f"""
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from ptoken import Token
from typing import TypeVar, Generic

T = TypeVar("T")

class {basename}(ABC):
    def accept(self, visitor: Visitor):
        pass
"""
        )
        for t in types:
            classname = t.split(":")[0].strip()
            fields = t.split(":")[1].strip()
            defineType(f, basename, classname, fields)
        f.write("\nclass Visitor(ABC, Generic[T]):\n")
        for t in types:
            classname = t.split(":")[0].strip()
            defineVisitor(f, basename, classname)


def defineType(f, basename, classname, fields):
    f.write(
        f"""
@dataclass
class {classname}({basename}):
"""
    )
    for field in map(str.strip, fields.split(",")):
        t = field.split(" ")[0].strip()
        n = field.split(" ")[1].strip()
        f.write(f"""    {n}: {t}\n""")
    f.write(
        f"""
    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visit{classname}{basename}(self)
"""
    )


def defineVisitor(f, basename: str, classname: str):
    f.write(
        f"""\
    def visit{classname}{basename}(self, {basename.lower()}: {classname}) -> T:
        pass
        
"""
    )


if __name__ == "__main__":
    args = sys.argv[1::]
    if len(args) != 1:
        print("Usage: generate_ast <output directory>")
        exit(64)
    outdir = args[0]
    defineAst(
        outdir,
        "Expr",
        [
            "Assignment : Token name, Expr value",
            "Ternary    : Expr cond, Expr first, Expr second",
            "Binary     : Expr left, Token operator, Expr right",
            "Grouping   : Expr expression",
            "Literal    : object value",
            "Unary      : Token operator, Expr right",
            "Variable   : Token name"
        ],
    )
    defineAst(
        outdir, "Stmt", ["Expression : Expr expression",
                         "Print      : Expr expression",
                         "Var        : Token name, Expr initializer"
                         ]
    )
