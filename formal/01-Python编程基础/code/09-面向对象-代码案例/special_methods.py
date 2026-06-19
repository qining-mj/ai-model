"""
魔术方法 / 特殊方法 — Magic / Special Methods
演示 __str__、__repr__、__len__、__getitem__、__call__、__eq__、__add__ 等。
"""

print("=" * 60)
print("1. __str__ vs __repr__")
print("=" * 60)


class Book:
    def __init__(self, title: str, author: str, pages: int):
        self.title = title
        self.author = author
        self.pages = pages

    def __repr__(self) -> str:
        """开发者友好 — 通常可 eval()"""
        return f"Book('{self.title}', '{self.author}', {self.pages})"

    def __str__(self) -> str:
        """用户友好"""
        return f"《{self.title}》作者: {self.author}"


book = Book("Python 编程", "张三", 300)
print(f"  print:    {book}")
print(f"  __str__:  {str(book)}")
print(f"  __repr__: {repr(book)}")


print("\n" + "=" * 60)
print("2. __len__ — 自定义长度")
print("=" * 60)


class Playlist:
    def __init__(self, name: str):
        self.name = name
        self._songs = []

    def add(self, song: str):
        self._songs.append(song)

    def __len__(self) -> int:
        return len(self._songs)

    def __getitem__(self, index):
        return self._songs[index]


pl = Playlist("我的歌单")
pl.add("晴天")
pl.add("七里香")
pl.add("稻香")
print(f"  歌单长度: {len(pl)}")
print(f"  第2首歌: {pl[1]}")


print("\n" + "=" * 60)
print("3. __getitem__ / __setitem__ — 下标访问")
print("=" * 60)


class Vector:
    def __init__(self, *components):
        self._data = list(components)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __repr__(self):
        return f"Vector({', '.join(str(v) for v in self._data)})"


v = Vector(10, 20, 30, 40)
print(f"  v[0] = {v[0]}, v[1:3] = {v[1:3]}")
v[0] = 99
print(f"  修改后: {v}")


print("\n" + "=" * 60)
print("4. __call__ — 让对象可调用")
print("=" * 60)


class Multiplier:
    def __init__(self, factor: float):
        self.factor = factor

    def __call__(self, x: float) -> float:
        return x * self.factor


double = Multiplier(2)
triple = Multiplier(3)

print(f"  double(5) = {double(5)}")
print(f"  triple(5) = {triple(5)}")
print(f"  可调用? {callable(double)}")


print("\n" + "=" * 60)
print("5. __eq__ / __lt__ — 比较运算符")
print("=" * 60)


class Money:
    def __init__(self, amount: float, currency: str = "CNY"):
        self.amount = amount
        self.currency = currency

    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError(f"货币单位不同: {self.currency} vs {other.currency}")
        return self.amount == other.amount

    def __lt__(self, other) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError(f"货币单位不同: {self.currency} vs {other.currency}")
        return self.amount < other.amount

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"


m1 = Money(100)
m2 = Money(100)
m3 = Money(200)

print(f"  m1 == m2: {m1 == m2}")
print(f"  m1 == m3: {m1 == m3}")
print(f"  m1 <  m3: {m1 < m3}")


print("\n" + "=" * 60)
print("6. __add__ — 运算符重载")
print("=" * 60)


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        """p1 + p2"""
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        """p1 - p2"""
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


p1 = Point(1, 2)
p2 = Point(3, 4)
print(f"  {p1} + {p2} = {p1 + p2}")
print(f"  {p2} - {p1} = {p2 - p1}")
