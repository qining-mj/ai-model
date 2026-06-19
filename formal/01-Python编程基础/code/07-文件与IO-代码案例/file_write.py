"""
文件写入 — Writing Files
演示 write()、writelines()、flush()、追加模式、with 语句。
"""

import os

output_file = os.path.join(os.path.dirname(__file__), "_demo_output.txt")

print("=" * 60)
print("1. write() — 写入字符串")
print("=" * 60)

with open(output_file, "w", encoding="utf-8") as f:
    f.write("第一行文本\n")
    f.write("第二行文本\n")
    f.write("第三行: 含有中文\n")

print("  已写入 3 行")


print("\n" + "=" * 60)
print("2. writelines() — 写入字符串列表")
print("=" * 60)

lines = [
    "第四行: writelines 示例\n",
    "第五行: 不会自动加换行符\n",
    "第六行: 需要自己在字符串中加 \\n\n",
]

with open(output_file, "a", encoding="utf-8") as f:
    f.writelines(lines)

print("  已追加 3 行（使用 writelines）")

# 验证写入结果
with open(output_file, "r", encoding="utf-8") as f:
    print(f"  文件现有 {len(f.readlines())} 行")


print("\n" + "=" * 60)
print("3. 追加模式 'a'")
print("=" * 60)

with open(output_file, "a", encoding="utf-8") as f:
    f.write("第七行: 追加写入\n")

with open(output_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"  追加后共 {len(lines)} 行")
print(f"  最后一行: {lines[-1]!r}")


print("\n" + "=" * 60)
print("4. with 语句 — 自动关闭文件")
print("=" * 60)

print("  with open(...) as f: ... 结束后文件自动关闭")
# 显式验证
f = open(output_file, "r", encoding="utf-8")
print(f"  文件打开: {not f.closed}")
f.close()
print(f"  文件关闭: {f.closed}")


print("\n" + "=" * 60)
print("5. 覆盖写入 'w' 模式")
print("=" * 60)

with open(output_file, "w", encoding="utf-8") as f:
    f.write("原内容被完全覆盖\n")
    f.write("只有这两行\n")

with open(output_file, "r", encoding="utf-8") as f:
    print(f"  覆盖后内容: {f.readlines()}")


print("\n" + "=" * 60)
print("6. flush() — 强制将缓冲区写入磁盘")
print("=" * 60)

with open(output_file, "a", encoding="utf-8") as f:
    f.write("这行立即写入\n")
    f.flush()                          # 强制刷盘
    print("  flush() 后数据已写入磁盘（即使 with 块未结束）")


print("\n" + "=" * 60)
print("7. 二进制写入模式 'wb'")
print("=" * 60)

with open(output_file.replace(".txt", ".bin"), "wb") as f:
    f.write(b"\x00\x01\x02\x03 binary data")
    f.write("中文编码".encode("utf-8"))

print("  二进制文件写入完成")


# 清理
os.remove(output_file)
bin_file = output_file.replace(".txt", ".bin")
if os.path.exists(bin_file):
    os.remove(bin_file)
