
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from expr import Expr
from ptoken import Token
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class Stmt(ABC):
    def accept(self, visitor: Visitor[T]) -> T: ...

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

@dataclass
class Var(Stmt):
    name: Token
    initializer: Optional[Expr]

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitVarStmt(self)

@dataclass
class Block(Stmt):
    statements: list[Stmt]

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitBlockStmt(self)

class Visitor(ABC, Generic[T]):
    def visitExpressionStmt(self, stmt: Expression) -> T: ...
        
    def visitPrintStmt(self, stmt: Print) -> T: ...
        
    def visitVarStmt(self, stmt: Var) -> T: ...
        
    def visitBlockStmt(self, stmt: Block) -> T: ...
        
