"""
包导入演示 — Packages Demo
创建了一个 mypackage 迷你包，演示 __init__.py、__all__ 和 sys.path。
"""

print("=" * 60)
print("1. 导入整个包")
print("=" * 60)

import mypackage

mypackage.show_info()


print("\n" + "=" * 60)
print("2. from 包 import 具体模块/函数")
print("=" * 60)

from mypackage import greet, Calculator

print(f"  greet('Alice') = {greet('Alice')}")

calc = Calculator()
print(f"  calc.multiply(6, 7) = {calc.multiply(6, 7)}")


print("\n" + "=" * 60)
print("3. __all__ 控制 from package import *")
print("=" * 60)

print(f"  mypackage.__all__ = {mypackage.__all__}")


# 执行 from mypackage import * 来验证 __all__
print("  执行 from mypackage import * ...")
exec("from mypackage import *")
# greet、add、Calculator 应被导入
print("  事实上 'greet', 'add', 'Calculator' 可通过 __all__ 被 * 导入")


print("\n" + "=" * 60)
print("4. 子模块别名")
print("=" * 60)

import mypackage.module_a as a
import mypackage.module_b as b

print(f"  a.greet('Bob') = {a.greet('Bob')}")
print(f"  b.Calculator.multiply(3, 4) = {b.Calculator.multiply(3, 4)}")


print("\n" + "=" * 60)
print("5. __init__.py 中的版本变量")
print("=" * 60)

print(f"  mypackage.VERSION = {mypackage.VERSION}")


print("\n" + "=" * 60)
print("6. sys.path — Python 模块搜索路径")
print("=" * 60)

import sys

print("  sys.path 的前 6 个条目:")
for i, p in enumerate(sys.path[:6], 1):
    print(f"    {i}. {p}")

print(f"\n  当前工作目录是否在路径中: {'.' in sys.path or '' in sys.path}")

# 临时添加自定义路径
sys.path.insert(0, "D:/ai/model_course/formal/python/code")
print(f"  已向 sys.path 头部添加自定义路径")


print("\n" + "=" * 60)
print("7. 相对导入（仅能在包内使用，此处仅演示概念）")
print("=" * 60)

print("  相对导入语法: from .module_a import greet")
print("  .  表示当前包")
print("  .. 表示父级包")
print("  相对导入仅在包内部（被导入时）有效")
