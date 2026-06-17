# 第1章 · 起步 — 从安装到第一个Python程序

> **时长**：约 3 小时 ｜ **难度**：⭐ ｜ **类型**：动手实操
>
> **目标**：从零开始搭建 Python 开发环境，掌握最基本的语法要素，并成功运行你的第一个 Python 程序。

---

## 学习目标

学完本章后，你将能够：
- 说出 Python 的历史、特点以及主要应用领域
- 在 Windows / macOS / Linux 上独立安装 Python 并验证版本
- 使用交互式解释器（REPL）执行简单代码
- 理解标识符命名规则、关键字列表、缩进规则等基础语法
- 正确使用单行注释和多行注释
- 使用 `print()` 和 `input()` 完成基本的输入输出
- 编写并运行第一个完整的 Python 程序

---

## 知识地图

```mermaid
graph TD
    A["Python 起步"] --> B["Python 简介"]
    A --> C["环境搭建"]
    A --> D["基础语法"]
    A --> E["注释"]
    A --> F["输入输出"]
    A --> G["第一个程序"]
    B --> B1["历史与特点"]
    B --> B2["应用领域"]
    C --> C1["Windows 安装"]
    C --> C2["macOS 安装"]
    C --> C3["Linux 安装"]
    C --> C4["验证 & REPL"]
    D --> D1["编码声明"]
    D --> D2["标识符 & 关键字"]
    D --> D3["缩进规则"]
    D --> D4["多行 & 多语句"]
    E --> E1["单行 #"]
    E --> E2["多行 \"\"\""]
    F --> F1["print()"]
    F --> F2["input()"]
```

---

## 1、Python 是什么

**概念定义**：Python 是一种解释型、面向对象、动态数据类型的高级程序设计语言。由荷兰人 Guido van Rossum 于 1989 年圣诞节开始设计，1991 年首次发布。Python 这个名字来源于 Guido 喜爱的喜剧团体 Monty Python's Flying Circus。

**核心价值**：Python 的设计哲学强调代码的可读性和简洁的语法（"优雅"、"明确"、"简单"），使得开发者能够用更少的代码表达想法，极大地降低了编程入门门槛，同时保持了足够强大的能力来构建企业级应用。

### 主要特点

- **简洁易读**：使用缩进而非花括号来界定代码块，语法接近自然语言
- **跨平台**：Windows / macOS / Linux 均可运行，代码无需修改即可跨平台执行
- **解释型语言**：代码逐行执行，无需编译，调试方便
- **动态类型**：变量不需要声明类型，运行时自动推断
- **丰富的标准库**：自带"电池"（batteries included），涵盖文件 I/O、网络、正则、数据库等
- **强大的第三方生态**：PyPI 上有超过 40 万个第三方包

### 应用领域对比

| 领域 | 代表框架/库 | 为什么用 Python |
|------|-------------|-----------------|
| Web 开发 | Django, Flask, FastAPI | 开发效率高，生态完善 |
| 数据分析 | Pandas, NumPy | 语法简洁，社区活跃 |
| 人工智能 | PyTorch, TensorFlow | 灵活的实验性语言，大量学术资源 |
| 自动化运维 | Ansible, SaltStack | 脚本能力强，跨平台 |
| 科学计算 | SciPy, Matplotlib | 与数学语法接近 |
| 桌面应用 | PyQt, Tkinter | 快速原型开发 |
| 游戏开发 | Pygame | 适合教学和 2D 小游戏 |

### 版本选择

Python 2.x 已于 2020 年 1 月 1 日正式终止支持（EOL）。本书所有内容均基于 **Python 3.x**（推荐 3.10+）。请务必使用 Python 3 版本学习。

---

## 2、环境搭建

**概念定义**：Python 环境搭建是指在你的操作系统中安装 Python 解释器，并确保可以在终端/命令行中调用它。解释器是运行 Python 代码的核心程序。

**核心价值**：正确搭建开发环境是学习编程的第一步。一个干净、稳定的环境能避免后续学习过程中 80% 以上的"环境问题"，让你把精力集中在编程本身。

### Windows 安装

**方式一：Microsoft Store（推荐初学者）**

1. 打开 Microsoft Store，搜索 "Python"
2. 选择 Python 3.12+（由 Python Software Foundation 发布）
3. 点击"安装"，自动配置环境变量
4. 安装完成后打开命令提示符（cmd）或 PowerShell，验证安装

