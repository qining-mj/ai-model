"""
Python 条件判断演示 — if/elif/else + match/case (Python 3.10+)
运行: python conditionals.py
"""

# ============================================================
# 1. if-elif-else 链
# ============================================================
print("=== if-elif-else 链 ===")
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"分数: {score}, 等级: {grade}")

# ============================================================
# 2. 三元运算符 (条件表达式)
# ============================================================
print("\n=== 三元运算符 ===")
age = 20
status = "成年" if age >= 18 else "未成年"
print(f"年龄 {age}: {status}")

# 嵌套三元 (不推荐, 可读性差)
x = 5
result = "正数" if x > 0 else "负数" if x < 0 else "零"
print(f"x={x}: {result}")

# ============================================================
# 3. 嵌套 if
# ============================================================
print("\n=== 嵌套 if ===")
x, y = 10, 5

if x > 0:
    if y > 0:
        print("第一象限")
    else:
        print("第四象限")
else:
    print("不在第一/四象限")

# ============================================================
# 4. match/case (Python 3.10+)
# ============================================================
print("\n=== match/case (Python 3.10+) ===")

# 4a. 字面量匹配
def describe_day(day):
    match day:
        case 1 | 2 | 3 | 4 | 5:
            return "工作日"
        case 6 | 7:
            return "周末"
        case _:
            return "无效日期"

for d in [1, 6, 8]:
    print(f"  day={d}: {describe_day(d)}")

# 4b. 序列匹配
def process_command(cmd):
    match cmd.split():
        case ["quit"]:
            return "退出程序"
        case ["hello", name]:
            return f"你好, {name}!"
        case ["add", *items]:
            return f"添加: {items}"
        case _:
            return "未知命令"

print(f"\n  命令 'quit': {process_command('quit')}")
print(f"  命令 'hello Alice': {process_command('hello Alice')}")
print(f"  命令 'add 1 2 3': {process_command('add 1 2 3')}")

# 4c. 映射匹配 + guard
def process_point(point):
    match point:
        case {"x": x, "y": y} if x == y:
            return f"点在对角线上: ({x}, {y})"
        case {"x": x, "y": y}:
            return f"普通点: ({x}, {y})"
        case _:
            return "不是有效的点"

print(f"\n  {{'x': 3, 'y': 3}}: {process_point({'x': 3, 'y': 3})}")
print(f"  {{'x': 3, 'y': 4}}: {process_point({'x': 3, 'y': 4})}")

print("\n条件判断演示完毕！")
