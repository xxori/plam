
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from ptoken import Token
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class Expr(ABC):
    def accept(self, visitor: Visitor[T]) -> T: ...

@dataclass
class Assignment(Expr):
    name: Token
    value: Expr

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitAssignmentExpr(self)

@dataclass
class Ternary(Expr):
    cond: Expr
    first: Expr
    second: Expr

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitTernaryExpr(self)

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitBinaryExpr(self)

@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitGroupingExpr(self)

@dataclass
class Literal(Expr):
    value: object

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitLiteralExpr(self)

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitUnaryExpr(self)

@dataclass
class Variable(Expr):
    name: Token

    def accept(self, visitor: Visitor[T]) -> T:
            return visitor.visitVariableExpr(self)

class Visitor(ABC, Generic[T]):
    def visitAssignmentExpr(self, expr: Assignment) -> T: ...
        
    def visitTernaryExpr(self, expr: Ternary) -> T: ...
        
    def visitBinaryExpr(self, expr: Binary) -> T: ...
        
    def visitGroupingExpr(self, expr: Grouping) -> T: ...
        
    def visitLiteralExpr(self, expr: Literal) -> T: ...
        
    def visitUnaryExpr(self, expr: Unary) -> T: ...
        
    def visitVariableExpr(self, expr: Variable) -> T: ...
        
