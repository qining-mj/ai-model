"""
02_deepseek_basic.py
DeepSeek 基础调用示例

特点：
- 极致性价比（价格仅为 GPT-4 的 1/50）
- 完全兼容 OpenAI API 格式
- 代码能力出色

运行前准备：
1. pip install openai python-dotenv
2. 在 .env 文件中添加：
   DEEPSEEK_API_KEY=sk-xxx
   DEEPSEEK_BASE_URL=https://api.deepseek.com
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def basic_chat():
    """基础对话示例"""
    print("=" * 60)
    print("【DeepSeek 基础对话】")
    print("=" * 60)

    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个有帮助的助手"},
            {"role": "user", "content": "用一句话介绍 DeepSeek"}
        ],
        temperature=0.7
    )

    print(f"\n回复: {response.choices[0].message.content}")
    print(f"\nToken 用量:")
    print(f"  输入: {response.usage.prompt_tokens}")
    print(f"  输出: {response.usage.completion_tokens}")

    # 计算成本（deepseek-chat: 输入 ¥1/M，输出 ¥2/M）
    input_cost = response.usage.prompt_tokens * 1 / 1_000_000
    output_cost = response.usage.completion_tokens * 2 / 1_000_000
    print(f"\n预估成本: ¥{input_cost + output_cost:.6f}")


def code_generation():
    """代码生成示例"""
    print("\n" + "=" * 60)
    print("【DeepSeek 代码生成】")
    print("=" * 60)

    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    )

    response = client.chat.completions.create(
        model="deepseek-coder",  # 代码专用模型
        messages=[
            {
                "role": "system",
                "content": "你是一个专业的 Python 程序员，编写高质量、有注释的代码。"
            },
            {
                "role": "user",
                "content": "实现一个简单的 LRU 缓存装饰器"
            }
        ],
        temperature=0
    )

    print(response.choices[0].message.content)


def streaming_chat():
    """流式输出示例"""
    print("\n" + "=" * 60)
    print("【DeepSeek 流式输出】")
    print("=" * 60)

    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    )

    print("\n回复: ", end="")

    stream = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "写一首关于编程的五言绝句"}
        ],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print()


def show_pricing():
    """展示 DeepSeek 价格优势"""
    print("\n" + "=" * 60)
    print("【DeepSeek 价格对比】")
    print("=" * 60)

    comparison = """
    ┌─────────────────┬───────────────┬───────────────┬──────────────┐
    │  模型            │  输入价格      │  输出价格      │  相对GPT-4o  │
    ├─────────────────┼───────────────┼───────────────┼──────────────┤
    │  GPT-4o         │  $2.5/M       │  $10/M        │  基准        │
    │  GPT-4o-mini    │  $0.15/M      │  $0.6/M       │  6%          │
    │  Claude 3.5     │  $3/M         │  $15/M        │  120%        │
    │  DeepSeek       │  ¥1/M(≈$0.14) │  ¥2/M(≈$0.28) │  约2%        │
    └─────────────────┴───────────────┴───────────────┴──────────────┘

    💰 DeepSeek 的成本优势：
    - 价格仅为 GPT-4o 的 1/50
    - 价格约为 GPT-4o-mini 的 1/3
    - 适合大批量处理任务
    - 适合成本敏感的场景

    💡 推荐使用场景：
    - 原型开发和测试
    - 大批量文本处理
    - 代码生成和补全
    - 对成本敏感的生产环境
    """
    print(comparison)


if __name__ == "__main__":
    show_pricing()

    if os.getenv("DEEPSEEK_API_KEY"):
        basic_chat()
        code_generation()
        streaming_chat()
    else:
        print("\n⚠️ 未设置 DEEPSEEK_API_KEY，跳过实际调用演示")
