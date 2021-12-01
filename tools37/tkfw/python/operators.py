from .base import UnaryOperator, BinaryOperator

__all__ = [
    'Neg',
    'BitwiseNot',
    'Not',
    'Add',
    'Sub',
    'Mul',
    'TrueDiv',
    'Mod',
    'Pow',
    'FloorDiv',
    'BitwiseAnd',
    'BitwiseOr',
    'BitwiseXor',
    'And',
    'Or'
]


class Neg(UnaryOperator):
    def __str__(self):
        return f"-{self.right!s}"


class BitwiseNot(UnaryOperator):
    def __str__(self):
        return f"~{self.right!s}"


class Not(UnaryOperator):
    def __str__(self):
        return f"not {self.right!s}"


class Add(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} + {self.right!s}"


class Sub(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} - {self.right!s}"


class Mul(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} * {self.right!s}"


class TrueDiv(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} / {self.right!s}"


class Mod(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} % {self.right!s}"


class Pow(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} ** {self.right!s}"


class FloorDiv(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} // {self.right!s}"


class BitwiseAnd(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} & {self.right!s}"


class BitwiseOr(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} | {self.right!s}"


class BitwiseXor(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} ^ {self.right!s}"


class And(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} and {self.right!s}"


class Or(BinaryOperator):
    def __str__(self):
        return f"{self.left!s} or {self.right!s}"
