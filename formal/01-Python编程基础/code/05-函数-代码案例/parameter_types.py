"""
Python 参数类型综合演示 — 位置参数、默认参数、关键字参数、/、*、*args、**kwargs
运行: python parameter_types.py
"""

# ============================================================
# 1. 位置参数 (Positional)
# ============================================================
print("=== 位置参数 ===")
def describe_person(name, age, city):
    print(f"  {name} is {age} years old, from {city}")

describe_person("Alice", 25, "Beijing")  # 按位置传递

# ============================================================
# 2. 默认参数 (Default)
# ============================================================
print("\n=== 默认参数 ===")
def greet(name, greeting="Hello"):
    print(f"  {greeting}, {name}!")

greet("Alice")              # 使用默认 greeting
greet("Bob", "Hi")          # 覆盖默认值

# 默认参数的陷阱: 可变默认值只初始化一次
def add_item(item, items=[]):
    items.append(item)
    return items

print("\n  默认参数可变对象陷阱:")
print(f"    第一次: {add_item('a')}")     # ['a']
print(f"    第二次: {add_item('b')}")     # ['a', 'b']  — 共用同一个列表!

# 正确做法: 使用 None 作为默认值
def add_item_safe(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print(f"    安全版第一次: {add_item_safe('a')}")
print(f"    安全版第二次: {add_item_safe('b')}")

# ============================================================
# 3. 关键字参数 (Keyword)
# ============================================================
print("\n=== 关键字参数 ===")
def introduce(name, age, city):
    print(f"  {name}, {age}, from {city}")

introduce(age=30, city="Shanghai", name="Charlie")  # 顺序不重要

# ============================================================
# 4. 强制位置参数 / (Positional-Only)
# ============================================================
print("\n=== 强制位置参数 / ===")
def divide(a, b, /):
    """a 和 b 必须用位置参数传递"""
    return a / b

print(f"  divide(10, 3) = {divide(10, 3):.2f}")
# divide(a=10, b=3)  # TypeError!

# ============================================================
# 5. 强制关键字参数 *
# ============================================================
print("\n=== 强制关键字参数 * ===")
def create_user(name, age, *, city="Beijing"):
    """city 必须是关键字参数"""
    print(f"  {name}, {age}, from {city}")

create_user("Alice", 25, city="Shanghai")
# create_user("Alice", 25, "Shanghai")  # TypeError!

# ============================================================
# 6. *args — 可变位置参数
# ============================================================
print("\n=== *args ===")
def sum_all(*args):
    """接收任意数量的位置参数"""
    print(f"  参数: {args}")
    return sum(args)

print(f"  sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
print(f"  sum_all(10, 20)  = {sum_all(10, 20)}")

# ============================================================
# 7. **kwargs — 可变关键字参数
# ============================================================
print("\n=== **kwargs ===")
def print_config(**kwargs):
    """接收任意数量的关键字参数"""
    for key, value in kwargs.items():
        print(f"  {key} = {value}")

print_config(db_host="localhost", db_port=3306, debug=True)

# ============================================================
# 8. 参数顺序 (完整展示)
# ============================================================
print("\n=== 完整参数顺序 ===")
# 规则: 位置参数 / 强制位置, *args, 关键字参数, **kwargs
def complex_func(a, b, /, c, d, *, e, **kwargs):
    print(f"  a={a}, b={b}, c={c}, d={d}, e={e}, kwargs={kwargs}")

complex_func(1, 2, 3, d=4, e=5, extra="data", verbose=True)

print("\n参数类型演示完毕！")
