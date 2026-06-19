"""
Python 循环演示 — while 和 for
运行: python loops.py
"""

# ============================================================
# 1. while 循环
# ============================================================
print("=== while 循环 ===")
count = 1
while count <= 5:
    print(f"  while 迭代 #{count}")
    count += 1

# ============================================================
# 2. while + else
# ============================================================
print("\n=== while + else ===")
# else 在循环正常结束时执行 (没有被 break)
n = 0
while n < 3:
    print(f"  n = {n}")
    n += 1
else:
    print("  循环正常结束 (未被 break)")

# break 时 else 不执行
print("\n  --- break 测试 ---")
n = 0
while n < 5:
    if n == 3:
        print("  n == 3, break!")
        break
    print(f"  n = {n}")
    n += 1
else:
    print("  这行不会打印")

# ============================================================
# 3. for 循环 — 遍历序列
# ============================================================
print("\n=== for 循环 ===")
# 遍历列表
fruits = ["apple", "banana", "cherry"]
print("  fruits:")
for fruit in fruits:
    print(f"    - {fruit}")

# 遍历字符串
print("  'Python' 中的字符:")
for ch in "Python":
    print(f"    '{ch}'")

# 遍历字典
d = {"name": "Alice", "age": 25, "city": "Beijing"}
print("  字典 items:")
for key, value in d.items():
    print(f"    {key} -> {value}")

# ============================================================
# 4. for + else
# ============================================================
print("\n=== for + else ===")
numbers = [1, 3, 5, 7, 9]
for n in numbers:
    if n > 10:
        print(f"  找到 > 10 的数字: {n}")
        break
else:
    print("  没有找到大于 10 的数字")

# ============================================================
# 5. range(start, stop, step)
# ============================================================
print("\n=== range() ===")
print(f"  range(5):        {list(range(5))}")       # [0,1,2,3,4]
print(f"  range(2, 7):     {list(range(2, 7))}")    # [2,3,4,5,6]
print(f"  range(0, 10, 2): {list(range(0, 10, 2))}")  # [0,2,4,6,8]
print(f"  range(10, 0, -2): {list(range(10, 0, -2))}") # [10,8,6,4,2]

# ============================================================
# 6. enumerate() — 获取索引和值
# ============================================================
print("\n=== enumerate() ===")
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"  index={index}, fruit='{fruit}'")

# 指定起始值
for index, fruit in enumerate(fruits, start=1):
    print(f"  #{index}: {fruit}")

print("\n循环演示完毕！")
