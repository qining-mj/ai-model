"""
01_basic_prompt.py
Prompt 基础示例

演示基本 Prompt 的编写和效果对比
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def compare_prompts():
    """对比不同质量的 Prompt 效果"""

    print("=" * 60)
    print("【模糊 vs 清晰 Prompt 对比】")
    print("=" * 60)

    # 模糊的 Prompt
    vague_prompt = "写个函数"

    # 清晰的 Prompt
    clear_prompt = """请用 Python 编写一个函数，要求：
1. 功能：计算列表中所有偶数的和
2. 参数：接收一个整数列表
3. 返回：偶数之和
4. 处理：空列表返回 0
5. 添加函数文档字符串和类型注解"""

    print("\n--- 模糊 Prompt ---")
    print(f"Prompt: {vague_prompt}\n")

    response1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": vague_prompt}],
        max_tokens=200
    )
    print(f"回复:\n{response1.choices[0].message.content}\n")

    print("\n--- 清晰 Prompt ---")
    print(f"Prompt:\n{clear_prompt}\n")

    response2 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": clear_prompt}],
        max_tokens=500
    )
    print(f"回复:\n{response2.choices[0].message.content}")


def role_demo():
    """演示角色设定的效果"""
    question = "什么是递归？"

    roles = [
        ("无角色", None),
        ("技术专家", "你是一位资深软件工程师，善于用精准的技术语言解释概念。回答要专业、准确。"),
        ("启蒙老师", "你是一位幼儿园老师，擅长用小朋友能理解的方式解释任何概念。使用简单的比喻和例子。"),
    ]

    print("\n" + "=" * 60)
    print("【角色设定对比】")
    print("=" * 60)
    print(f"问题: {question}\n")

    for role_name, system_prompt in roles:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": question})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=200
        )

        print(f"--- {role_name} ---")
        print(f"{response.choices[0].message.content}\n")


def structured_prompt_demo():
    """演示结构化 Prompt"""

    print("\n" + "=" * 60)
    print("【结构化 Prompt 示例】")
    print("=" * 60)

    structured_prompt = """## 任务
分析以下代码的问题并提供改进建议。

## 代码
```python
def calc(x,y):
    return x/y
```

## 要求
1. 列出所有潜在问题
2. 每个问题标注严重程度（高/中/低）
3. 提供修复后的代码

## 输出格式
问题列表 → 修复代码 → 总结"""

    print(f"Prompt:\n{structured_prompt}\n")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": structured_prompt}],
        max_tokens=500
    )
    print(f"回复:\n{response.choices[0].message.content}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY 环境变量")
        exit()

    compare_prompts()
    role_demo()
    structured_prompt_demo()
