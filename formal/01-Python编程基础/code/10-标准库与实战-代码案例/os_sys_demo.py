"""
OS / Sys / Platform 模块
演示 os.environ、sys.argv、sys.exit、platform 等。
"""

import os
import sys
import platform

print("=" * 60)
print("1. os 模块 — 操作系统接口")
print("=" * 60)

print(f"  os.name:               {os.name}")           # 'nt' (Windows) / 'posix' (Linux/macOS)
print(f"  当前工作目录:          {os.getcwd()}")

# 环境变量
print(f"  PATH 环境变量 (前100字符): {os.environ.get('PATH', 'N/A')[:100]}...")
print(f"  USERNAME:               {os.environ.get('USERNAME', 'N/A')}")
print(f"  os.getenv('HOME'):      {os.getenv('HOME', 'N/A')}")


print("\n" + "=" * 60)
print("2. sys 模块 — Python 运行时")
print("=" * 60)

print(f"  sys.platform:          {sys.platform}")      # win32 / linux / darwin
print(f"  sys.version:           {sys.version.split()[0]}")
print(f"  sys.maxsize:           {sys.maxsize:,}")      # 最大整数
print(f"  sys.executable:        {sys.executable}")
print(f"  sys.argv (本脚本):     {sys.argv}")

# sys.argv 演示
print(f"  sys.argv 长度:          {len(sys.argv)}")
if len(sys.argv) > 1:
    print(f"  第一个参数:             {sys.argv[1]}")


print("\n" + "=" * 60)
print("3. sys.exit() — 退出程序")
print("=" * 60)

print("  sys.exit(0)  正常退出")
print("  sys.exit(1)  异常退出")
print("  （本示例跳过实际 exit 以避免终止脚本）")
# sys.exit(0)

# 在 except 中使用 sys.exit
try:
    # sys.exit("错误信息")  # 会抛出 SystemExit
    pass
except SystemExit as e:
    print(f"  捕获 SystemExit: {e}")


print("\n" + "=" * 60)
print("4. platform 模块 — 详细系统信息")
print("=" * 60)

print(f"  platform.system():      {platform.system()}")
print(f"  platform.release():     {platform.release()}")
print(f"  platform.version():     {platform.version()[:50]}...")
print(f"  platform.machine():     {platform.machine()}")
print(f"  platform.processor():   {platform.processor()}")
print(f"  platform.python_version(): {platform.python_version()}")
print(f"  platform.node():        {platform.node()}")


print("\n" + "=" * 60)
print("5. os.path 跨平台路径操作")
print("=" * 60)

path = os.path.join("folder", "sub", "file.txt")
print(f"  os.path.join:           {path}")
print(f"  os.path.abspath:        {os.path.abspath(path)}")
print(f"  os.path.normpath:       {os.path.normpath('a/b/../c/./d')}")


print("\n" + "=" * 60)
print("6. 跨平台差异总结")
print("=" * 60)

print(f"  Windows 路径分隔符: \\")
print(f"  Linux/macOS 路径分隔符: /")
print(f"  os.sep = {os.sep!r}")
print(f"  os.linesep = {os.linesep!r}")
print(f"  os.pathsep = {os.pathsep!r}")


print("\n" + "=" * 60)
print("7. 临时使用环境变量")
print("=" * 60)

# 临时修改（仅在当前进程内有效）
original = os.environ.get("MY_VAR", "(未设置)")
print(f"  修改前 MY_VAR: {original}")

os.environ["MY_VAR"] = "临时值"
print(f"  修改后 MY_VAR: {os.environ['MY_VAR']}")

del os.environ["MY_VAR"]
print(f"  删除后 MY_VAR: {os.environ.get('MY_VAR', '(未设置)')}")
