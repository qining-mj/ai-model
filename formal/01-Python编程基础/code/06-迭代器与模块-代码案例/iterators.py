"""
迭代器协议 — Iterator Protocol
演示 iter()、next()、StopIteration 以及自定义迭代器类。
"""

print("=" * 60)
print("1. 内置可迭代对象：iter() 和 next()")
print("=" * 60)

my_list = [10, 20, 30]
it = iter(my_list)                # 获取迭代器

print(next(it))                    # 10
print(next(it))                    # 20
print(next(it))                    # 30
# print(next(it))                  # 如果取消注释：StopIteration 异常


print("\n" + "=" * 60)
print("2. for 循环背后的工作原理")
print("=" * 60)

for item in my_list:
    print(f"  {item}")

# 上面的 for 等价于：
print("  --- 等价于 ---")
_iter = iter(my_list)
while True:
    try:
        val = next(_iter)
        print(f"  {val} (模拟 for)")
    except StopIteration:
        break


print("\n" + "=" * 60)
print("3. 自定义迭代器类")
print("=" * 60)


class CountDown:
    """倒计时迭代器：从 N 递减到 1"""

    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        """返回迭代器对象本身"""
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration          # 终止信号
        value = self.current
        self.current -= 1
        return value


for num in CountDown(5):
    print(f"  CountDown: {num}")


print("\n" + "=" * 60)
print("4. 可迭代对象与迭代器分离")
print("=" * 60)


class MyRange:
    """一个可迭代对象，每次返回新的迭代器"""

    def __init__(self, n: int):
        self.n = n

    def __iter__(self):
        return MyRangeIterator(self.n)


class MyRangeIterator:
    """实际的迭代器"""

    def __init__(self, n: int):
        self.i = 0
        self.n = n

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        val = self.i
        self.i += 1
        return val


r = MyRange(3)
for x in r:
    print(f"  MyRange: {x}")

print(f"  list(r) == {list(r)}")       # 可以重复迭代，因为每次都创建新迭代器


print("\n" + "=" * 60)
print("5. iter() 的第二个参数：可调用对象 + 哨兵值")
print("=" * 60)


def counter():
    i = 0
    while True:
        i += 1
        return i


# iter(callable, sentinel) 持续调用 callable 直到返回 sentinel
it2 = iter(lambda: int(input("  输入数字（0 停止）: ")), 0)
# 本示例仅演示概念，下一行被注释以避免阻塞
# for val in it2:
#     print(f"  你输入了: {val}")
print("  iter(callable, sentinel) 可一直读取直到遇到哨兵值")

print("\n" + "=" * 60)
print("6. 迭代器是一次性的")
print("=" * 60)

nums = [1, 2, 3]
it3 = iter(nums)
print(f"  list(it3) = {list(it3)}")
print(f"  list(it3) = {list(it3)}")   # 第二次为空，因为迭代器已耗尽
