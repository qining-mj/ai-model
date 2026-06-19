"""
OS 与 Pathlib 操作 — OS and pathlib Operations
演示 os 模块与传统 os.path 操作，以及 pathlib.Path 等效方法。
"""

import os
import sys
from pathlib import Path

# 获取脚本所在目录
script_dir = os.path.dirname(__file__)

print("=" * 60)
print("1. 当前工作目录")
print("=" * 60)

cwd = os.getcwd()
print(f"  os.getcwd()  = {cwd}")

# 切换目录 (之后会切回来)
original_dir = os.getcwd()
os.chdir(script_dir)
print(f"  os.chdir() 切换到: {os.getcwd()}")
os.chdir(original_dir)
print(f"  已恢复: {os.getcwd()}")


print("\n" + "=" * 60)
print("2. 列出目录与创建目录")
print("=" * 60)

print(f"  当前目录内容 (前5项): {os.listdir('.')[:5]}")

# 创建单层目录
test_dir = os.path.join(script_dir, "_demo_testdir")
if not os.path.exists(test_dir):
    os.mkdir(test_dir)
    print(f"  创建目录: {test_dir}")

# 创建多层目录
nested = os.path.join(script_dir, "_demo_a", "_demo_b", "_demo_c")
if not os.path.exists(nested):
    os.makedirs(nested, exist_ok=True)
    print(f"  创建多层目录: {nested}")


print("\n" + "=" * 60)
print("3. 删除文件与目录")
print("=" * 60)

# 创建临时文件用于删除演示
tmp_file = os.path.join(script_dir, "_demo_tmp.txt")
with open(tmp_file, "w") as f:
    f.write("临时文件")
os.remove(tmp_file)
print(f"  删除文件: {tmp_file}")

# 清理上面创建的目录
if os.path.exists(nested):
    os.rmdir(nested)           # 只删除空目录
    os.chdir(script_dir)       # 避免被占用
    os.rmdir(os.path.join(script_dir, "_demo_a", "_demo_b"))
    os.rmdir(os.path.join(script_dir, "_demo_a"))
    print("  删除多层空目录完成")


print("\n" + "=" * 60)
print("4. os.path 函数")
print("=" * 60)

path = os.path.join(script_dir, "formatting.py")
print(f"  路径: {path}")
print(f"  os.path.exists    = {os.path.exists(path)}")
print(f"  os.path.isfile    = {os.path.isfile(path)}")
print(f"  os.path.isdir     = {os.path.isdir(path)}")
print(f"  os.path.basename  = {os.path.basename(path)}")
print(f"  os.path.dirname   = {os.path.dirname(path)}")
print(f"  os.path.getsize   = {os.path.getsize(path)} 字节")
print(f"  os.path.splitext  = {os.path.splitext(path)}")


print("\n" + "=" * 60)
print("5. pathlib.Path 等效操作（现代 Python 推荐）")
print("=" * 60)

p = Path(script_dir) / "formatting.py"
print(f"  Path: {p}")
print(f"  p.exists()        = {p.exists()}")
print(f"  p.is_file()       = {p.is_file()}")
print(f"  p.is_dir()        = {p.is_dir()}")
print(f"  p.name            = {p.name}")
print(f"  p.parent          = {p.parent}")
print(f"  p.stem            = {p.stem}")
print(f"  p.suffix          = {p.suffix}")
print(f"  p.stat().st_size  = {p.stat().st_size} 字节")

# pathlib 创建目录
tmp_path = Path(script_dir) / "_demo_pathlib_dir"
tmp_path.mkdir(exist_ok=True)
print(f"  使用 pathlib 创建目录: {tmp_path}")
tmp_path.rmdir()
print(f"  使用 pathlib 删除目录: {tmp_path}")

# pathlib 遍历
print(f"\n  当前目录 .py 文件:")
for py in Path(script_dir).glob("*.py"):
    print(f"    {py.name}")


print("\n" + "=" * 60)
print("6. 重命名")
print("=" * 60)

old = Path(script_dir) / "_demo_rename_old.txt"
new = Path(script_dir) / "_demo_rename_new.txt"

if not old.exists():
    old.write_text("重命名测试", encoding="utf-8")

os.rename(old, new)
print(f"  重命名: {old.name} -> {new.name}")
os.rename(new, old)
print(f"  重命名: {new.name} -> {old.name}")
os.remove(old)
print(f"  删除: {old.name}")
