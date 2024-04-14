
from __future__ import annotations
from dataclasses import dataclass
from expr import Expr
from abc import ABC
from ptoken import Token
from typing import TypeVar, Generic

T = TypeVar("T")

class Stmt(ABC):
    def accept(self, visitor: Visitor):
        pass

@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitExpressionStmt(self)

@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitPrintStmt(self)

class Visitor(ABC, Generic[T]):
    def visitExpressionStmt(self, stmt: Expression) -> T:
        pass
        
    def visitPrintStmt(self, stmt: Print) -> T:
        pass
        