
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from scanner import Token
from typing import TypeVar, Generic

T = TypeVar("T")

class Expr(ABC):
    def accept(self, visitor: Visitor):
        pass

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

class Visitor(ABC, Generic[T]):
    def visitBinaryExpr(self, expr: Binary) -> T:
        pass
        
    def visitGroupingExpr(self, expr: Grouping) -> T:
        pass
        
    def visitLiteralExpr(self, expr: Literal) -> T:
        pass
        
    def visitUnaryExpr(self, expr: Unary) -> T:
        pass
        
