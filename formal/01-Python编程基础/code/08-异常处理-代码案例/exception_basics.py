"""
异常处理基础 — try / except / else / finally
演示基本异常捕获、多重 except、else、finally 以及 return 交互。
"""

print("=" * 60)
print("1. 基本 try-except")
print("=" * 60)

try:
    result = 10 / 0
except ZeroDivisionError:
    print("  捕获: 除以零错误！")

print("  程序继续运行...")


print("\n" + "=" * 60)
print("2. 捕获特定异常类型")
print("=" * 60)

values = [10, "abc", [1, 2, 3], None]

for v in values:
    try:
        result = v + 5
        print(f"  {v} + 5 = {result}")
    except TypeError:
        print(f"  类型错误: 不能对 {type(v).__name__} 类型使用 +")


print("\n" + "=" * 60)
print("3. 多个 except 块")
print("=" * 60)


def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "除数不能为 0"
    except TypeError:
        return "参数类型错误"


print(f"  safe_divide(10, 2)  = {safe_divide(10, 2)}")
print(f"  safe_divide(10, 0)  = {safe_divide(10, 0)}")
print(f"  safe_divide(10, 'x') = {safe_divide(10, 'x')}")


print("\n" + "=" * 60)
print("4. 一个 except 捕获多个异常类型")
print("=" * 60)


def process_value(val):
    try:
        return 100 / val
    except (ZeroDivisionError, TypeError, ValueError) as e:
        print(f"  捕获到 {type(e).__name__}: {e}")
        return None


process_value(0)
process_value("abc")


print("\n" + "=" * 60)
print("5. else 子句 — 未发生异常时执行")
print("=" * 60)


def read_int(prompt):
    try:
        value = int(input(prompt))
    except ValueError:
        print("  输入无效，不是整数")
        return None
    else:
        print(f"  输入有效: {value}")
        return value


# 模拟输入, 不阻塞
import io
import sys
sys.stdin = io.StringIO("42\n")
read_int("  请输入整数: ")
sys.stdin = sys.__stdin__  # 恢复


print("\n" + "=" * 60)
print("6. finally 子句 — 始终执行")
print("=" * 60)


def demo_finally():
    try:
        print("  尝试执行...")
        # 即使是 return 也不会阻止 finally
        return "返回值"
    finally:
        print("  finally: 无论如何都会执行")


print(f"  函数返回: {demo_finally()}")


print("\n" + "=" * 60)
print("7. finally 与 return 的交互")
print("=" * 60)


def finally_return():
    try:
        return "try 中的 return"
    finally:
        return "finally 中的 return"   # 会覆盖 try 的 return


print(f"  结果: {finally_return()}")


print("\n" + "=" * 60)
print("8. 获取异常信息: as 关键字 + traceback")
print("=" * 60)

import traceback

try:
    1 / 0
except ZeroDivisionError as e:
    print(f"  异常对象: {e!r}")
    print(f"  异常类型: {type(e).__name__}")
    print(f"  异常参数: {e.args}")
    print("  完整 traceback:")
    traceback.print_exc(limit=1)
