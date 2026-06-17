"""
断言 — assert 用法
演示 assert 基本用法、带消息断言、与异常的对比、-O 标志的影响。
"""

print("=" * 60)
print("1. assert 基本用法")
print("=" * 60)


def divide_positive(a: int, b: int) -> float:
    """只允许正数除法"""
    assert a > 0, f"a ({a}) 必须 > 0"
    assert b > 0, f"b ({b}) 必须 > 0"
    return a / b


print(f"  divide_positive(10, 2) = {divide_positive(10, 2)}")

try:
    divide_positive(10, -2)
except AssertionError as e:
    print(f"  AssertionError: {e}")


print("\n" + "=" * 60)
print("2. assert 带消息")
print("=" * 60)


def check_age(age: int):
    assert 0 <= age <= 150, f"年龄 {age} 超出合理范围 [0, 150]"
    print(f"  年龄 {age} 合法")


check_age(25)

try:
    check_age(200)
except AssertionError as e:
    print(f"  捕获断言错误: {e}")


print("\n" + "=" * 60)
print("3. assert vs 显式异常")
print("=" * 60)


# 使用 assert（开发时检查）
def safe_sqrt_assert(x: float) -> float:
    assert x >= 0, "不能对负数开平方"
    return x ** 0.5


# 使用显式异常（生产代码推荐）
def safe_sqrt_exception(x: float) -> float:
    if x < 0:
        raise ValueError(f"不能对负数 {x} 开平方")
    return x ** 0.5


print(f"  safe_sqrt_assert(9)      = {safe_sqrt_assert(9)}")
print(f"  safe_sqrt_exception(9)   = {safe_sqrt_exception(9)}")

# assert 可能被禁用（见下方），而 raise 始终生效
print("\n  【关键区别】assert 可能被 -O 标志禁用；raise 始终执行。")


print("\n" + "=" * 60)
print("4. -O 标志禁用 assert 的演示")
print("=" * 60)

print("  在命令行运行: python -O assert_demo.py")
print("  此时所有 assert 语句会被跳过。")
print("  验证: 使用 __debug__ 标志\n")


def test_assert_enabled():
    try:
        assert False, "assert 未禁用"
        return "assert 被禁用"
    except AssertionError:
        return "assert 被启用"


print(f"  __debug__ = {__debug__}")
print(f"  结果: {test_assert_enabled()}")
print("  （在 -O 模式下 __debug__ 为 False，assert 将被跳过）")


print("\n" + "=" * 60)
print("5. 正确的 assert 使用场景")
print("=" * 60)

print("  ✅ 好的场景:")
print("     - 内部不变量的检查")
print("     - 单元测试中的断言")
print("     - 开发期前置/后置条件检查")
print("")
print("  ❌ 不应使用 assert 的场景:")
print("     - 用户输入验证（用显式异常）")
print("     - 安全相关的检查（assert 可被禁用）")
print("     - 必须执行的逻辑（assert 可被禁用）")


print("\n" + "=" * 60)
print("6. assert 在数据验证中的实用示例")
print("=" * 60)


def process_data(data: list):
    """处理数据列表，使用 assert 检查前置条件"""
    assert isinstance(data, list), "data 必须是列表"
    assert len(data) > 0, "data 不能为空"
    assert all(isinstance(x, (int, float)) for x in data), "所有元素必须是数字"

    total = sum(data)
    avg = total / len(data)
    return {"sum": total, "avg": avg, "count": len(data)}


try:
    result = process_data([10, 20, 30])
    print(f"  process_data 结果: {result}")
except AssertionError as e:
    print(f"  断言失败: {e}")
