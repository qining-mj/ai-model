"""
Python 数据类型演示 — 变量、六大标准类型、type()/isinstance()
运行: python data_types.py
"""

# ============================================================
# 1. 动态类型 (Dynamic Typing)
# ============================================================
print("=== 动态类型 ===")
var = 10          # 此时是 int
print(f"var = {var}, type = {type(var)}")
var = "hello"     # 同一变量变为 str
print(f"var = '{var}', type = {type(var)}")
var = 3.14        # 变为 float
print(f"var = {var}, type = {type(var)}")

# ============================================================
# 2. 多变量赋值
# ============================================================
print("\n=== 多变量赋值 ===")
a, b, c = 1, 2, 3
print(f"a={a}, b={b}, c={c}")

x = y = z = 0     # 链式赋值
print(f"x={x}, y={y}, z={z}")

# ============================================================
# 3. 六大标准类型
# ============================================================
print("\n=== 六大标准数据类型 ===")

# 3a. Number (数字): int, float, complex
n_int = 42
n_float = 3.14
n_complex = 1 + 2j
print(f"int: {n_int}, float: {n_float}, complex: {n_complex}")

# 3b. String (字符串)
s = "Hello Python"
print(f"str: '{s}'")

# 3c. List (列表)
lst = [1, 2, 3, "a", "b"]
print(f"list: {lst}")

# 3d. Tuple (元组)
t = (1, 2, 3)
print(f"tuple: {t}")

# 3e. Set (集合)
st = {1, 2, 3, 3, 2}   # 自动去重
print(f"set: {st}")

# 3f. Dictionary (字典)
d = {"name": "Alice", "age": 25}
print(f"dict: {d}")

# ============================================================
# 4. type() vs isinstance()
# ============================================================
print("\n=== type() vs isinstance() ===")

value = True
print(f"type(value) = {type(value)}")                     # <class 'bool'>
print(f"isinstance(value, int) = {isinstance(value, int)}")  # True! bool 是 int 的子类
print(f"type(value) is int = {type(value) is int}")        # False — type 不考虑继承

# isinstance 适合检查类型层次
print(f"isinstance(value, (int, float, bool)) = {isinstance(value, (int, float, bool))}")

# ============================================================
# 5. 真值测试 (Truthiness)
# ============================================================
print("\n=== 真值测试 ===")
# 以下值被视为 False
falsy_values = [None, False, 0, 0.0, "", [], (), {}, set()]
for val in falsy_values:
    print(f"  bool({val!r}) = {bool(val)}")

# 其余所有值被视为 True
print(f"  bool(42) = {bool(42)}")
print(f"  bool('hello') = {bool('hello')}")
print(f"  bool([0]) = {bool([0])}")

print("\n数据类型演示完毕！")
