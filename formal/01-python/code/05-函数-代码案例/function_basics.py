"""
Python 函数基础演示 — def、docstring、参数、返回值
运行: python function_basics.py
"""

# ============================================================
# 1. 函数定义 + 文档字符串 (docstring)
# ============================================================
def greet(name: str) -> str:
    """
    向指定的人问好。

    参数:
        name: 人的名字

    返回:
        问候语字符串
    """
    return f"Hello, {name}!"

# 调用并查看 docstring
print("=== 函数定义与 docstring ===")
print(greet("Alice"))
print(f"函数的文档: {greet.__doc__}")

# ============================================================
# 2. 多个返回值 (实际是打包为元组)
# ============================================================
print("\n=== 多个返回值 ===")
def min_max(items):
    """返回序列的最小值和最大值"""
    return min(items), max(items)

result = min_max([3, 1, 4, 1, 5, 9, 2, 6])
print(f"min_max([3,1,4,1,5,9,2,6]) = {result}")
print(f"类型: {type(result)}")

# 解包接收
low, high = min_max([3, 1, 4, 1, 5])
print(f"解包: low={low}, high={high}")

# ============================================================
# 3. 返回 None
# ============================================================
print("\n=== None 返回 ===")
def print_message(msg: str):
    """打印消息, 不返回值"""
    print(f"  消息: {msg}")
    # 没有 return 语句, 隐式返回 None

def explicit_none():
    """显式返回 None"""
    return None

result1 = print_message("你好")
result2 = explicit_none()
print(f"无 return: result = {result1}")
print(f"return None: result = {result2}")
print(f"result is None: {result2 is None}")

# ============================================================
# 4. 单返回值函数的类型
# ============================================================
print("\n=== 返回值类型 ===")
def add(a: int, b: int) -> int:
    return a + b

def is_even(n: int) -> bool:
    return n % 2 == 0

print(f"add(3, 5) = {add(3, 5)}")
print(f"is_even(4) = {is_even(4)}")

# 类型提示只是提示, 不会强制检查
print(f"add('Hello ', 'World') = {add('Hello ', 'World')}")  # 也能工作

print("\n函数基础演示完毕！")
