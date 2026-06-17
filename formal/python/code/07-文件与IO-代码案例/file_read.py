"""
文件读取 — Reading Files
演示 open()、read()、readline()、readlines()、for 循环逐行读取与分块读取。
"""

import os

# 准备一个测试文件
demo_file = os.path.join(os.path.dirname(__file__), "_demo_sample.txt")
with open(demo_file, "w", encoding="utf-8") as f:
    f.write("第一行: Hello, World!\n")
    f.write("第二行: Python 文件读写\n")
    f.write("第三行: 最后一行\n")

print("=" * 60)
print("1. read() — 读取全部内容")
print("=" * 60)

with open(demo_file, "r", encoding="utf-8") as f:
    content = f.read()
    print(f"  读取了 {len(content)} 个字符")
    print(repr(content))


print("\n" + "=" * 60)
print("2. readline() — 逐行读取")
print("=" * 60)

with open(demo_file, "r", encoding="utf-8") as f:
    line1 = f.readline()
    line2 = f.readline()
    print(f"  第1行: {line1!r}")
    print(f"  第2行: {line2!r}")
    # 剩下的行
    rest = f.read()
    print(f"  剩余: {rest!r}")


print("\n" + "=" * 60)
print("3. readlines() — 读取所有行到列表")
print("=" * 60)

with open(demo_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"  行列表: {lines}")
print(f"  行数: {len(lines)}")


print("\n" + "=" * 60)
print("4. for line in file — 最佳实践（惰性逐行读取）")
print("=" * 60)

with open(demo_file, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"  第{i}行: {line}", end="")


print("\n" + "=" * 60)
print("5. 大文件分块读取")
print("=" * 60)

# 模拟一个稍大的文件
big_file = os.path.join(os.path.dirname(__file__), "_demo_big.txt")
with open(big_file, "w", encoding="utf-8") as f:
    for i in range(10000):
        f.write(f"这是第 {i + 1} 行数据\n")

# 分块读取：每次读取固定字节
with open(big_file, "r", encoding="utf-8") as f:
    chunk_size = 500
    chunk_count = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        chunk_count += 1
        if chunk_count <= 3:
            print(f"  块{chunk_count} ({len(chunk)} 字符): {chunk[:60]}...")

print(f"  共读取 {chunk_count} 块（每块 {chunk_size} 字符）")


print("\n" + "=" * 60)
print("6. 文件打开模式速览")
print("=" * 60)

modes = [
    ("r", "只读（默认）"),
    ("w", "写入，覆盖已有"),
    ("a", "追加"),
    ("r+", "读写"),
    ("rb", "二进制只读"),
    ("wb", "二进制写入"),
]
for mode, desc in modes:
    print(f"  '{mode}' — {desc}")


# 清理临时文件
os.remove(demo_file)
os.remove(big_file)
