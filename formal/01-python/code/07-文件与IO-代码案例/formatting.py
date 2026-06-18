"""
输出格式化 — Output Formatting
演示 % 格式化、str.format()、f-string（推荐）。
"""

print("=" * 60)
print("1. % 格式化（旧风格）")
print("=" * 60)

name = "Alice"
age = 25
score = 92.5678

print("  姓名: %s, 年龄: %d, 分数: %.1f" % (name, age, score))
print("  整数: %5d, 左对齐: %-5d, 补零: %05d" % (42, 42, 42))
print("  浮点: %8.2f, 科学: %e" % (3.14159, 3.14159))


print("\n" + "=" * 60)
print("2. str.format() 方法")
print("=" * 60)

print("  姓名: {}, 年龄: {}".format(name, age))
print("  {1} 今年 {0} 岁".format(age, name))
print("  {name} 的分数是 {score:.2f}".format(name="Bob", score=87.3))
print("  二进制: {0:b}, 十六进制: {0:x}".format(255))

# 对齐
print("  |{:<10}|{:^10}|{:>10}|".format("左", "中", "右"))
print("  |{:*<10}|{:*^10}|{:*>10}|".format("左", "中", "右"))


print("\n" + "=" * 60)
print("3. f-string（推荐 — Python 3.6+）")
print("=" * 60)

print(f"  姓名: {name}, 年龄: {age}")
print(f"  分数: {score:.2f}, 四舍五入: {score:.0f}")

# 对齐与填充
value = 42
print(f"  |{value:<10}|{value:^10}|{value:>10}|")
print(f"  |{value:*<10}|{value:*^10}|{value:*>10}|")

# 数字分组
big = 123456789
print(f"  千分位: {big:,}")
print(f"  二进制: {big:b}, 八进制: {big:o}, 十六进制: {big:x}")

# 表达式
print(f"  算术: {15 + 27}")

# 调用方法
print(f"  大写: {name.upper()}")

# 调试格式 (Python 3.8+)
x = 10
y = 20
print(f"  {x=}, {y=}, {x + y=}")


print("\n" + "=" * 60)
print("4. 精度与类型码")
print("=" * 60)

pi = 3.1415926535
print(f"  pi = {pi}")
print(f"  pi 保留 2 位: {pi:.2f}")
print(f"  pi 保留 4 位: {pi:.4f}")
print(f"  百分比: {0.875:.1%}")
print(f"  指数: {pi:e}, 指数 2 位: {pi:.2e}")


print("\n" + "=" * 60)
print("5. 格式规范迷你语言汇总")
print("=" * 60)

print("  [[fill]align][sign][#][0][width][grouping][.precision][type]")
print("  示例:")
print(f"  {12345:=>+10,.2f}")       # 填充= + 宽度10 千分位 2位小数 浮点
