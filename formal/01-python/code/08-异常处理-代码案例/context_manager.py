"""
上下文管理器 — with 语句 + contextlib
演示基于类与基于函数的上下文管理器、嵌套 with。
"""

import contextlib
import os

print("=" * 60)
print("1. 基于类的上下文管理器 (__enter__ / __exit__)")
print("=" * 60)


class ManagedFile:
    """一个简单的上下文管理器，用于文件操作"""

    def __init__(self, filename: str, mode: str = "r"):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"  [__enter__] 打开文件: {self.filename}")
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file              # as 子句接收的值

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  [__exit__]  关闭文件: {self.filename}")
        if self.file:
            self.file.close()
        # 返回 False 表示不抑制异常，True 表示抑制
        if exc_type is not None:
            print(f"     异常信息: {exc_type.__name__}: {exc_val}")
        return False                   # 不抑制异常


tmp_file = os.path.join(os.path.dirname(__file__), "_demo_cm.txt")
with open(tmp_file, "w", encoding="utf-8") as f:
    f.write("Hello, Context Manager!\n")

with ManagedFile(tmp_file, "r") as f:
    content = f.read()
    print(f"  文件内容: {content!r}")

print("  with 块外: 文件已自动关闭")

# 异常时 __exit__ 也会被调用
try:
    with ManagedFile(tmp_file, "r") as f:
        data = f.read()
        raise ValueError("故意出错")
except ValueError:
    print("  异常被上层捕获")


print("\n" + "=" * 60)
print("2. 基于 @contextmanager 装饰器（函数式）")
print("=" * 60)


@contextlib.contextmanager
def managed_file(filename: str, mode: str = "r"):
    """使用 contextmanager 装饰器的上下文管理器"""
    print(f"  [进入] 打开 {filename}")
    file = open(filename, mode, encoding="utf-8")
    try:
        yield file                    # 产出给 with 块使用
    finally:
        print(f"  [退出] 关闭 {filename}")
        file.close()


with managed_file(tmp_file, "r") as f:
    print(f"  内容: {f.read()!r}")


print("\n" + "=" * 60)
print("3. 上下文管理器用于其他资源（计时器示例）")
print("=" * 60)

import time


@contextlib.contextmanager
def timer(label: str = "耗时"):
    """测量代码块执行时间"""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"  [{label}] {elapsed:.4f} 秒")


with timer("睡眠测试"):
    time.sleep(0.1)


print("\n" + "=" * 60)
print("4. 嵌套 with 语句")
print("=" * 60)

# 传统嵌套
with managed_file(tmp_file, "r") as src:
    with managed_file(tmp_file.replace(".txt", "_copy.txt"), "w") as dst:
        dst.write(src.read())

print("  文件复制完成（嵌套 with）")

# Python 3.10+ 括号内多个上下文
with (
    open(tmp_file, "r", encoding="utf-8") as f1,
    open(tmp_file.replace(".txt", "_copy2.txt"), "w", encoding="utf-8") as f2,
):
    f2.write(f1.read())

print("  文件复制完成（多上下文 with）")


print("\n" + "=" * 60)
print("5. contextlib.suppress — 忽略特定异常")
print("=" * 60)

from contextlib import suppress

# 传统方式
try:
    os.remove("_不存在的文件.txt")
except FileNotFoundError:
    pass

# suppress 方式
with suppress(FileNotFoundError):
    os.remove("_不存在的文件.txt")

print("  FileNotFoundError 被 suppress 忽略")


# 清理
os.remove(tmp_file)
copy1 = tmp_file.replace(".txt", "_copy.txt")
copy2 = tmp_file.replace(".txt", "_copy2.txt")
for f in [copy1, copy2]:
    if os.path.exists(f):
        os.remove(f)
