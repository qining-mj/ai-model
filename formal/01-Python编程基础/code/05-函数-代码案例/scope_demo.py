"""
Python 作用域演示 — LEGB 规则 (Local, Enclosing, Global, Built-in)
运行: python scope_demo.py
"""

# ============================================================
# LEGB 规则: Local → Enclosing → Global → Built-in
# ============================================================

# 全局变量 (Global)
x = "global x"
y = "global y"

def outer():
    """外层函数 — 创建 Enclosing 作用域"""
    x = "outer x"            # 封闭作用域 (Enclosing)
    z = "outer z"

    def inner():
        """内层函数 — 创建 Local 作用域"""
        x = "inner x"        # 局部变量 (Local)
        print(f"  inner 中的 x: {x}")   # inner x (Local)
        # 如果没有局部 x, 会找 enclosing 的 x
        # 如果 enclosing 也没有, 找 global
        # 再找不到, 找 built-in
        print(f"  inner 中的 y: {y}")   # global y

    inner()
    print(f"  outer 中的 x: {x}")      # outer x
    print(f"  outer 中的 z: {z}")      # outer z

print("=== LEGB 规则 ===")
outer()
print(f"  全局 x: {x}")               # global x

# ============================================================
# global 关键字 — 在函数内修改全局变量
# ============================================================
print("\n=== global 关键字 ===")
counter = 0

def increment():
    global counter          # 声明使用全局变量
    counter += 1            # 没有 global 会报 UnboundLocalError
    print(f"  counter = {counter}")

increment()
increment()
print(f"  全局 counter: {counter}")

# ============================================================
# nonlocal 关键字 — 修改封闭作用域的变量
# ============================================================
print("\n=== nonlocal 关键字 ===")
def make_counter():
    count = 0               # Enclosing 变量

    def increment():
        nonlocal count      # 声明使用封闭作用域的变量
        count += 1
        return count

    return increment

counter_fn = make_counter()
print(f"  第一次调用: {counter_fn()}")
print(f"  第二次调用: {counter_fn()}")
print(f"  第三次调用: {counter_fn()}")

# ============================================================
# 闭包 (Closure) 演示
# ============================================================
print("\n=== 闭包 (Closure) ===")
def multiply_by(n):
    """返回一个乘以 n 的函数"""
    def multiplier(x):
        return x * n
    return multiplier

times_2 = multiply_by(2)
times_3 = multiply_by(3)

print(f"  times_2(5) = {times_2(5)}")     # 10
print(f"  times_3(5) = {times_3(5)}")     # 15
print(f"  times_2.__closure__: {times_2.__closure__}")

# ============================================================
# Built-in 作用域
# ============================================================
print("\n=== Built-in 作用域 ===")
# 内置函数 (如 len, print, range) 在 built-in 作用域
print(f"  len 是内置函数: {len}")
print(f"  builtins 模块中的函数列表:")
import builtins
builtin_names = [name for name in dir(builtins) if not name.startswith("_")]
print(f"  共 {len(builtin_names)} 个内置函数/类型")

print("\n作用域演示完毕！")
