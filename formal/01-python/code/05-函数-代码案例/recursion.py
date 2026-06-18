"""
Python 递归函数演示 — 阶乘、斐波那契、递归深度与优化
运行: python recursion.py
"""

# ============================================================
# 1. 阶乘 — 递归 vs 迭代
# ============================================================
print("=== 阶乘 ===")

def factorial_recursive(n: int) -> int:
    """递归计算阶乘"""
    if n <= 1:          # 基准情况 (base case)
        return 1
    return n * factorial_recursive(n - 1)   # 递归调用

def factorial_iterative(n: int) -> int:
    """迭代计算阶乘"""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

for n in range(0, 11):
    r = factorial_recursive(n)
    i = factorial_iterative(n)
    print(f"  {n}! = {r} (递归), {i} (迭代)")
    assert r == i

# ============================================================
# 2. 斐波那契数列 — 朴素递归 (效率低)
# ============================================================
print("\n=== 斐波那契: 朴素递归 (低效) ===")

def fib_naive(n: int) -> int:
    """朴素递归 — O(2^n), 存在大量重复计算"""
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

# n 小的时候还 OK
for i in range(10):
    print(f"  fib({i}) = {fib_naive(i)}")
# 注意: fib_naive(40) 就会非常慢!

# ============================================================
# 3. 斐波那契 — 记忆化递归 (Memoization)
# ============================================================
print("\n=== 斐波那契: 记忆化递归 (优化) ===")

def fib_memo(n: int, memo: dict = None) -> int:
    """带记忆化的递归 — O(n)"""
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

for i in range(20):
    print(f"  fib_memo({i}) = {fib_memo(i)}")

# ============================================================
# 4. 递归深度限制
# ============================================================
print("\n=== 递归深度限制 ===")
import sys
print(f"  默认递归深度限制: {sys.getrecursionlimit()}")

def recurse(level: int):
    """递归直到达到深度限制"""
    print(f"  深度: {level}", end="\r")
    recurse(level + 1)

print("  尝试递归过深...")
try:
    recurse(1)
except RecursionError as e:
    print(f"\n  触发 RecursionError: {e}")

# 可以调整递归限制 (不推荐过大)
# sys.setrecursionlimit(5000)
print(f"  当前递归限制: {sys.getrecursionlimit()}")

print("\n递归演示完毕！")
