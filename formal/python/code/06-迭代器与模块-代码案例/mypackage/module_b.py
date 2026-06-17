"""module_b — 提供 Calculator 类"""


class Calculator:
    """一个简单的计算器类"""

    @staticmethod
    def multiply(a: int, b: int) -> int:
        return a * b

    @staticmethod
    def divide(a: int, b: int) -> float:
        if b == 0:
            raise ZeroDivisionError("除数不能为 0")
        return a / b
