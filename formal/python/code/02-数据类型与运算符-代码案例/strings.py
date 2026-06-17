"""
Python 字符串操作演示
运行: python strings.py
"""

# ============================================================
# 1. 字符串创建 — 单引号、双引号、三引号
# ============================================================
print("=== 字符串创建 ===")
s1 = '单引号'
s2 = "双引号"
s3 = """三引号
支持换行"""
print(f"s1 = {s1}\ns2 = {s2}\ns3 = {s3}")

# ============================================================
# 2. 索引和切片 [start:end:step]
# ============================================================
print("\n=== 索引和切片 ===")
s = "Hello, Python"
print(f"字符串: '{s}'")
print(f"s[0]      = '{s[0]}'")          # H
print(f"s[-1]     = '{s[-1]}'")         # n (最后一个字符)
print(f"s[0:5]    = '{s[0:5]}'")        # Hello
print(f"s[7:]     = '{s[7:]}'")         # Python
print(f"s[::-1]   = '{s[::-1]}'")       # 反转
print(f"s[::2]    = '{s[::2]}'")        # 步长为 2

# ============================================================
# 3. 转义字符和原始字符串
# ============================================================
print("\n=== 转义字符和原始字符串 ===")
print("换行符:\n第二行")
print("制表符:\t缩进")
path_raw = r"C:\Users\name"             # 原始字符串 — 不处理转义
print(f"原始字符串: {path_raw}")
path_normal = "C:\\Users\\name"
print(f"普通字符串: {path_normal}")

# ============================================================
# 4. 字符串运算符
# ============================================================
print("\n=== 字符串运算符 ===")
print(f"'Hello' + ' ' + 'World' = {'Hello' + ' ' + 'World'}")
print(f"'Ha' * 3 = {'Ha' * 3}")
print(f"'Py' in 'Python' = {'Py' in 'Python'}")
print(f"'xyz' not in 'Python' = {'xyz' not in 'Python'}")

# ============================================================
# 5. f-string 格式化 (Python 3.6+)
# ============================================================
print("\n=== f-string 格式化 ===")
name, age, height = "Alice", 25, 1.68
print(f"姓名: {name}, 年龄: {age}, 身高: {height:.2f}m")
print(f"计算: {5 * 6} = 30")
print(f"对齐: {'你好':>10} | {'你好':<10} | {'你好':^10}")

# ============================================================
# 6. 常用字符串方法
# ============================================================
print("\n=== 常用字符串方法 ===")
text = "  Hello, Python World!  "
print(f"原文: '{text}'")
print(f"len: {len(text)}")
print(f"upper: '{text.upper()}'")
print(f"lower: '{text.lower()}'")
print(f"strip: '{text.strip()}'")
print(f"replace: '{text.replace('Python', 'Java')}'")

csv = "apple,banana,orange"
print(f"\ncsv: '{csv}'")
print(f"split: {csv.split(',')}")

words = ["Python", "is", "fun"]
print(f"join: '{' '.join(words)}'")

s = "Hello, welcome to Python programming"
print(f"\nfind('Python'): {s.find('Python')}")
print(f"startswith('Hello'): {s.startswith('Hello')}")
print(f"endswith('ing'): {s.endswith('ing')}")
print(f"count('o'): {s.count('o')}")

print("\n字符串演示完毕！")
