"""
继承 — Inheritance
演示单继承、super()、方法重写、isinstance/issubclass、多重继承与 MRO。
"""

print("=" * 60)
print("1. 单继承 — 基础")
print("=" * 60)


class Animal:
    """基类"""

    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "..."  # 抽象意义不大，子类需重写

    def move(self) -> str:
        return f"{self.name} 在移动"


class Dog(Animal):
    """Dog 继承 Animal"""

    def __init__(self, name: str, breed: str):
        super().__init__(name)         # 调用父类 __init__
        self.breed = breed

    def speak(self) -> str:
        return "汪汪！"                 # 方法重写


class Cat(Animal):
    def speak(self) -> str:
        return "喵～"


dog = Dog("旺财", "金毛")
cat = Cat("咪咪")

print(f"  {dog.name} ({dog.breed}): {dog.speak()}, {dog.move()}")
print(f"  {cat.name}: {cat.speak()}, {cat.move()}")


print("\n" + "=" * 60)
print("2. isinstance / issubclass")
print("=" * 60)

print(f"  isinstance(dog, Dog)     = {isinstance(dog, Dog)}")
print(f"  isinstance(dog, Animal)  = {isinstance(dog, Animal)}")
print(f"  isinstance(dog, Cat)     = {isinstance(dog, Cat)}")
print(f"  issubclass(Dog, Animal)  = {issubclass(Dog, Animal)}")
print(f"  issubclass(Dog, Cat)     = {issubclass(Dog, Cat)}")
print(f"  issubclass(Animal, object) = {issubclass(Animal, object)}")


print("\n" + "=" * 60)
print("3. super() — 调用父类方法")
print("=" * 60)


class Printable:
    def __init__(self):
        print("  Printable.__init__")

    def info(self):
        return "[Printable]"


class Person(Printable):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        print(f"  Person.__init__({name})")

    @property
    def info(self):
        base = super().info()         # 调用父类方法
        return f"{base} Person: {self.name}"


p = Person("Alice")
print(f"  {p.info}")


print("\n" + "=" * 60)
print("4. 方法解析顺序 (MRO) — 多重继承")
print("=" * 60)


class A:
    def method(self):
        return "A"


class B(A):
    def method(self):
        return "B"


class C(A):
    def method(self):
        return "C"


class D(B, C):
    """D 继承自 B 和 C，MRO: D -> B -> C -> A"""
    pass


d = D()
print(f"  D().method() = {d.method()}")          # B (因为 B 在 C 前面)
print(f"  D.__mro__    = {[c.__name__ for c in D.__mro__]}")


print("\n" + "=" * 60)
print("5. 多重继承实战 — Mixin")
print("=" * 60)


class JsonMixin:
    """Mixin: 提供 to_json 方法"""

    def to_json(self):
        import json
        return json.dumps(self.__dict__, ensure_ascii=False)


class CsvMixin:
    """Mixin: 提供 to_csv 方法"""

    def to_csv(self):
        return ",".join(str(v) for v in self.__dict__.values())


class Product(JsonMixin, CsvMixin):
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


p = Product("笔记本电脑", 5999.0)
print(f"  to_json: {p.to_json()}")
print(f"  to_csv:  {p.to_csv()}")


print("\n" + "=" * 60)
print("6. 抽象基类 (abc)")
print("=" * 60)

from abc import ABC, abstractmethod


class Shape(ABC):
    """抽象基类 — 不能直接实例化"""

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass


class Square(Shape):
    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return self.side ** 2

    def perimeter(self) -> float:
        return 4 * self.side


# shape = Shape()            # TypeError!
sq = Square(4)
print(f"  正方形 4×4: 面积={sq.area}, 周长={sq.perimeter}")
