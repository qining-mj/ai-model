"""
模块导入系统 — Module Import System
演示 import、from…import、as、__name__、__file__ 等。
"""

print("=" * 60)
print("1. 基本 import")
print("=" * 60)

import math

print(f"  math.sqrt(16) = {math.sqrt(16)}")
print(f"  math.pi = {math.pi}")


print("\n" + "=" * 60)
print("2. from … import")
print("=" * 60)

from math import sqrt, pi

print(f"  sqrt(25) = {sqrt(25)}")
print(f"  pi = {pi}")


print("\n" + "=" * 60)
print("3. import … as — 别名")
print("=" * 60)

import datetime as dt

print(f"  dt.date.today() = {dt.date.today()}")
from math import factorial as fac
print(f"  fac(5) = {fac(5)}")


print("\n" + "=" * 60)
print("4. dir() — 查看模块/对象的所有属性")
print("=" * 60)

print(f"  dir(math) 中与三角相关的内容: {[n for n in dir(math) if n.startswith('sin')]}")
print(f"  当前模块 (__name__): {__name__}")


print("\n" + "=" * 60)
print("5. __name__ == '__main__' 模式")
print("=" * 60)


def main():
    """演示用主函数"""
    print("  main() 被调用 — 脚本作为入口运行时执行")


if __name__ == "__main__":
    main()
    print(f"  脚本被直接运行")
else:
    print(f"  脚本被导入: __name__ = {__name__}")


print("\n" + "=" * 60)
print("6. __file__ 属性")
print("=" * 60)

print(f"  当前模块的 __file__: {__file__}")
print(f"  math 模块的 __file__: {math.__file__}")
print(f"  dt  模块的 __file__: {dt.__file__}")


print("\n" + "=" * 60)
print("7. 导入 * 与下划线私有约定")
print("=" * 60)

print("  创建临时模块演示私有属性...")


# 使用 exec 模拟一个模块
module_code = """
_private = "不应被外部访问"
public = "可以被外部访问"
__all__ = ["public"]
"""


namespace = {}
exec(module_code, namespace)
print(f"  模块内容: {list(namespace.keys())}")


print("\n" + "=" * 60)
print("8. sys.modules — 已缓存模块字典")
print("=" * 60)

import sys

print(f"  sys 已加载: {'sys' in sys.modules}")
print(f"  math 是否已缓存: {'math' in sys.modules}")
# 注意：多次 import 同一模块只会执行一次
