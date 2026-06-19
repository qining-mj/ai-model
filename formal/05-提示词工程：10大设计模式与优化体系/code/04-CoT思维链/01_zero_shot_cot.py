"""
01_zero_shot_cot.py
Zero-shot Chain-of-Thought 示例
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def compare_with_and_without_cot():
    """对比有无 CoT 的效果"""

    problems = [
        # 数学问题
        "一个农场有 15 只鸡和 12 只鸭。农夫卖掉了 7 只鸡，又买入 5 只鸭。现在农场有多少只家禽？",

        # 逻辑问题
        "小明比小红高，小红比小华高，小华比小刚矮。请问谁最高？",

        # 常识推理
        "张三周一上班迟到了，被扣了 50 元。周二到周五他都准时到达。这周他因迟到被扣了多少钱？",

        # 多步计算
        "一本书原价 80 元，打 8 折后又减 10 元优惠券，最终价格是多少？",
    ]

    for i, problem in enumerate(problems, 1):
        print(f"\n{'='*60}")
        print(f"问题 {i}: {problem}")
        print("="*60)

        # 无 CoT
        response1 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": problem}],
            max_tokens=100
        )
        print(f"\n【无 CoT】")
        print(response1.choices[0].message.content)

        # 有 CoT
        cot_prompt = f"{problem}\n\n让我们一步一步思考。"
        response2 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": cot_prompt}],
            max_tokens=400
        )
        print(f"\n【有 CoT】")
        print(response2.choices[0].message.content)


def different_cot_triggers():
    """不同的 CoT 触发词"""

    problem = "书店有 45 本书，卖掉 18 本，又进货 23 本，现在有多少本书？"

    triggers = [
        "让我们一步一步思考。",
        "请展示你的推理过程。",
        "让我们分析一下这个问题。",
        "First, let's break this down step by step.",
        "请详细说明解题步骤。",
    ]

    print("\n" + "=" * 60)
    print("【不同 CoT 触发词效果】")
    print("=" * 60)
    print(f"问题: {problem}\n")

    for trigger in triggers:
        prompt = f"{problem}\n\n{trigger}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        print(f"--- 触发词: {trigger[:20]}... ---")
        # 只显示前150字
        content = response.choices[0].message.content
        print(content[:150] + "..." if len(content) > 150 else content)
        print()


def cot_for_code_debug():
    """CoT 用于代码调试"""

    print("\n" + "=" * 60)
    print("【CoT 代码调试】")
    print("=" * 60)

    prompt = """下面这段代码有 bug，请帮我找出来。

```python
def find_max(numbers):
    max_num = 0
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

# 测试
print(find_max([-1, -5, -3]))  # 期望输出 -1，实际输出 0
```

让我们一步一步分析这个问题：
1. 首先理解代码的意图
2. 然后跟踪代码执行过程
3. 找出问题所在
4. 给出修复方案"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    compare_with_and_without_cot()
    different_cot_triggers()
    cot_for_code_debug()
