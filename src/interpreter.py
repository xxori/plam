from expr import Binary, Expr, Grouping, Literal, Ternary, Unary, Visitor as EVisitor
from ptoken import TokenType, Token
from stmt import Stmt, Expression, Print, Visitor as SVisitor

class PlamRuntimeError(RuntimeError):
    token: Token
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token

class Interpreter(EVisitor[object], SVisitor[None]):
    plam: object
    def __init__(self, plam):
        self.plam = plam

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except PlamRuntimeError as e:
            self.plam.runtimeError(e)

    def stringify(self, obj: object) -> str:
        if obj == None: return "null"

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        
        if obj == True:
            return "true"
        if obj == False:
            return "false"
        return str(obj)

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)
    
    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def isTruthy(self, obj: object) -> bool:
        if object == None: return False
        if isinstance(obj, bool): return bool(obj)
        return True
    
    def isEqual(self, left: object, right: object) -> bool:
        if type(left) != type(right): return False
        return left == right

    def checkNumberOperands(self, operator: Token, *operands: object):
        if all([isinstance(x, float) for x in operands]): return
        raise PlamRuntimeError(operator, "Operand must be a number.")

    def visitExpressionStmt(self, stmt: Expression) -> None:
       self.evaluate(stmt.expression)
    
    def visitPrintStmt(self, stmt: Print) -> None:
        value: object = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visitLiteralExpr(self, expr: Literal) -> object:
        return expr.value
    
    def visitGroupingExpr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expression)
    
    def visitUnaryExpr(self, expr: Unary) -> object:
        right = self.evaluate(expr.right)

        match expr.operator.t:
            case TokenType.MINUS:
                self.checkNumberOperands(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.isTruthy(right)
        
        # unreachable
        return None
    
    def visitTernaryExpr(self, expr: Ternary) -> object:
        cond = self.evaluate(expr.cond)
        if self.isTruthy(cond):
            return self.evaluate(expr.first)
        else:
            return self.evaluate(expr.second)
    
    def visitBinaryExpr(self, expr: Binary) -> object:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.t:
            case TokenType.MINUS:
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self.checkNumberOperands(expr.operator, left, right)
                if float(right) == 0.0:
                    raise PlamRuntimeError(expr.operator, "Can't divide by zero.")
                return float(left) / float(right)
            case TokenType.STAR:
                if isinstance(left, str) and isinstance(right, float):
                    if float(right).is_integer():
                        return str(left) * int(right)
                    else:
                        raise PlamRuntimeError(expr.operator, "Can't multiply string by non-integer amount.")
                if isinstance(right, str) and isinstance(left, float):
                    if float(left).is_integer():
                        return str(right) * int(left)
                    else:
                        raise PlamRuntimeError(expr.operator, "Can't multiply string by non-integer amount.")
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.PLUS:
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                raise PlamRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
            case TokenType.GREATER:
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATEREQ:
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESSEQ:
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANGEQ:
                return not self.isEqual(left, right)
            case TokenType.EQUALEQ:
                return self.isEqual(left, right)
            

    