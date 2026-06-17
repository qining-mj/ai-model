"""
Python 元组操作综合演示
运行: python tuples.py
"""

# ============================================================
# 1. 创建元组
# ============================================================
print("=== 创建元组 ===")
t1 = (1, 2, 3)
t2 = 1, 2, 3           # 省略括号也可以
t3 = (5,)              # 单元素元组 — 逗号不能省!
t4 = ()                # 空元组
print(f"t1 = {t1}, type = {type(t1)}")
print(f"t2 = {t2}")
print(f"t3 = {t3}, len = {len(t3)}")
print(f"t4 = {t4}")
print(f"t1[0] = {t1[0]}")

# ============================================================
# 2. 不可变性演示
# ============================================================
print("\n=== 不可变性 ===")
t = (1, 2, 3)
# t[0] = 10           # TypeError: 'tuple' object does not support item assignment
# t.append(4)         # AttributeError
print(f"元组 {t} 的内容不能被修改")
print("但元组中的可变对象可以修改:")
t_mut = ([1, 2], 3)   # 元组包含列表
t_mut[0].append(999)  # 列表可以修改 (元组本身没变)
print(f"  t_mut = {t_mut}")

# ============================================================
# 3. 访问和切片
# ============================================================
print("\n=== 访问和切片 ===")
t = (0, 1, 2, 3, 4, 5)
print(f"t[0]     = {t[0]}")
print(f"t[-1]    = {t[-1]}")
print(f"t[1:4]   = {t[1:4]}")
print(f"t[::-1]  = {t[::-1]}")

# ============================================================
# 4. 解包 (Unpacking)
# ============================================================
print("\n=== 解包 ===")
# 基本解包
a, b, c = (1, 2, 3)
print(f"a={a}, b={b}, c={c}")

# 交换变量
x, y = 10, 20
x, y = y, x
print(f"交换后: x={x}, y={y}")

# * 运算符解包
first, second, *rest = (1, 2, 3, 4, 5)
print(f"first={first}, second={second}, rest={rest}")

first, *middle, last = (1, 2, 3, 4, 5)
print(f"first={first}, middle={middle}, last={last}")

# ============================================================
# 5. 内置函数
# ============================================================
print("\n=== 内置函数 ===")
nums = (3, 1, 4, 1, 5, 9)
print(f"nums = {nums}")
print(f"len:  {len(nums)}")
print(f"max:  {max(nums)}")
print(f"min:  {min(nums)}")
print(f"sum:  {sum(nums)}")
print(f"sorted: {sorted(nums)}")   # 返回列表
print(f"3 in nums: {3 in nums}")

# ============================================================
# 6. 元组的用途
# ============================================================
print("\n=== 典型用途 ===")
# 函数返回多个值
def min_max(items):
    return min(items), max(items)

result = min_max([3, 1, 4, 1, 5])
print(f"min_max([3,1,4,1,5]) = {result}")
low, high = result
print(f"low={low}, high={high}")

# 字典的 key (元组是不可变的, 可以做 key)
d = {(0, 0): "原点", (1, 0): "右"}
print(f"字典以元组为 key: {d}")

# 记录/命名元组替代
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(f"namedtuple: Point(3,4), x={p.x}, y={p.y}")

print("\n元组演示完毕！")
