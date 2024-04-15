
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from ptoken import Token
from typing import TypeVar, Generic, Optional
from expr import Expr

T = TypeVar("T")

class Stmt(ABC):
    def accept(self, visitor: Visitor[T]) -> T: ...

@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitExpressionStmt(self)

@dataclass
class If(Stmt):
    cond: Expr
    thenBranch: Stmt
    elseBranch: Optional[Stmt]

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitIfStmt(self)

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

class While(Stmt):
    cond: Expr
    body: Stmt
    post: Optional[Stmt]

    def __init__(self, cond: Expr, body: Stmt, post: Optional[Stmt] = None):
          self.cond = cond
          self.body = body
          self.post = post

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitWhileStmt(self)

@dataclass
class Block(Stmt):
    statements: list[Stmt]

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitBlockStmt(self)

@dataclass
class Break(Stmt):
    tok: Token

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitBreakStmt(self)

@dataclass
class Continue(Stmt):
    tok: Token

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitContinueStmt(self)

class Visitor(ABC, Generic[T]):
    def visitExpressionStmt(self, stmt: Expression) -> T: ...
        
    def visitIfStmt(self, stmt: If) -> T: ...
        
    def visitPrintStmt(self, stmt: Print) -> T: ...
        
    def visitVarStmt(self, stmt: Var) -> T: ...
        
    def visitWhileStmt(self, stmt: While) -> T: ...
        
    def visitBlockStmt(self, stmt: Block) -> T: ...
        
    def visitBreakStmt(self, stmt: Break) -> T: ...
        
    def visitContinueStmt(self, stmt: Continue) -> T: ...
        
