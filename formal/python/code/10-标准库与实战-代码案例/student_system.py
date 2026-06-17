#!/usr/bin/env python3
"""
学生信息管理系统 — Student Information Management System
======================================================

集成功能:
  - Student 数据类 (name, student_id, age, grade, major, email, phone)
  - JSON 文件持久化 (自动保存/加载)
  - 正则表达式输入校验 (学号、邮箱、电话)
  - 全面的异常处理
  - 命令行菜单界面 (增/删/查/改/列表/统计/退出)
  - collections 模块应用 (defaultdict 成绩统计)

课程: Python3 标准库与实战
"""

import json
import re
import os
from dataclasses import dataclass, field
from typing import Optional
from collections import defaultdict


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------

@dataclass
class Student:
    """学生数据模型

    Attributes:
        name:       学生姓名
        student_id: 学号 (格式: STU-XXXXX, X 为数字)
        age:        年龄 (18-60)
        grade:      年级 (大一/大二/大三/大四/研一/研二/研三)
        major:      专业
        email:      邮箱
        phone:      手机号 (11 位数字)
    """
    name: str
    student_id: str
    age: int
    grade: str
    major: str
    email: str = ""
    phone: str = ""

    def to_dict(self) -> dict:
        """转换为字典 (用于 JSON 序列化)"""
        return {
            "name": self.name,
            "student_id": self.student_id,
            "age": self.age,
            "grade": self.grade,
            "major": self.major,
            "email": self.email,
            "phone": self.phone,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """从字典创建 Student 实例"""
        return cls(**data)


# ---------------------------------------------------------------------------
# 校验工具
# ---------------------------------------------------------------------------

def validate_student_id(sid: str) -> bool:
    """校验学号格式: STU- 后跟 5 位数字"""
    return bool(re.fullmatch(r"STU-\d{5}", sid))


def validate_email(email: str) -> bool:
    """校验邮箱格式 (简单校验)"""
    return bool(re.fullmatch(r"[\w.]+@[\w.]+\.\w+", email))


def validate_phone(phone: str) -> bool:
    """校验手机号: 11 位数字"""
    return bool(re.fullmatch(r"1[3-9]\d{9}", phone))


# ---------------------------------------------------------------------------
# 持久化
# ---------------------------------------------------------------------------

DATA_FILE = os.path.join(os.path.dirname(__file__), "_students.json")


def save_students(students: list[Student]) -> None:
    """将学生列表保存到 JSON 文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in students], f,
                  ensure_ascii=False, indent=2)


def load_students() -> list[Student]:
    """从 JSON 文件加载学生列表，文件不存在时返回空列表"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data_list = json.load(f)
        return [Student.from_dict(d) for d in data_list]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"  [!] 数据文件损坏，将重新创建: {e}")
        return []


# ---------------------------------------------------------------------------
# 管理系统核心类
# ---------------------------------------------------------------------------

class StudentSystem:
    """学生信息管理系统"""

    VALID_GRADES = {"大一", "大二", "大三", "大四", "研一", "研二", "研三"}

    def __init__(self):
        self._students = load_students()

    # ---- CRUD 操作 ----

    def add_student(self, s: Student) -> None:
        """添加学生，检查学号唯一性"""
        if any(stu.student_id == s.student_id for stu in self._students):
            raise ValueError(f"学号 {s.student_id} 已存在")
        self._students.append(s)
        save_students(self._students)
        print(f"  [+] 学生 {s.name} 添加成功")

    def remove_student(self, student_id: str) -> Student:
        """按学号删除学生，返回被删除的学生"""
        for i, stu in enumerate(self._students):
            if stu.student_id == student_id:
                removed = self._students.pop(i)
                save_students(self._students)
                print(f"  [-] 学生 {removed.name} 已删除")
                return removed
        raise KeyError(f"未找到学号为 {student_id} 的学生")

    def update_student(self, student_id: str, **kwargs) -> Student:
        """更新学生信息，返回更新后的学生"""
        for stu in self._students:
            if stu.student_id == student_id:
                for key, value in kwargs.items():
                    if hasattr(stu, key) and value is not None:
                        setattr(stu, key, value)
                save_students(self._students)
                print(f"  [*] 学生 {stu.name} 信息已更新")
                return stu
        raise KeyError(f"未找到学号为 {student_id} 的学生")

    def search_student(self, keyword: str) -> list[Student]:
        """按姓名或学号搜索学生（模糊匹配）"""
        keyword = keyword.lower()
        results = []
        for stu in self._students:
            if keyword in stu.name.lower() or keyword in stu.student_id.lower():
                results.append(stu)
        return results

    def list_students(self) -> list[Student]:
        """返回所有学生列表"""
        return self._students

    def get_grade_statistics(self) -> dict:
        """使用 defaultdict 按年级统计学生人数"""
        stats = defaultdict(int)
        for stu in self._students:
            stats[stu.grade] += 1
        return dict(stats)

    def get_major_statistics(self) -> dict:
        """使用 defaultdict 按专业统计学生人数"""
        stats = defaultdict(int)
        for stu in self._students:
            stats[stu.major] += 1
        return dict(stats)

    # ---- 输入辅助 ----

    @staticmethod
    def input_student_info() -> Student:
        """交互式输入学生信息，带校验"""
        name = input("    姓名: ").strip()
        if not name:
            raise ValueError("姓名不能为空")

        sid = input("    学号 (格式 STU-XXXXX): ").strip()
        if not validate_student_id(sid):
            raise ValueError("学号格式无效，应为 STU- followed by 5 digits")

        age_str = input("    年龄 (18-60): ").strip()
        try:
            age = int(age_str)
        except ValueError:
            raise ValueError("年龄必须是整数")
        if age < 18 or age > 60:
            raise ValueError("年龄必须在 18-60 之间")

        grade = input(f"    年级 ({'/'.join(StudentSystem.VALID_GRADES)}): ").strip()
        if grade not in StudentSystem.VALID_GRADES:
            raise ValueError(f"无效年级，可选: {', '.join(StudentSystem.VALID_GRADES)}")

        major = input("    专业: ").strip()
        if not major:
            raise ValueError("专业不能为空")

        email = input("    邮箱 (可选): ").strip()
        if email and not validate_email(email):
            raise ValueError("邮箱格式无效")

        phone = input("    电话 (可选, 11位数字): ").strip()
        if phone and not validate_phone(phone):
            raise ValueError("电话格式无效，应为 11 位数字")

        return Student(name=name, student_id=sid, age=age,
                       grade=grade, major=major, email=email, phone=phone)


