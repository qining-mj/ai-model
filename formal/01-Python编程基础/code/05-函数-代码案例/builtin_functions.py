"""
Python 内置函数演示 — map, filter, zip, sorted, enumerate, any, all
运行: python builtin_functions.py
"""

# ============================================================
# 1. map() — 对每个元素应用函数
# ============================================================
print("=== map() ===")
numbers = [1, 2, 3, 4, 5]

# 用 lambda
squared = list(map(lambda x: x ** 2, numbers))
print(f"  平方: {squared}")

# 用命名函数
def to_celsius(f):
    return (f - 32) * 5 / 9

fahrenheit = [32, 68, 86, 104]
celsius = list(map(to_celsius, fahrenheit))
print(f"  华氏 {fahrenheit} -> 摄氏 {[round(c, 1) for c in celsius]}")

# 多个可迭代对象
a = [1, 2, 3]
b = [4, 5, 6]
sums = list(map(lambda x, y: x + y, a, b))
print(f"  map 多参数: {a} + {b} = {sums}")

# ============================================================
# 2. filter() — 过滤元素
# ============================================================
print("\n=== filter() ===")
numbers = list(range(1, 21))

# 筛选偶数
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"  偶数: {evens}")

# 筛选质数
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = list(filter(is_prime, numbers))
print(f"  质数: {primes}")

# ============================================================
# 3. zip() — 打包多个可迭代对象
# ============================================================
print("\n=== zip() ===")
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["Beijing", "Shanghai", "Guangzhou"]

zipped = list(zip(names, ages, cities))
print(f"  zip 结果: {zipped}")

# 解包
for name, age, city in zipped:
    print(f"    {name}, {age}, from {city}")

# zip 用于字典构造
keys = ["name", "age", "city"]
values = ["Alice", 25, "Beijing"]
d = dict(zip(keys, values))
print(f"  dict(zip(...)): {d}")

# ============================================================
# 4. sorted() — 排序
# ============================================================
print("\n=== sorted() ===")
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"  原始:       {nums}")
print(f"  sorted:     {sorted(nums)}")
print(f"  降序:       {sorted(nums, reverse=True)}")

# 按绝对值排序
print(f"  按绝对值:   {sorted([-3, 1, -4, 2], key=abs)}")

# 按自定义规则
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78},
]
by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
print(f"  按成绩降序: {by_grade}")

# ============================================================
# 5. enumerate() — 带索引迭代
# ============================================================
print("\n=== enumerate() ===")
fruits = ["apple", "banana", "cherry", "date"]

for idx, fruit in enumerate(fruits):
    print(f"  {idx}: {fruit}")

for idx, fruit in enumerate(fruits, start=1):
    print(f"  #{idx}: {fruit}")

# ============================================================
# 6. any() 和 all()
# ============================================================
print("\n=== any() 和 all() ===")
nums = [0, 1, 2, 3, 4]
print(f"  nums = {nums}")
print(f"  any(x > 3 for x in nums): {any(x > 3 for x in nums)}")     # True (有 >3 的)
print(f"  all(x > 0 for x in nums): {all(x > 0 for x in nums)}")     # False (有 0)
print(f"  all(x >= 0 for x in nums): {all(x >= 0 for x in nums)}")   # True

# 实际应用: 检查列表
data = [100, 200, 300]
print(f"  data = {data}")
print(f"  所有值都 > 50? {all(v > 50 for v in data)}")
print(f"  有任何值 > 250? {any(v > 250 for v in data)}")

# 验证输入
def validate_user(user: dict) -> bool:
    required_fields = ["name", "age", "email"]
    return all(field in user for field in required_fields)

user1 = {"name": "Alice", "age": 25, "email": "alice@example.com"}
user2 = {"name": "Bob", "age": 30}
print(f"  user1 有效: {validate_user(user1)}")
print(f"  user2 有效: {validate_user(user2)}")

print("\n内置函数演示完毕！")
