"""module_a — 提供 greet() 和 add() 工具函数"""


def greet(name: str) -> str:
    """返回问候语"""
    return f"你好，{name}！欢迎使用 mypackage。"


def add(a: int, b: int) -> int:
    """返回两个整数之和"""
    return a + b


def _helper():
    """以下划线开头 = 内部函数，不应被外部使用"""
    pass
