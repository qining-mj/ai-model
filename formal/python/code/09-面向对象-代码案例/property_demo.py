"""
@property 装饰器 — Property Decorator
演示 getter、setter、deleter、计算属性、验证。
"""

print("=" * 60)
print("1. 基本 @property — 只读属性")
print("=" * 60)


class Circle:
    def __init__(self, radius: float):
        self._radius = radius         # 用下划线表示"内部"属性

    @property
    def radius(self) -> float:
        """Radius getter (只读)"""
        return self._radius

    @property
    def area(self) -> float:
        """计算属性 — 没有 setter，只读"""
        return 3.14159 * self._radius ** 2

    @property
    def diameter(self) -> float:
        """计算属性"""
        return self._radius * 2


c = Circle(5)
print(f"  radius:   {c.radius}")
print(f"  diameter: {c.diameter:.2f}")
print(f"  area:     {c.area:.2f}")

# c.radius = 10  # 会报错: AttributeError，因为没有 setter


print("\n" + "=" * 60)
print("2. @property + @setter — 可读写属性 + 验证")
print("=" * 60)


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self._age = age

    @property
    def age(self) -> int:
        """Age getter"""
        return self._age

    @age.setter
    def age(self, value: int):
        """Age setter with validation"""
        if not isinstance(value, int):
            raise TypeError(f"年龄必须是整数，收到 {type(value).__name__}")
        if value < 0 or value > 150:
            raise ValueError(f"年龄必须在 0-150 之间，收到 {value}")
        print(f"  设置年龄: {value}")
        self._age = value

    @property
    def is_adult(self) -> bool:
        """计算属性"""
        return self._age >= 18


p = Person("Alice", 20)
print(f"  {p.name} 年龄: {p.age}，成年: {p.is_adult}")

p.age = 25
print(f"  更新后年龄: {p.age}")

try:
    p.age = -5
except ValueError as e:
    print(f"  验证捕获: {e}")

try:
    p.age = "abc"
except TypeError as e:
    print(f"  类型检查: {e}")


print("\n" + "=" * 60)
print("3. @deleter — 删除属性")
print("=" * 60)


class TempFile:
    def __init__(self, name: str):
        self._name = name
        self._content = ""

    @property
    def name(self) -> str:
        return self._name

    @name.deleter
    def name(self):
        print(f"  删除 name 属性并执行清理")
        self._name = None


t = TempFile("test.txt")
print(f"  文件名: {t.name}")
del t.name
print(f"  删除后: {t.name}")


print("\n" + "=" * 60)
print("4. 计算属性 — 依赖其他属性")
print("=" * 60)


class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    @property
    def area(self) -> float:
        """面积 = 宽 × 高"""
        return self.width * self.height

    @property
    def perimeter(self) -> float:
        """周长 = 2 × (宽 + 高)"""
        return 2 * (self.width + self.height)


rect = Rectangle(3, 4)
print(f"  矩形 3×4: 面积={rect.area}, 周长={rect.perimeter}")
rect.width = 5
print(f"  宽度改为 5: 面积={rect.area}, 周长={rect.perimeter}")


print("\n" + "=" * 60)
print("5. property 的另一种写法 — 使用 property() 函数")
print("=" * 60)


class Temperature:
    def __init__(self, celsius: float = 0):
        self._celsius = celsius

    def _get_fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    def _set_fahrenheit(self, value: float):
        self._celsius = (value - 32) * 5 / 9

    fahrenheit = property(_get_fahrenheit, _set_fahrenheit)

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        self._celsius = value


t = Temperature(100)
print(f"  100°C = {t.fahrenheit:.1f}°F")
t.fahrenheit = 212
print(f"  212°F = {t.celsius:.1f}°C")
