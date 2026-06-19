"""
Python Lambda 表达式演示
运行: python lambda_demo.py
"""

# ============================================================
# 1. 基本 Lambda
# ============================================================
print("=== 基本 lambda ===")

# 普通函数
def add(a, b):
    return a + b

# 等价的 lambda
add_lambda = lambda a, b: a + b

print(f"  普通函数: add(3, 5) = {add(3, 5)}")
print(f"  lambda:   add_lambda(3, 5) = {add_lambda(3, 5)}")

# 无参数 lambda
greeting = lambda: "Hello, World!"
print(f"  无参数 lambda: {greeting()}")

# ============================================================
# 2. lambda 在 sorted() 中
# ============================================================
print("\n=== lambda 在 sorted() 中 ===")

people = [
    ("Alice", 25, 165),
    ("Bob", 30, 175),
    ("Charlie", 20, 180),
]

# 按年龄排序
sorted_by_age = sorted(people, key=lambda p: p[1])
print(f"  按年龄排序: {sorted_by_age}")

# 按身高降序
sorted_by_height = sorted(people, key=lambda p: p[2], reverse=True)
print(f"  按身高降序: {sorted_by_height}")

# dict 排序
scores = {"Alice": 90, "Bob": 75, "Charlie": 85}
sorted_names = sorted(scores.items(), key=lambda item: item[1])
print(f"  按分数排序: {sorted_names}")

# ============================================================
# 3. lambda 在 map() 中
# ============================================================
print("\n=== lambda 在 map() 中 ===")
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(f"  平方: {squared}")

celsius = [0, 10, 20, 30, 40]
fahrenheit = list(map(lambda c: c * 9 / 5 + 32, celsius))
print(f"  摄氏转华氏: {fahrenheit}")

# ============================================================
# 4. lambda 在 filter() 中
# ============================================================
print("\n=== lambda 在 filter() 中 ===")
numbers = list(range(1, 21))
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"  偶数: {evens}")

# 筛选长度 > 5 的单词
words = ["apple", "banana", "cherry", "date", "elderberry"]
long_words = list(filter(lambda w: len(w) > 5, words))
print(f"  长单词 (len>5): {long_words}")

# ============================================================
# 5. lambda 的局限性
# ============================================================
print("\n=== lambda 局限性 ===")
# lambda 只能包含单个表达式, 不能包含语句
# 下列操作在 lambda 中非法:
#   - 赋值 (=)  — 但海象运算符 := 可以
#   - return
#   - if/elif/else 语句 — 但三元表达式可以
#   - for/while 循环
#   - try/except

# 合法: 三元表达式
sign = lambda x: "positive" if x > 0 else "negative" if x < 0 else "zero"
print(f"  sign(5) = {sign(5)}")

# 合法: 海象运算符 (Python 3.8+)
# 不推荐在 lambda 中使用, 影响可读性

# 复杂逻辑应使用普通函数
def process(x):
    """复杂逻辑用普通函数"""
    result = x * 2
    result += 10
    return result

print(f"  process(5) = {process(5)}")

print("\nLambda 演示完毕！")
