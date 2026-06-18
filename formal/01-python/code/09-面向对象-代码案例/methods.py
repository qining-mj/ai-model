"""
实例方法 / 类方法 / 静态方法
演示 @classmethod、@staticmethod 以及各自的使用场景。
"""

print("=" * 60)
print("1. 实例方法 — 操作实例数据")
print("=" * 60)


class Student:
    school = "北京大学"

    def __init__(self, name: str, score: float):
        self.name = name
        self.score = score

    def get_grade(self) -> str:
        """实例方法：基于实例的 score 计算等级"""
        if self.score >= 90:
            return "A"
        elif self.score >= 80:
            return "B"
        elif self.score >= 70:
            return "C"
        elif self.score >= 60:
            return "D"
        return "F"

    def __repr__(self):
        return f"Student({self.name}, {self.score})"


s = Student("Alice", 85)
print(f"  {s.name} 的等级: {s.get_grade()}")


print("\n" + "=" * 60)
print("2. @classmethod — 操作类数据/工厂方法")
print("=" * 60)


class StudentDB:
    students = []

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def add_student(cls, name: str, score: float):
        """类方法：通过类来管理所有学生"""
        student = Student(name, score)
        cls.students.append(student)
        print(f"  添加: {student}")

    @classmethod
    def average_score(cls) -> float:
        """类方法：计算所有学生的平均分"""
        if not cls.students:
            return 0.0
        return sum(s.score for s in cls.students) / len(cls.students)

    @classmethod
    def from_csv_line(cls, csv_line: str):
        """类方法：工厂方法，从 CSV 行创建实例"""
        name, score = csv_line.strip().split(",")
        return cls.add_student(name, float(score))


StudentDB.add_student("Bob", 92)
StudentDB.add_student("Charlie", 78)
StudentDB.add_student("Diana", 88)
print(f"  平均分: {StudentDB.average_score():.1f}")


print("\n" + "=" * 60)
print("3. @staticmethod — 工具方法，与类/实例无关")
print("=" * 60)


class MathUtils:
    """数学工具集合"""

    @staticmethod
    def is_even(n: int) -> bool:
        return n % 2 == 0

    @staticmethod
    def clamp(value: float, low: float, high: float) -> float:
        return max(low, min(value, high))

    @staticmethod
    def grade_description(grade: str) -> str:
        descriptions = {
            "A": "优秀",
            "B": "良好",
            "C": "中等",
            "D": "及格",
            "F": "不及格",
        }
        return descriptions.get(grade.upper(), "未知等级")


print(f"  7 是偶数? {MathUtils.is_even(7)}")
print(f"  clamp(150, 0, 100) = {MathUtils.clamp(150, 0, 100)}")
print(f"  等级 A 的含义: {MathUtils.grade_description('A')}")


print("\n" + "=" * 60)
print("4. 三种方法的对比")
print("=" * 60)

print(f"  {'方法':<20} {'第一个参数':<15} {'访问实例':<10} {'访问类':<10}")
print(f"  {'-'*20} {'-'*15} {'-'*10} {'-'*10}")
print(f"  {'实例方法':<20} {'self (实例)':<15} {'是':<10} {'是'}")
print(f"  {'类方法':<20} {'cls (类)':<15} {'否':<10} {'是'}")
print(f"  {'静态方法':<20} {'无':<15} {'否':<10} {'否'}")


print("\n" + "=" * 60)
print("5. 何时使用哪种方法？")
print("=" * 60)

print("  实例方法: 需要访问实例属性（name, score 等）")
print("  类方法:  需要访问类属性/类状态，或实现工厂方法")
print("  静态方法: 功能与类相关，但不需要访问类或实例数据")


print("\n" + "=" * 60)
print("6. 静态方法的替代 — 模块级函数")
print("=" * 60)

print("  Python 中静态方法常可替换为模块级函数，")
print("  放在类中主要是为了命名空间组织。")
