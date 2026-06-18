"""
高级 OOP 特性 — Advanced OOP
__slots__、__dict__、@dataclass、type() 动态创建类。
"""

import sys

print("=" * 60)
print("1. __slots__ — 节省内存")
print("=" * 60)


class PointNoSlots:
    """没有 __slots__ — 使用 __dict__"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class PointWithSlots:
    """有 __slots__ — 不使用 __dict__，固定属性"""
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# 内存比较
p1 = PointNoSlots(1, 2)
p2 = PointWithSlots(1, 2)

print(f"  PointNoSlots   大小: {sys.getsizeof(p1)} bytes")
print(f"  PointWithSlots 大小: {sys.getsizeof(p2)} bytes")
print(f"  PointNoSlots   有 __dict__: {hasattr(p1, '__dict__')}")
print(f"  PointWithSlots 有 __dict__: {hasattr(p2, '__dict__')}")

# __slots__ 禁止动态添加属性
try:
    p2.z = 3
except AttributeError as e:
    print(f"  无法添加新属性: {e}")


print("\n" + "=" * 60)
print("2. __dict__ 深入洞察")
print("=" * 60)


class Demo:
    class_var = "类变量"

    def __init__(self):
        self.inst_attr = "实例变量"
        self.value = 42


d = Demo()
print(f"  实例 __dict__: {d.__dict__}")
print(f"  类   __dict__ 键: {list(Demo.__dict__.keys())}")

# 修改 __dict__ 直接操作属性
d.__dict__["new_attr"] = "动态添加"
print(f"  通过 __dict__ 添加: d.new_attr = {d.new_attr}")


print("\n" + "=" * 60)
print("3. @dataclass — 自动生成 __init__、__repr__、__eq__")
print("=" * 60)

from dataclasses import dataclass, field


@dataclass(order=True)
class Student:
    """使用 @dataclass，自动生成 __init__、__repr__、__eq__、__lt__ 等"""
    name: str
    age: int
    grade: str = "A"
    scores: list = field(default_factory=list)


s1 = Student("Alice", 20, "A")
s2 = Student("Bob", 22, "B")
s3 = Student("Alice", 20, "A")

print(f"  s1          = {s1}")
print(f"  s1 == s3    = {s1 == s3}")          # 自动 __eq__
print(f"  s1 == s2    = {s1 == s2}")
print(f"  s1 < s2     = {s1 < s2}")           # order=True 时自动 __lt__

# 冻结（不可变）dataclass
@dataclass(frozen=True)
class Point:
    x: float
    y: float


p = Point(10, 20)
try:
    p.x = 30
except Exception as e:
    print(f"  冻结 dataclass 不可修改: {e}")


print("\n" + "=" * 60)
print("4. type() — 动态创建类")
print("=" * 60)


# type(name, bases, dict) 动态创建类
DynamicClass = type("DynamicClass", (object,), {
    "greeting": "Hello",
    "say_hello": lambda self: f"{self.greeting} from DynamicClass!",
})

obj = DynamicClass()
print(f"  类名: {type(obj).__name__}")
print(f"  方法调用: {obj.say_hello()}")

# 也可以动态添加方法
def new_method(self):
    return "这是动态添加的方法"

DynamicClass.new_method = new_method
obj2 = DynamicClass()
print(f"  {obj2.new_method()}")


print("\n" + "=" * 60)
print("5. @dataclass 高级功能 — field 与 __post_init__")
print("=" * 60)


@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0
    total_value: float = field(init=False)  # 不参与 __init__

    def __post_init__(self):
        """初始化后自动调用，用于计算派生字段"""
        self.total_value = self.price * self.quantity


prod = Product("笔记本", 2.5, 10)
print(f"  {prod.name}: 单价={prod.price}, 数量={prod.quantity}, 总价={prod.total_value}")