# ---------------------------------------------------------------------------
# 菜单界面
# ---------------------------------------------------------------------------

def display_student(stu: Student) -> None:
    """打印单个学生信息"""
    print(f"    {stu.student_id} | {stu.name:<8} | {stu.age:2d}岁 | "
          f"{stu.grade:<4} | {stu.major:<10} | {stu.email:<20} | {stu.phone}")


def display_students(students: list[Student]) -> None:
    """打印学生列表"""
    if not students:
        print("    (空)")
        return
    print(f"    {'学号':<10} {'姓名':<8} {'年龄':<4} {'年级':<6} "
          f"{'专业':<12} {'邮箱':<22} {'电话'}")
    print("    " + "-" * 80)
    for stu in students:
        display_student(stu)
    print(f"    --- 共 {len(students)} 人 ---")


def run_menu() -> None:
    """运行主菜单"""
    system = StudentSystem()

    menu = {
        "1": ("添加学生", lambda: _add_student(system)),
        "2": ("删除学生", lambda: _remove_student(system)),
        "3": ("搜索学生", lambda: _search_student(system)),
        "4": ("修改学生", lambda: _update_student(system)),
        "5": ("列出全部", lambda: _list_all(system)),
        "6": ("统计信息", lambda: _show_stats(system)),
        "7": ("退出系统", lambda: _exit_system(system)),
    }

    while True:
        print("\n" + "=" * 50)
        print("  学生信息管理系统")
        print("=" * 50)
        for key, (desc, _) in menu.items():
            print(f"    {key}. {desc}")
        print("-" * 50)

        choice = input("  请选择操作: ").strip()
        print()

        if choice in menu:
            try:
                menu[choice][1]()
            except (ValueError, KeyError) as e:
                print(f"  [!] {e}")
            except Exception as e:
                print(f"  [!] 发生未预料的错误: {e}")
        else:
            print("  [!] 无效选择，请重新输入")


# ---- 菜单函数 ----

def _add_student(system: StudentSystem) -> None:
    """添加学生菜单项"""
    print("  --- 添加学生 ---")
    stu = system.input_student_info()
    system.add_student(stu)


def _remove_student(system: StudentSystem) -> None:
    """删除学生菜单项"""
    print("  --- 删除学生 ---")
    sid = input("    请输入要删除的学号: ").strip()
    system.remove_student(sid)


def _search_student(system: StudentSystem) -> None:
    """搜索学生菜单项"""
    print("  --- 搜索学生 ---")
    keyword = input("    请输入姓名或学号关键字: ").strip()
    results = system.search_student(keyword)
    display_students(results)


def _update_student(system: StudentSystem) -> None:
    """修改学生信息菜单项"""
    print("  --- 修改学生信息 ---")
    sid = input("    请输入要修改的学号: ").strip()
    stu = system.search_student(sid)
    if not stu:
        raise KeyError(f"未找到学号为 {sid} 的学生")
    print("    当前信息:")
    display_student(stu[0])

    print("    (留空表示不修改)")
    new_name = input("    新姓名: ").strip() or None
    new_age_str = input("    新年龄: ").strip()
    new_age = int(new_age_str) if new_age_str else None
    new_grade = input(f"    新年级 ({'/'.join(StudentSystem.VALID_GRADES)}): ").strip() or None
    new_major = input("    新专业: ").strip() or None
    new_email = input("    新邮箱: ").strip() or None
    new_phone = input("    新电话: ").strip() or None

    kwargs = {
        "name": new_name, "age": new_age,
        "grade": new_grade, "major": new_major,
        "email": new_email, "phone": new_phone,
    }
    system.update_student(sid, **kwargs)


def _list_all(system: StudentSystem) -> None:
    """列出所有学生"""
    print("  --- 全部学生 ---")
    display_students(system.list_students())


def _show_stats(system: StudentSystem) -> None:
    """显示统计信息"""
    print("  --- 统计信息 ---")
    students = system.list_students()
    print(f"  学生总数: {len(students)}")

    if students:
        print(f"\n  按年级分布:")
        for grade, count in system.get_grade_statistics().items():
            print(f"    {grade}: {count} 人")

        print(f"\n  按专业分布:")
        for major, count in system.get_major_statistics().items():
            print(f"    {major}: {count} 人")


def _exit_system(system: StudentSystem) -> None:
    """退出系统"""
    print("  感谢使用学生信息管理系统，再见！")
    raise SystemExit(0)


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        run_menu()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        print("\n  用户中断，退出系统。")