**方式二：winget（推荐开发者）**

```powershell
winget install Python.Python.3.12
```

**方式三：官网安装包**

1. 访问 [python.org](https://python.org) 下载最新版安装包
2. 运行安装程序，**务必勾选** "Add Python to PATH"
3. 选择 "Install Now" 完成安装

### macOS 安装

**推荐使用 pyenv 管理 Python 版本**：

```bash
# 使用 Homebrew 安装 pyenv
brew install pyenv

# 安装指定 Python 版本
pyenv install 3.12.0

# 设为全局默认
pyenv global 3.12.0
```

也可以直接从 python.org 下载 macOS 安装包，但 pyenv 更便于多版本切换。

### Linux 安装

**Ubuntu / Debian**：

```bash
sudo apt update
sudo apt install python3 python3-pip
```

**CentOS / RHEL / Fedora**：

```bash
sudo yum install python3    # CentOS 7+
sudo dnf install python3    # Fedora
```

### 验证安装

无论哪种操作系统，安装完成后在终端执行：

```powershell
python --version
```

或（Linux/macOS 可能需用）：

```bash
python3 --version
```

看到类似 `Python 3.12.x` 的输出即表示安装成功。

### 交互式解释器（REPL）

REPL 代表 Read-Eval-Print Loop（读取-求值-输出-循环），是 Python 自带的交互式编程环境。

在终端直接输入 `python`（或 `python3`）即可进入：

```python
Python 3.12.0 (tags/v3.12.0, ...)
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

在 `>>>` 提示符后输入代码，立即执行并显示结果：

```python
>>> print("Hello, Python!")
Hello, Python!

>>> 1 + 2 + 3 + 4 + 5
15

>>> 2 ** 10
1024

>>> exit()  # 退出 REPL
```

> REPL 非常适合快速验证想法、测试小段代码、学习新语法。学会善用 REPL 能显著提升学习效率。

### ▶ 代码案例

```powershell
cd code/01-起步-代码案例
python check_python_version.py
```

---

## 3、基础语法

**概念定义**：基础语法是编程语言的"规则手册"，规定了代码应该如何书写才能被解释器正确理解。包括编码声明、标识符、关键字、缩进、语句分隔等规则。

**核心价值**：准确掌握基础语法是写出正确、规范代码的前提。Python 的语法设计以简洁著称，但正是这些"规矩"保证了代码的可读性和一致性。

### 3.1 编码声明

Python 3 默认使用 UTF-8 编码，因此源文件中可以直接使用中文等 Unicode 字符：

```python
# -*- coding: utf-8 -*-
# 在 Python 3 中，上面的声明是可选默认的，但保留它是好习惯
print("你好，世界！")
```

### 3.2 标识符命名规则

标识符是变量、函数、类等的名字，必须遵守以下规则：

- 由 **字母**（a-z, A-Z）、**下划线**（_）和 **数字**（0-9）组成
- **不能以数字开头**
- **区分大小写**：`name` 和 `Name` 是两个不同的标识符
- 不能使用 Python 关键字

```python
# 合法标识符
name = "Alice"
my_name = "Bob"
_name = "private"
name1 = "Charlie"
camelCase = "ok"

# 不合法标识符（会报 SyntaxError）
# 1name = "error"    # 数字开头
# my-name = "error"  # 不允许连字符
# class = "error"    # 使用了关键字
```

### 3.3 关键字列表

关键字是 Python 语言保留的特殊标识符，有特定含义，不能用作变量名。

```python
import keyword

print(keyword.kwlist)
# 输出：['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
#        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
#        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
#        'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
#        'try', 'while', 'with', 'yield']

print(f"Python 共有 {len(keyword.kwlist)} 个关键字")
```

### 3.4 缩进规则

Python 使用 **缩进** 来表示代码块，而不是像其他语言那样使用花括号 `{}`。

```python
# 正确的缩进
if True:
    print("条件为真")      # 4 个空格缩进
    print("同一代码块")
else:
    print("条件为假")

# 缩进不一致会报错！
# if True:
#     print("4个空格")
# 	print("tab")      # IndentationError: unexpected indent
```

> **最佳实践**：始终使用 **4 个空格** 作为一级缩进，不要在同一个文件中混用 Tab 和空格。大多数现代编辑器（VS Code、PyCharm 等）默认将 Tab 键转换为 4 个空格。

### 3.5 多行语句

当一行代码太长时，可以用反斜杠 `\` 换行，或者在括号内自动换行：

```python
# 方法一：反斜杠续行
total = 1 + 2 + 3 \
      + 4 + 5 + 6

# 方法二：括号内自动换行（推荐）
total = (1 + 2 + 3
         + 4 + 5 + 6)

# 括号包括圆括号()、方括号[]、花括号{}
my_list = [
    1, 2, 3,
    4, 5, 6
]
```

### 3.6 一行多语句

可以用分号 `;` 在一行中写多条语句，但**不推荐**这样做，会影响可读性：

```python
# 不推荐，仅供了解
name = "Alice"; age = 20; print(name, age)

# 推荐写法（每行一条语句）
name = "Alice"
age = 20
print(name, age)
```

### ▶ 代码案例

```powershell
cd code/01-起步-代码案例
python basic_syntax.py
```

---

## 4、注释

**概念定义**：注释是代码中被解释器忽略的文本，用于向阅读代码的人提供解释、说明或提醒。注释不是写给计算机的，而是写给人的。

**核心价值**：良好的注释能极大提升代码的可维护性。好的注释回答"为什么这样做"，而不是"做了什么"（代码本身已经回答了后者）。养成写注释的习惯，是对未来自己和其他开发者的善意。

### 4.1 单行注释

使用 `#` 开头，从 `#` 到行尾都是注释：

```python
# 这是单行注释
print("Hello")  # 行尾也可以加注释

# 多个单行注释可以连用
# 模拟多行注释的效果
```

### 4.2 多行注释

使用三个单引号 `'''` 或三个双引号 `"""` 包裹：

```python
'''
这是多行注释
使用三个单引号
可以跨多行
'''

"""
这也是多行注释
使用三个双引号
效果完全相同
"""
```

> **注意**：三引号注释实质上是未被赋值给任何变量的字符串字面量。它们在运行时仍会创建字符串对象（虽被垃圾回收），但在日常使用中作为注释绝无问题。严格意义上，Python 没有原生多行注释语法，这是"约定俗成"的用法。

### 4.3 注释最佳实践

```python
# 1. 用注释解释"为什么"，而非"是什么"
# BAD: 将变量加1
counter = counter + 1

# GOOD: 跳过标题行（第1行），因为文件格式规定第1行为列名
start_processing_from_line_2()

# 2. 代码应当自解释，注释只补充上下文
# BAD 的极端：x = x + 1  # 给x加1

# 3. TODO 注释标记未完成的工作
# TODO: 处理边缘情况——当文件为空时
```

### ▶ 代码案例

```powershell
cd code/01-起步-代码案例
python comments_demo.py
```

---

## 5、输入输出

**概念定义**：`print()` 是 Python 内置的输出函数，将内容打印到控制台；`input()` 是内置的输入函数，从控制台读取用户输入。

**核心价值**：输入输出是程序与用户交互的基本方式。`print()` 是调试程序最常用的工具，而 `input()` 让程序能够接收动态数据，使程序从"死"变"活"。

### 5.1 print() 函数

`print()` 的基本用法和常用参数：

```python
# 基本输出
print("Hello, World!")

# 多个参数——自动用空格分隔
print("Hello", "World", "Python")  # 输出：Hello World Python

# sep 参数——自定义分隔符
print("2024", "01", "15", sep="-")  # 输出：2024-01-15
print("A", "B", "C", sep=" | ")     # 输出：A | B | C

# end 参数——自定义结尾（默认是换行符 \n）
print("正在下载", end="")
print("...", end="")
print("完成！")
# 输出：正在下载...完成！

# 组合使用
print("姓名", "年龄", "城市", sep=" | ", end="\n---\n")
print("Alice", 20, "北京", sep=" | ")
```

### 5.2 input() 函数

`input()` 从用户获取输入，返回的数据类型永远是**字符串**：

```python
# 基本用法
name = input("请输入你的名字：")
print(f"你好，{name}！")

# input() 返回的是字符串，需要数字时要手动转换
age_str = input("请输入你的年龄：")
age = int(age_str)  # 字符串 → 整数
print(f"明年你 {age + 1} 岁")

# 一行代码完成输入和转换
height = float(input("请输入身高(cm)："))
print(f"你的身高是 {height} cm")
```

### 5.3 综合示例

```python
# 一个简单的个人信息收集程序
name = input("姓名：")
age = int(input("年龄："))
city = input("城市：")

# 格式化输出
print("--- 个人信息 ---")
print(f"姓名：{name}")
print(f"年龄：{age}")
print(f"城市：{city}")
print(f"{name} 明年 {age + 1} 岁，住在 {city}。")
```

### ▶ 代码案例

```powershell
cd code/01-起步-代码案例
python hello_world.py
```

---

## 6、第一个程序

**概念定义**：一个完整的 Python 程序是由若干语句组成的文本文件（`.py` 后缀），由 Python 解释器顺序执行。

**核心价值**：从第一个程序开始，建立"编写 → 保存 → 运行"的完整工作流，是编程学习的起点。

### 第一个完整的 Python 程序

创建一个文件 `hello_world.py`，输入以下内容：

```python
# hello_world.py —— 我的第一个 Python 程序

# 1. 获取用户输入
name = input("请输入你的名字：")

# 2. 获取年龄并转换为整数
age = int(input("请输入你的年龄："))

# 3. 计算明年年龄
next_year_age = age + 1

# 4. 输出问候信息
print(f"你好，{name}！")
print(f"你明年 {next_year_age} 岁。")

# 5. 根据年龄给出简单反馈
if age < 18:
    print("你还在成长阶段，加油学习！")
else:
    print("欢迎来到 Python 的世界！")
```

### 逐行解释

| 行号 | 代码 | 说明 |
|------|------|------|
| 1 | `# hello_world.py ...` | 注释，描述文件用途 |
| 4 | `name = input(...)` | 调用 input() 获取用户输入，赋值给变量 `name` |
| 7 | `age = int(input(...))` | 先 input 获取字符串，再 int() 转为整数 |
| 10 | `next_year_age = age + 1` | 算术运算，将结果赋给新变量 |
| 13 | `print(f"...{name}...")` | f-string 格式化输出，用 `{}` 嵌入变量 |
| 16-19 | `if ... else ...` | 条件分支语句（后续章节详解） |

### 运行程序

```powershell
cd code/01-起步-代码案例
python hello_world.py
```

运行后与程序交互：

```
请输入你的名字：Alice
请输入你的年龄：20
你好，Alice！
你明年 21 岁。
欢迎来到 Python 的世界！
```

### ▶ 代码案例

```powershell
cd code/01-起步-代码案例
python hello_world.py
```

---

## 常见踩坑

1. **安装时忘记勾选 "Add Python to PATH"**：在命令行输入 `python` 提示"不是内部或外部命令"。→ 重新运行安装程序，选择 Modify 并勾选 PATH 选项；或手动将 Python 安装目录添加到系统环境变量。

2. **缩进混用 Tab 和空格**：`IndentationError: unexpected indent`。→ 在编辑器中开启"显示空格/Tab"功能，并使用"将 Tab 转换为空格"功能统一为 4 个空格。

3. **input() 返回的字符串直接参与数字运算**：`TypeError: can only concatenate str`。→ 记住 `input()` 永远返回字符串，需要用 `int()` 或 `float()` 显式转换为数字后再进行数学运算。

4. **中文编码问题**：在极少数旧系统上，`print("中文")` 出现乱码或报错。→ 确认文件顶部有 `# -*- coding: utf-8 -*-`；确保编辑器以 UTF-8 编码保存文件。

5. **`python` vs `python3` 命令混淆**：macOS/Linux 上 `python` 可能指向 Python 2.x。→ 使用 `python --version` 检查；在 Linux/macOS 上统一使用 `python3` 命令。

---

---

## 本节小结

- ✅ Python 是解释型、动态类型的高级语言，以简洁优雅著称，广泛应用于 Web、数据科学、AI 等领域
- ✅ 通过官网、包管理器或 pyenv 安装 Python，验证 `python --version`
- ✅ REPL 交互式环境是快速实验的好工具
- ✅ 标识符以字母或下划线开头，区分大小写，不能使用关键字
- ✅ 缩进是 Python 的代码块标记，始终使用 4 个空格
- ✅ 单行注释用 `#`，多行注释用 `'''` 或 `"""`
- ✅ `print()` 支持 `sep` 和 `end` 参数自定义输出格式
- ✅ `input()` 返回字符串，数字输入需手动类型转换

---

> **下一章**：[第2章 · 数据类型与运算符 — 掌握Python的基石](./第2章%20·%20数据类型与运算符%20—%20掌握Python的基石.md)——从变量到运算符，扎实掌握 Python 的核心数据类型和运算规则。
