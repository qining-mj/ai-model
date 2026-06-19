"""
raise 与自定义异常 — raise and Custom Exceptions
演示 raise ValueError、bare raise、异常链、自定义异常类。
"""

print("=" * 60)
print("1. 主动抛出异常")
print("=" * 60)


def set_age(age: int):
    if age < 0 or age > 150:
        raise ValueError(f"年龄必须在 0-150 之间，收到: {age}")
    print(f"  年龄设置为: {age}")


try:
    set_age(-5)
except ValueError as e:
    print(f"  捕获: {e}")

set_age(25)


print("\n" + "=" * 60)
print("2. bare raise — 重新抛出当前异常")
print("=" * 60)


def process_with_cleanup(data):
    try:
        result = 100 / data
        return result
    except:
        print("  执行清理操作...")
        raise                              # 重新抛出, 保留原始 traceback


try:
    process_with_cleanup(0)
except ZeroDivisionError:
    print("  上层捕获到重新抛出的异常")


print("\n" + "=" * 60)
print("3. 异常链 — raise … from …")
print("=" * 60)


def load_config(filepath):
    try:
        with open(filepath) as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"无法加载配置文件: {filepath}") from e


try:
    load_config("_不存在_的文件_.txt")
except RuntimeError as e:
    print(f"  RuntimeError: {e}")
    print(f"  原始异常: {e.__cause__}")


print("\n" + "=" * 60)
print("4. raise … from None — 隐藏异常链")
print("=" * 60)


def safe_load(filepath):
    try:
        with open(filepath) as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError("文件未找到") from None


try:
    safe_load("_不存在的.txt")
except ValueError as e:
    print(f"  ValueError (没有原始异常信息): {e}")
    print(f"  __cause__ 为 None: {e.__cause__}")


print("\n" + "=" * 60)
print("5. 自定义异常类")
print("=" * 60)


class InsufficientBalanceError(Exception):
    """账户余额不足时抛出的异常"""

    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        self.shortfall = amount - balance
        super().__init__(
            f"余额不足: 需要 {amount:.2f}, "
            f"可用 {balance:.2f}, "
            f"短缺 {self.shortfall:.2f}"
        )


class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount: float):
        if amount > self.balance:
            raise InsufficientBalanceError(self.balance, amount)
        self.balance -= amount
        print(f"  提现 {amount:.2f} 成功，余额: {self.balance:.2f}")


acc = BankAccount("Alice", 100)

try:
    acc.withdraw(200)
except InsufficientBalanceError as e:
    print(f"  自定义异常: {e}")
    print(f"  短缺金额: {e.shortfall:.2f}")


print("\n" + "=" * 60)
print("6. 检查异常类型: isinstance")
print("=" * 60)

try:
    raise InsufficientBalanceError(50, 100)
except Exception as e:
    if isinstance(e, InsufficientBalanceError):
        print(f"  这是一个 InsufficientBalanceError")
    if isinstance(e, (ValueError, TypeError)):
        print(f"  也是 ValueError 或 TypeError")
