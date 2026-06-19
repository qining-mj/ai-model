"""
02_parameters_demo.py
核心参数对比实验

演示 temperature、top_p、max_tokens 等参数的效果
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def demo_temperature():
    """演示 temperature 参数的效果"""
    print("=" * 60)
    print("【实验1】temperature 参数对比")
    print("=" * 60)

    prompt = "给公司起一个名字，行业是人工智能"

    for temp in [0, 0.5, 1.0, 1.5]:
        print(f"\n>>> temperature = {temp}")

        # 同样的问题问3次，观察一致性
        for i in range(3):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                max_tokens=50
            )
            print(f"  第{i+1}次: {response.choices[0].message.content.strip()}")


def demo_max_tokens():
    """演示 max_tokens 参数的效果"""
    print("\n" + "=" * 60)
    print("【实验2】max_tokens 参数对比")
    print("=" * 60)

    prompt = "详细介绍Python语言的特点"

    for max_tok in [20, 50, 100]:
        print(f"\n>>> max_tokens = {max_tok}")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tok,
            temperature=0.7
        )
        result = response.choices[0].message.content
        print(f"  回复({len(result)}字): {result[:100]}...")

        # 检查是否被截断
        if response.choices[0].finish_reason == "length":
            print("  ⚠️ 回复被截断！")


def demo_stop():
    """演示 stop 参数的效果"""
    print("\n" + "=" * 60)
    print("【实验3】stop 参数演示")
    print("=" * 60)

    prompt = "列出5种常见的编程语言：\n1."

    # 不设置 stop
    print("\n>>> 不设置 stop:")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    print(response.choices[0].message.content)

    # 设置 stop 为 "3."，只输出前2个
    print("\n>>> stop=['3.']（遇到'3.'就停止）:")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        stop=["3."]
    )
    print(response.choices[0].message.content)


def demo_seed():
    """演示 seed 参数的效果"""
    print("\n" + "=" * 60)
    print("【实验4】seed 参数演示（可复现性）")
    print("=" * 60)

    prompt = "生成一个随机的人名"

    print("\n>>> 不设置 seed（每次不同）:")
    for i in range(3):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=1
        )
        print(f"  第{i+1}次: {response.choices[0].message.content.strip()}")

    print("\n>>> seed=42, temperature=0（尽量相同）:")
    for i in range(3):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            seed=42
        )
        print(f"  第{i+1}次: {response.choices[0].message.content.strip()}")


if __name__ == "__main__":
    demo_temperature()
    demo_max_tokens()
    demo_stop()
    demo_seed()

    print("\n" + "=" * 60)
    print("实验完成！")
