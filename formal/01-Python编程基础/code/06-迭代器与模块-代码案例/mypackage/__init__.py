"""
mypackage — 一个迷你包示例

__all__ 控制 from mypackage import * 的行为
"""

print("  [mypackage] __init__.py 被执行")

__all__ = ["greet", "add", "Calculator"]

from .module_a import greet, add
from .module_b import Calculator

VERSION = "1.0.0"


def show_info():
    print(f"  mypackage 版本 {VERSION}")
