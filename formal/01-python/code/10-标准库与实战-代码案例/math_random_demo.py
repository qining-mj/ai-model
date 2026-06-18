"""
Math 与 Random 模块
演示 math 模块的数学函数与 random 模块的各种随机操作。
"""

import math
import random

print("=" * 60)
print("1. math 模块 — 数学函数与常量")
print("=" * 60)

# 常量
print(f"  math.pi     = {math.pi}")
print(f"  math.e      = {math.e}")
print(f"  math.inf    = {math.inf}")
print(f"  math.nan    = {math.nan}")

# 取整
print(f"\n  math.ceil(3.14)  = {math.ceil(3.14)}")      # 向上取整
print(f"  math.floor(3.14) = {math.floor(3.14)}")      # 向下取整
print(f"  math.trunc(3.14) = {math.trunc(3.14)}")      # 截断小数
print(f"  round(3.5)       = {round(3.5)}")             # 内置四舍五入

# 幂与根
print(f"\n  math.pow(2, 10)   = {math.pow(2, 10)}")
print(f"  math.sqrt(144)    = {math.sqrt(144)}")
print(f"  144 ** 0.5        = {144 ** 0.5}")

# 对数
print(f"\n  math.log(100, 10) = {math.log(100, 10)}")   # 以 10 为底
print(f"  math.log(math.e)  = {math.log(math.e)}")      # 自然对数
print(f"  math.log2(1024)   = {math.log2(1024)}")        # 以 2 为底
print(f"  math.log10(1000)  = {math.log10(1000)}")       # 以 10 为底

# 三角函数
angle = math.radians(45)                                  # 角度转弧度
print(f"\n  sin(45°) = {math.sin(angle):.4f}")
print(f"  cos(45°) = {math.cos(angle):.4f}")
print(f"  tan(45°) = {math.tan(angle):.4f}")
print(f"  degrees(pi/4) = {math.degrees(math.pi / 4)}")


print("\n" + "=" * 60)
print("2. random 模块 — 随机数")
print("=" * 60)

# 0 ~ 1 之间的随机浮点数
print(f"  random.random()     = {random.random()}")

# 指定范围内的随机整数 [a, b]
print(f"  random.randint(1, 6)  = {random.randint(1, 6)}")   # 模拟骰子

# 指定范围内的随机浮点数 [a, b)
print(f"  random.uniform(0, 10) = {random.uniform(0, 10):.4f}")

# 从序列中随机选择
fruits = ["苹果", "香蕉", "樱桃", "榴莲", "葡萄"]
print(f"  random.choice:    {random.choice(fruits)}")

# 随机取样（不重复）
print(f"  random.sample(3): {random.sample(fruits, 3)}")

# 打乱顺序
cards = list(range(1, 11))
random.shuffle(cards)
print(f"  shuffle:          {cards}")

# 设置种子 — 可重现的随机
random.seed(42)
print(f"\n  种子=42 的随机:")
print(f"    {random.randint(1, 100)}, {random.randint(1, 100)}, {random.randint(1, 100)}")

random.seed(42)                                           # 重置种子
print(f"  再次种子=42 的随机:")
print(f"    {random.randint(1, 100)}, {random.randint(1, 100)}, {random.randint(1, 100)}")


print("\n" + "=" * 60)
print("3. 综合应用 — 模拟掷骰子统计")
print("=" * 60)

rolls = [random.randint(1, 6) + random.randint(1, 6) for _ in range(10000)]

# 计算每个和的出现次数
from collections import Counter
counts = Counter(rolls)

print("  两个骰子和的分布（10000 次):")
for total in range(2, 13):
    bar = "#" * (counts[total] // 50)
    print(f"    {total:2d}: {bar} ({counts[total]})")
