"""
Python 集合操作综合演示
运行: python sets.py
"""

# ============================================================
# 1. 创建集合
# ============================================================
print("=== 创建集合 ===")
s1 = {1, 2, 3, 3, 2}          # 自动去重
s2 = set([1, 2, 3, 3])        # 从列表创建
s3 = set("hello")              # 从字符串创建 (无序)
empty_set = set()              # 空集合 (不能用 {}, 那是空字典)
print(f"s1 = {s1}")
print(f"s2 = {s2}")
print(f"s3 = {s3}")
print(f"empty_set = {empty_set}")

# ============================================================
# 2. 添加元素
# ============================================================
print("\n=== 添加元素 ===")
s = {1, 2, 3}
s.add(4)
print(f"add(4): {s}")
s.update([5, 6, 7])   # 添加多个
print(f"update([5,6,7]): {s}")
s.update({8, 9}, [10])  # 多个可迭代对象
print(f"update({{8,9}}, [10]): {s}")

# ============================================================
# 3. 删除元素
# ============================================================
print("\n=== 删除元素 ===")
s = {1, 2, 3, 4, 5}
s.remove(3)          # 元素不存在会 KeyError
print(f"remove(3): {s}")
s.discard(99)        # discard 不会报错
print(f"discard(99): {s}")  # 没变化
popped = s.pop()     # pop 删除并返回任意元素
print(f"pop(): {popped}, 剩余: {s}")
s.clear()
print(f"clear(): {s}")

# ============================================================
# 4. 集合运算
# ============================================================
print("\n=== 集合运算 ===")
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}
print(f"A = {a}")
print(f"B = {b}")
print(f"  A & B = {a & b}")          # 交集
print(f"  A | B = {a | b}")          # 并集
print(f"  A - B = {a - b}")          # 差集 (在 A 不在 B)
print(f"  B - A = {b - a}")          # 差集 (在 B 不在 A)
print(f"  A ^ B = {a ^ b}")          # 对称差 (不同时在 A 和 B 中的元素)

# 方法形式
print(f"  A.intersection(B): {a.intersection(b)}")
print(f"  A.union(B):        {a.union(b)}")
print(f"  A.difference(B):   {a.difference(b)}")
print(f"  A.symmetric_difference(B): {a.symmetric_difference(b)}")

# ============================================================
# 5. 子集/超集判断
# ============================================================
print("\n=== 子集/超集 ===")
x = {1, 2, 3}
y = {1, 2, 3, 4, 5}
print(f"X = {x}")
print(f"Y = {y}")
print(f"  X <= Y (X 是 Y 的子集): {x <= y}")
print(f"  X < Y (X 是 Y 的真子集): {x < y}")
print(f"  Y >= X (Y 是 X 的超集): {y >= x}")
print(f"  Y > X (Y 是 X 的真超集): {y > x}")

# ============================================================
# 6. frozenset — 不可变集合
# ============================================================
print("\n=== frozenset ===")
fs = frozenset([1, 2, 3])
print(f"fs = {fs}")
# fs.add(4)     # AttributeError
# 可以作为字典的 key
d = {fs: "frozenset as key"}
print(f"frozenset 可作为 dict key: {d}")
# 常规 set 不能做 key
# d = {{1, 2}: "no"}  # TypeError: unhashable type: 'set'

print("\n集合演示完毕！")
