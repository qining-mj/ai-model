"""
collections 模块
演示 namedtuple、deque、Counter、defaultdict、OrderedDict。
"""

from collections import namedtuple, deque, Counter, defaultdict, OrderedDict
import json

print("=" * 60)
print("1. namedtuple — 具名元组")
print("=" * 60)

# 定义
Point = namedtuple("Point", ["x", "y"])
Person = namedtuple("Person", "name age job")

p = Point(10, 20)
alice = Person("Alice", 28, "工程师")

print(f"  p             = {p}")
print(f"  p.x, p.y      = {p.x}, {p.y}")
print(f"  alice         = {alice}")
print(f"  alice.name    = {alice.name}")

# 拆包 & 转字典
x, y = p
print(f"  拆包: x={x}, y={y}")
print(f"  转字典: {p._asdict()}")
print(f"  替换: {p._replace(x=100)}")


print("\n" + "=" * 60)
print("2. deque — 双端队列（高效两端操作）")
print("=" * 60)

dq = deque()
dq.append("右1")
dq.append("右2")
dq.appendleft("左1")
dq.appendleft("左2")

print(f"  deque: {list(dq)}")
print(f"  pop 右侧: {dq.pop()}")
print(f"  popleft:  {dq.popleft()}")
print(f"  剩余: {list(dq)}")

# 旋转
dq2 = deque(range(1, 6))
print(f"  初始: {list(dq2)}")
dq2.rotate(2)                          # 右移 2
print(f"  rotate(2):  {list(dq2)}")
dq2.rotate(-3)                         # 左移 3
print(f"  rotate(-3): {list(dq2)}")

# 最大长度 (固定大小队列)
dq3 = deque(maxlen=3)
for i in range(5):
    dq3.append(i)
    print(f"  添加 {i}: {list(dq3)}")   # 超出时自动移除最左


print("\n" + "=" * 60)
print("3. Counter — 计数")
print("=" * 60)

words = ["apple", "banana", "apple", "cherry", "banana", "apple", "durian"]
counter = Counter(words)

print(f"  计数: {dict(counter)}")
print(f"  most_common(2): {counter.most_common(2)}")
print(f"  apple 出现: {counter['apple']} 次")

# 更新计数
counter.update(["apple", "banana"])
print(f"  update 后 apple: {counter['apple']}")

# 数学运算
c1 = Counter(a=3, b=1, c=0)
c2 = Counter(a=1, b=2, d=5)
print(f"  c1 + c2 = {dict(c1 + c2)}")
print(f"  c1 - c2 = {dict(c1 - c2)}")     # 只保留正数


print("\n" + "=" * 60)
print("4. defaultdict — 带默认值的字典")
print("=" * 60)

# list 作为默认值
groups = defaultdict(list)
data = [("水果", "苹果"), ("水果", "香蕉"), ("动物", "猫"), ("水果", "樱桃")]
for category, item in data:
    groups[category].append(item)

print(f"  defaultdict(list): {dict(groups)}")

# int 作为默认值（适用于计数）
counter2 = defaultdict(int)
sentence = "hello world hello python hello world"
for word in sentence.split():
    counter2[word] += 1
print(f"  defaultdict(int): {dict(counter2)}")

# 自定义默认值
default_value = defaultdict(lambda: "N/A")
default_value["name"] = "Alice"
print(f"  存在的键: {default_value['name']}")
print(f"  不存在的键: {default_value['age']}")


print("\n" + "=" * 60)
print("5. OrderedDict — 有序字典（Python 3.7+ 普通 dict 也有序，但语义不同）")
print("=" * 60)

od = OrderedDict()
od["z"] = 1
od["a"] = 2
od["m"] = 3

print(f"  OrderedDict: {dict(od)}")

# 移动到末尾
od.move_to_end("a")
print(f"  move_to_end('a'): {list(od.keys())}")

# 移动到开头
od.move_to_end("a", last=False)
print(f"  move_to_end('a', False): {list(od.keys())}")

# OrderedDict 在比较时考虑顺序
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
print(f"  OrderedDict 顺序不同 == 比较: {od1 == od2}")

d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
print(f"  普通 dict 顺序不同 == 比较: {d1 == d2}")


print("\n" + "=" * 60)
print("6. 使用场景总结")
print("=" * 60)

scenarios = [
    ("namedtuple", "轻量级不可变数据对象"),
    ("deque", "队列/栈/两端高效操作"),
    ("Counter", "计数/频率统计"),
    ("defaultdict", "分组/计数字典"),
    ("OrderedDict", "需要控制键顺序的场景"),
]
for name, desc in scenarios:
    print(f"  {name:15s}: {desc}")
