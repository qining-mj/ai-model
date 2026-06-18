"""
03_model_comparison.py
模型对比实验

对比 gpt-4o-mini、gpt-4o 等模型在不同任务上的表现
"""
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def compare_models_simple_task():
    """简单任务对比：翻译"""
    print("=" * 60)
    print("【对比1】简单任务 - 翻译")
    print("=" * 60)

    prompt = "把下面的句子翻译成英文：春眠不觉晓，处处闻啼鸟。"
    models = ["gpt-4o-mini", "gpt-4o"]

    for model in models:
        print(f"\n>>> 模型: {model}")
        start = time.time()

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            elapsed = time.time() - start
            result = response.choices[0].message.content
            tokens = response.usage.total_tokens

            print(f"  回复: {result}")
            print(f"  耗时: {elapsed:.2f}秒")
            print(f"  Token: {tokens}")

        except Exception as e:
            print(f"  错误: {e}")


def compare_models_reasoning_task():
    """推理任务对比：数学问题"""
    print("\n" + "=" * 60)
    print("【对比2】推理任务 - 数学问题")
    print("=" * 60)

    prompt = """
    小明有5个苹果，小红比小明多3个苹果，小华的苹果数是小红的2倍。
    问：三个人一共有多少个苹果？
    请一步一步思考。
    """

    models = ["gpt-4o-mini", "gpt-4o"]

    for model in models:
        print(f"\n>>> 模型: {model}")
        start = time.time()

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            elapsed = time.time() - start
            result = response.choices[0].message.content
            tokens = response.usage.total_tokens

            print(f"  回复:\n{result}")
            print(f"\n  耗时: {elapsed:.2f}秒")
            print(f"  Token: {tokens}")

        except Exception as e:
            print(f"  错误: {e}")


def compare_models_creative_task():
    """创意任务对比：写诗"""
    print("\n" + "=" * 60)
    print("【对比3】创意任务 - 写诗")
    print("=" * 60)

    prompt = "写一首关于人工智能的七言绝句"
    models = ["gpt-4o-mini", "gpt-4o"]

    for model in models:
        print(f"\n>>> 模型: {model}")
        start = time.time()

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8
            )

            elapsed = time.time() - start
            result = response.choices[0].message.content
            tokens = response.usage.total_tokens

            print(f"  回复:\n{result}")
            print(f"\n  耗时: {elapsed:.2f}秒")
            print(f"  Token: {tokens}")

        except Exception as e:
            print(f"  错误: {e}")


def model_selection_guide():
    """模型选择建议"""
    print("\n" + "=" * 60)
    print("【模型选择指南】")
    print("=" * 60)

    guide = """
    ┌─────────────────┬──────────────────┬───────────────────┐
    │  任务类型        │  推荐模型         │  原因             │
    ├─────────────────┼──────────────────┼───────────────────┤
    │  日常对话/问答   │  gpt-4o-mini     │  便宜、快、够用    │
    │  翻译/摘要       │  gpt-4o-mini     │  性价比最高        │
    │  代码生成        │  gpt-4o-mini     │  代码能力足够      │
    │  复杂推理/数学   │  gpt-4o / o1     │  需要更强推理      │
    │  图像理解        │  gpt-4o          │  多模态能力        │
    │  顶级质量要求    │  gpt-4o          │  最强综合能力      │
    │  科研/竞赛难题   │  o1              │  最强推理能力      │
    └─────────────────┴──────────────────┴───────────────────┘

    💡 经验法则：
    1. 默认用 gpt-4o-mini，遇到瓶颈再升级
    2. 90% 的任务 gpt-4o-mini 都能胜任
    3. gpt-4o 成本是 mini 的 16 倍，慎用
    """
    print(guide)


if __name__ == "__main__":
    compare_models_simple_task()
    compare_models_reasoning_task()
    compare_models_creative_task()
    model_selection_guide()
