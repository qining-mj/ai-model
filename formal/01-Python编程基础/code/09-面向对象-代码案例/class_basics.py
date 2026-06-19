"""
类定义基础 — Class Definition
演示 class、__init__、self、实例属性、类变量与实例变量的区别。
"""

print("=" * 60)
print("1. 定义一个简单的类")
print("=" * 60)


class Student:
    """表示一个学生"""

    # 类变量 — 所有实例共享
    school = "北京大学"
    student_count = 0

    def __init__(self, name: str, age: int, grade: str):
        """初始化方法（构造器）"""
        self.name = name              # 实例属性
        self.age = age
        self.grade = grade
        Student.student_count += 1    # 修改类变量


# 创建实例
s1 = Student("Alice", 20, "A")
s2 = Student("Bob", 22, "B")

print(f"  s1.name = {s1.name}, s1.age = {s1.age}, s1.grade = {s1.grade}")
print(f"  s2.name = {s2.name}, s2.age = {s2.age}, s2.grade = {s2.grade}")


print("\n" + "=" * 60)
print("2. 类变量 vs 实例变量")
print("=" * 60)

print(f"  Student.school = {Student.school}")
print(f"  s1.school      = {s1.school}")
print(f"  s2.school      = {s2.school}")

# 通过实例修改类变量 — 实际上创建了实例属性
s1.school = "清华大学"
print(f"\n  执行 s1.school = '清华大学' 后:")
print(f"  Student.school = {Student.school}")     # 未变
print(f"  s1.school      = {s1.school}")            # 变了（实例属性遮蔽）
print(f"  s2.school      = {s2.school}")            # 未变

# 真正修改类变量
Student.school = "浙江大学"
print(f"\n  执行 Student.school = '浙江大学' 后:")
print(f"  Student.school = {Student.school}")
print(f"  s1.school      = {s1.school}")            # 实例属性优先
print(f"  s2.school      = {s2.school}")            # 跟随类变量


print("\n" + "=" * 60)
print("3. 类变量：计数器")
print("=" * 60)

print(f"  学生总数: {Student.student_count}")


print("\n" + "=" * 60)
print("4. self 的本质")
print("=" * 60)

print("  self 就是实例对象本身")
s3 = Student("Charlie", 21, "A")
print(f"  id(s3) == id(self) 在 __init__ 中指向同一对象")


print("\n" + "=" * 60)
print("5. 动态添加属性")
print("=" * 60)

s3.email = "charlie@example.com"      # 动态添加
print(f"  s3.email = {s3.email}")

# 但其他实例没有
if not hasattr(s2, "email"):
    print("  s2 没有 email 属性")


print("\n" + "=" * 60)
print("6. 检查属性: hasattr / getattr / setattr")
print("=" * 60)

print(f"  hasattr(s1, 'name')  = {hasattr(s1, 'name')}")
print(f"  getattr(s1, 'name', '默认')   = {getattr(s1, 'name', '默认')}")
print(f"  getattr(s1, 'email', '默认')  = {getattr(s1, 'email', '默认')}")

setattr(s1, "nickname", "Ali")
print(f"  s1.nickname = {s1.nickname}")


print("\n" + "=" * 60)
print("7. __dict__ — 查看实例/类的属性字典")
print("=" * 60)

print(f"  s1.__dict__   = {s1.__dict__}")
print(f"  s2.__dict__   = {s2.__dict__}")
print(f"  Student.__dict__ 的键: {list(Student.__dict__.keys())}")
