"""
文件指针操作 — File Pointer Operations
演示 tell()、seek()、truncate()。
"""

import os

data_file = os.path.join(os.path.dirname(__file__), "_demo_seek.txt")

# 准备测试文件
with open(data_file, "w", encoding="utf-8") as f:
    f.write("0123456789ABCDEFGHIJ")

print("=" * 60)
print("1. tell() — 查看当前文件指针位置")
print("=" * 60)

with open(data_file, "r", encoding="utf-8") as f:
    print(f"  打开后: tell() = {f.tell()}")
    data = f.read(5)
    print(f"  读取 5 字符: '{data}', tell() = {f.tell()}")
    data = f.read(5)
    print(f"  再读 5 字符: '{data}', tell() = {f.tell()}")


print("\n" + "=" * 60)
print("2. seek(offset, whence) — 移动文件指针")
print("=" * 60)

with open(data_file, "r", encoding="utf-8") as f:
    # whence=0: 从文件开头 (默认)
    f.seek(0)                         # 回到开头
    print(f"  seek(0): tell() = {f.tell()}, 字符 = '{f.read(1)}'")

    f.seek(5)                         # 跳到第 5 个字符
    print(f"  seek(5): tell() = {f.tell()}, 字符 = '{f.read(1)}'")

    # whence=1: 从当前位置
    f.seek(2, 1)                      # 当前位置 + 2
    print(f"  seek(2, 1): tell() = {f.tell()}, 字符 = '{f.read(1)}'")

    # whence=2: 从文件末尾
    f.seek(-3, 2)                     # 末尾往前 3
    print(f"  seek(-3, 2): tell() = {f.tell()}, 字符 = '{f.read(3)}'")


print("\n" + "=" * 60)
print("3. 使用 seek 重新读取部分内容")
print("=" * 60)

with open(data_file, "r", encoding="utf-8") as f:
    first_pass = f.read()
    print(f"  第一次读取: '{first_pass}'")

    f.seek(0)                         # 回到开头
    second_pass = f.read()
    print(f"  seek(0) 后重读: '{second_pass}'")


print("\n" + "=" * 60)
print("4. truncate() — 截断文件")
print("=" * 60)

# 先复制一份来测试截断
test_trunc = data_file.replace(".txt", "_trunc.txt")
with open(data_file, "r", encoding="utf-8") as src:
    with open(test_trunc, "w", encoding="utf-8") as dst:
        dst.write(src.read())

with open(test_trunc, "r+", encoding="utf-8") as f:
    print(f"  截断前文件大小: {os.path.getsize(test_trunc)} 字节")
    f.truncate(8)                     # 只保留前 8 个字符
    print(f"  截断到 8 字符后大小: {os.path.getsize(test_trunc)} 字节")
    f.seek(0)
    print(f"  文件内容: '{f.read()}'")


print("\n" + "=" * 60)
print("5. 读写模式 r+ 与 w+ 的区别")
print("=" * 60)

print("  'r+' — 读写，不会清空文件，需要先读或 seek")
print("  'w+' — 读写，会清空文件")
print("  'a+' — 读写追加，写入总是在末尾")

# 演示 r+
with open(data_file, "r+", encoding="utf-8") as f:
    f.seek(10)
    old = f.read(3)
    f.seek(10)
    f.write("XXX")
    f.seek(0)
    print(f"  r+ 修改后: '{f.read()}' (将 'ABC' 替换为 'XXX')")

# 演示 w+
with open(data_file.replace(".txt", "_wplus.txt"), "w+", encoding="utf-8") as f:
    f.write("全新内容")
    f.seek(0)
    print(f"  w+ 写入后: '{f.read()}'")


print("\n" + "=" * 60)
print("6. 二进制模式下 seek 的 whence 参数")
print("=" * 60)

with open(data_file, "rb") as f:
    f.seek(0, 2)                      # 移到末尾
    print(f"  文件末尾位置（大小）: {f.tell()}")

print("\n  注意: 文本模式下 ('r') seek 的返回值可能有差异；")
print("  二进制模式 ('rb') 下 seek/whence 行为更可预测。")


# 清理
os.remove(data_file)
if os.path.exists(test_trunc):
    os.remove(test_trunc)
wplus = data_file.replace(".txt", "_wplus.txt")
if os.path.exists(wplus):
    os.remove(wplus)
