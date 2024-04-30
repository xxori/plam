from expr import (
    Assignment,
    Binary,
    Grouping,
    Literal,
    Logical,
    Ternary,
    Unary,
    Variable,
    Visitor,
    Expr,
)


class AstPrinter(Visitor[str]):
    def print(self, expr: Expr):
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        strbuilder = ["(", name]
        for expr in exprs:
            strbuilder.append(" ")
            strbuilder.append(expr.accept(self))
        strbuilder.append(")")
        return "".join(strbuilder)

    def visitTernaryExpr(self, expr: Ternary) -> str:
        return self.parenthesize(expr.cond.accept(self) + "?", expr.first, expr.second)

    def visitVariableExpr(self, expr: Variable) -> str:
        return expr.name.lexeme

    def visitAssignmentExpr(self, expr: Assignment) -> str:
        return self.parenthesize("=", Literal(expr.name.lexeme), expr.value)

    def visitLogicalExpr(self, expr: Logical) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: Literal) -> str:
        if expr.value == None:
            return "null"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)


# if __name__ == "__main__":
#     from ptoken import Token, TokenType

#     expr = Binary(
#         Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
#         Token(TokenType.STAR, "*", None, 1),
#         Grouping(Literal(45.67)),
#     )
#     print(AstPrinter().print(expr))
