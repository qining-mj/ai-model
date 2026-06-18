"""
Python 推导式综合演示 — 列表、字典、集合、生成器
运行: python comprehensions.py
"""

# ============================================================
# 1. 列表推导式
# ============================================================
print("=== 列表推导式 ===")
# 基本
squares = [x ** 2 for x in range(10)]
print(f"平方: {squares}")

# 条件过滤
evens = [x for x in range(20) if x % 2 == 0]
print(f"偶数: {evens}")

# 嵌套循环
pairs = [(x, y) for x in range(3) for y in range(3)]
print(f"坐标对: {pairs}")

# 三元表达式在推导式中
labels = ["even" if x % 2 == 0 else "odd" for x in range(10)]
print(f"奇偶标签: {labels}")

# ============================================================
# 2. 字典推导式
# ============================================================
print("\n=== 字典推导式 ===")
squares_dict = {x: x ** 2 for x in range(5)}
print(f"平方字典: {squares_dict}")

# 条件过滤
filtered = {k: v for k, v in squares_dict.items() if v % 2 == 0}
print(f"偶数平方: {filtered}")

# 交换键值
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(f"交换键值: {swapped}")

# ============================================================
# 3. 集合推导式
# ============================================================
print("\n=== 集合推导式 ===")
nums = [1, 2, 2, 3, 3, 4, 4, 5]
unique_squares = {x ** 2 for x in nums}
print(f"唯一平方值: {unique_squares}")

# 过滤
even_set = {x for x in range(20) if x % 2 == 0}
print(f"偶数集合: {even_set}")

# ============================================================
# 4. 生成器表达式 (Generator Expression)
# ============================================================
print("\n=== 生成器表达式 ===")
# 生成器 — 惰性求值, 节省内存
gen = (x ** 2 for x in range(10))
print(f"生成器对象: {gen}")
print(f"转为列表: {list(gen)}")   # 只能迭代一次!

# 生成器用于 sum/max/min 等函数
total = sum(x ** 2 for x in range(10))
print(f"sum(x**2 for x in range(10)) = {total}")

# ============================================================
# 5. 嵌套推导式
# ============================================================
print("\n=== 嵌套推导式 ===")
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(f"矩阵展开: {flat}")

# 矩阵转置
transposed = [[row[i] for row in matrix] for i in range(3)]
print(f"矩阵转置: {transposed}")

# ============================================================
# 6. 性能对比 (列表推导式 vs 循环)
# ============================================================
print("\n=== 性能对比 ===")
import time

def using_loop(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

def using_comp(n):
    return [i ** 2 for i in range(n)]

n = 10_000_000
# 只演示逻辑, 不实际跑大数据量
print(f"列表推导式通常比 for 循环快 2-3 倍")
print(f"但对于 {n:,} 个元素, 两者都 O(n) 复杂度")

print("\n推导式演示完毕！")
