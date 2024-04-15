import sys
import os


def defineAst(outdir: str, basename: str, types: list[str], additional=""):
    path = os.path.join(outdir, basename.lower() + ".py")
    with open(path, "w+") as f:
        f.write(
            f"""
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from ptoken import Token
from typing import TypeVar, Generic, Optional
{additional}

T = TypeVar("T")

class {basename}(ABC):
    def accept(self, visitor: Visitor[T]) -> T: ...
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
    for field in [x.strip() for x in fields.split(",") if len(x.strip()) > 0]:
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
    def visit{classname}{basename}(self, {basename.lower()}: {classname}) -> T: ...
        
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
            "Logical    : Expr left, Token operator, Expr right",
            "Unary      : Token operator, Expr right",
            "Variable   : Token name",
        ],
    )
    defineAst(
        outdir,
        "Stmt",
        [
            "Expression : Expr expression",
            "If         : Expr cond, Stmt thenBranch, Optional[Stmt] elseBranch, ",
            "Print      : Expr expression",
            "Var        : Token name, Optional[Expr] initializer",
            "While      : Expr cond, Stmt body",
            "Block      : list[Stmt] statements",
            "Break      : Token tok",
            "Continue   : Token tok",
        ],
        "from expr import Expr",
    )

# class While(Stmt):
#     cond: Expr
#     body: Stmt
#     post: Optional[Expr]

#     def __init__(self, cond: Expr, body: Stmt, post: Optional[Expr] = None):
#           self.cond = cond
#           self.body = body
#           self.post = post

#     def accept(self, visitor: Visitor[T]) -> T:
#             return visitor.visitWhileStmt(self)
