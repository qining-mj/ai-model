"""
Python 字典操作综合演示
运行: python dicts.py
"""

# ============================================================
# 1. 创建字典
# ============================================================
print("=== 创建字典 ===")
d1 = {"name": "Alice", "age": 25}
d2 = dict(name="Bob", age=30)           # dict() 构造
d3 = dict([("a", 1), ("b", 2)])         # 从键值对列表
d4 = dict(zip(["x", "y"], [10, 20]))    # 从两个序列
print(f"d1 = {d1}")
print(f"d2 = {d2}")
print(f"d3 = {d3}")
print(f"d4 = {d4}")

# ============================================================
# 2. Key 必须是不可变类型
# ============================================================
print("\n=== Key 的不可变性 ===")
d = {}
d["str"] = 1         # str ok
d[42] = 2            # int ok
d[(1, 2)] = 3        # tuple ok
# d[[1, 2]] = 4      # list → TypeError: unhashable type: 'list'
# d[{"a": 1}] = 5    # dict → TypeError
print(f"字典: {d}")

# ============================================================
# 3. 访问元素
# ============================================================
print("\n=== 访问元素 ===")
d = {"name": "Alice", "age": 25, "city": "Beijing"}
print(f"d['name'] = {d['name']}")
print(f"d.get('age') = {d.get('age')}")
print(f"d.get('country', 'China') = {d.get('country', 'China')}")  # 默认值
# print(d['country'])  # KeyError!

# ============================================================
# 4. CRUD 操作
# ============================================================
print("\n=== CRUD 操作 ===")
d = {"x": 1}

# Create
d["y"] = 2
print(f"添加: {d}")

# Read
print(f"读取: d['x'] = {d['x']}")

# Update
d["x"] = 100
print(f"更新: {d}")

# Delete
del d["y"]
print(f"del: {d}")

# ============================================================
# 5. 迭代
# ============================================================
print("\n=== 迭代 ===")
d = {"a": 1, "b": 2, "c": 3}
print("keys:")
for k in d:
    print(f"  {k}")
print(f"  keys(): {list(d.keys())}")
print(f"  values(): {list(d.values())}")
print(f"  items(): {list(d.items())}")

for k, v in d.items():
    print(f"  {k} -> {v}")

# ============================================================
# 6. 常用方法
# ============================================================
print("\n=== 常用方法 ===")
d = {"a": 1, "b": 2}

# setdefault — 不存在才设置
d.setdefault("c", 3)
d.setdefault("a", 999)     # a 已经存在, 不会覆盖
print(f"setdefault: {d}")

# pop — 删除并返回值
val = d.pop("b")
print(f"pop('b') = {val}, 剩余: {d}")

# popitem — 删除并返回最后一个键值对 (LIFO)
d["x"] = 10
d["y"] = 20
item = d.popitem()
print(f"popitem() = {item}, 剩余: {d}")

# update — 合并另一个字典
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
d1.update(d2)
print(f"update: {d1}")

# fromkeys — 用序列创建字典
keys = ["name", "age", "city"]
d = dict.fromkeys(keys, "unknown")
print(f"fromkeys: {d}")

# ============================================================
# 7. 嵌套字典
# ============================================================
print("\n=== 嵌套字典 ===")
users = {
    "alice": {"age": 25, "city": "Beijing"},
    "bob": {"age": 30, "city": "Shanghai"},
}
print(f"users['alice']['city'] = {users['alice']['city']}")

# ============================================================
# 8. 合并操作符 | (Python 3.9+)
# ============================================================
print("\n=== 合并操作符 | (Python 3.9+) ===")
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
merged = d1 | d2
print(f"d1 | d2 = {merged}")
d1 |= d2   # 就地合并
print(f"d1 |= d2 = {d1}")

print("\n字典演示完毕！")
