"""
生成器函数与表达式 — Generator Functions and Expressions
演示 yield、生成器表达式、yield from 及流水线。
"""

print("=" * 60)
print("1. 基本生成器函数")
print("=" * 60)


def simple_gen():
    yield "A"
    yield "B"
    yield "C"


for val in simple_gen():
    print(f"  {val}")

print(f"  list(simple_gen()) = {list(simple_gen())}")


print("\n" + "=" * 60)
print("2. 带状态的生成器：斐波那契")
print("=" * 60)


def fibonacci(n: int):
    """生成前 n 个斐波那契数"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1


for i, f in enumerate(fibonacci(10), 1):
    print(f"  fib({i}) = {f}")


print("\n" + "=" * 60)
print("3. 生成器表达式 vs 列表推导式 — 内存对比")
print("=" * 60)

import sys

# 列表推导式：一次性生成所有元素
list_comp = [x ** 2 for x in range(1000000)]
print(f"  列表推导式大小: {sys.getsizeof(list_comp) // 1024:,} KB")

# 生成器表达式：惰性求值
gen_expr = (x ** 2 for x in range(1000000))
print(f"  生成器表达式大小: {sys.getsizeof(gen_expr)} bytes")

# 但遍历结果是相同的
small_gen = (x ** 2 for x in range(5))
print(f"  生成器内容: {list(small_gen)}")


print("\n" + "=" * 60)
print("4. yield from — 委托给子生成器")
print("=" * 60)


def sub_gen():
    yield "来自子生成器"
    yield "也在子生成器中"


def main_gen():
    yield "来自主生成器"
    yield from sub_gen()
    yield "主生成器继续"


for val in main_gen():
    print(f"  {val}")


print("\n" + "=" * 60)
print("5. 生成器流水线 — 数据处理的 Unix 风格")
print("=" * 60)

lines = [
    "  苹果 3",
    "香蕉 5  ",
    "  樱桃 2  ",
    "",
    "# 这是注释",
    "  ！无效行",
    " 榴莲 1",
]


def tokenize(lines):
    """去除空格，跳过空行"""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        yield line


def parse(tokens):
    """解析为 (名称, 数量) 元组"""
    for token in tokens:
        parts = token.split()
        if len(parts) != 2:
            continue
        try:
            name = parts[0]
            count = int(parts[1])
            yield name, count
        except ValueError:
            continue


def filter_positive(items):
    """只保留数量 > 0 的项"""
    for name, count in items:
        if count > 0:
            yield name, count


# 流水线：tokenize -> parse -> filter_positive
pipeline = filter_positive(parse(tokenize(lines)))
for name, count in pipeline:
    print(f"  {name}: {count}")


print("\n" + "=" * 60)
print("6. 生成器是迭代器，只能遍历一次")
print("=" * 60)

g = (x for x in [1, 2, 3])
print(f"  list(g) = {list(g)}")
print(f"  list(g) = {list(g)}")       # 已耗尽
