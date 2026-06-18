"""
06_token_counting.py
Token 计算与成本估算

演示如何准确计算 Token 数量和预估 API 调用成本
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 尝试导入 tiktoken，如果没有安装则提示
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    print("⚠️ tiktoken 未安装，请运行: pip install tiktoken")


# 模型定价表（美元 / 1M tokens，2024年价格）
PRICING = {
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.6},
    "gpt-4-turbo": {"input": 10.0, "output": 30.0},
    "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
    "o1": {"input": 15.0, "output": 60.0},
    "o1-mini": {"input": 3.0, "output": 12.0},
}


def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """
    计算文本的 Token 数量

    Args:
        text: 要计算的文本
        model: 模型名称

    Returns:
        Token 数量
    """
    if not TIKTOKEN_AVAILABLE:
        # 粗略估算：英文约 1 word = 1.3 token，中文约 1 字 = 1.5 token
        return int(len(text) * 0.5)

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # 如果模型不支持，使用 cl100k_base（GPT-4 系列的编码器）
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(text))


def count_messages_tokens(messages: list, model: str = "gpt-4o-mini") -> int:
    """
    计算消息列表的 Token 数量

    OpenAI 的消息格式会额外消耗一些 Token
    """
    if not TIKTOKEN_AVAILABLE:
        total = sum(len(m.get("content", "")) for m in messages)
        return int(total * 0.5) + len(messages) * 4

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens_per_message = 3  # 每条消息的开销
    tokens_per_name = 1     # 如果有 name 字段的额外开销

    total = 0
    for message in messages:
        total += tokens_per_message
        for key, value in message.items():
            total += len(encoding.encode(str(value)))
            if key == "name":
                total += tokens_per_name

    total += 3  # 每次请求的固定开销

    return total


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "gpt-4o-mini"
) -> dict:
    """
    估算 API 调用成本

    Returns:
        {
            "input_cost": float,
            "output_cost": float,
            "total_cost": float,
            "currency": "USD"
        }
    """
    pricing = PRICING.get(model, PRICING["gpt-4o-mini"])

    input_cost = input_tokens * pricing["input"] / 1_000_000
    output_cost = output_tokens * pricing["output"] / 1_000_000

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": input_cost + output_cost,
        "currency": "USD"
    }


def demo_token_counting():
    """Token 计算演示"""
    print("=" * 60)
    print("【演示】Token 计算")
    print("=" * 60)

    # 测试文本
    texts = [
        "Hello, world!",
        "你好，世界！",
        "The quick brown fox jumps over the lazy dog.",
        "人工智能正在改变我们的生活方式，从智能家居到自动驾驶汽车。",
        "def hello():\n    print('Hello, World!')",
    ]

    print("\n文本 Token 数量：")
    for text in texts:
        tokens = count_tokens(text)
        print(f"  {tokens:4d} tokens | {text[:40]}{'...' if len(text) > 40 else ''}")


def demo_message_tokens():
    """消息 Token 计算演示"""
    print("\n" + "=" * 60)
    print("【演示】消息 Token 计算")
    print("=" * 60)

    messages = [
        {"role": "system", "content": "你是一个专业的Python程序员，回答简洁准确。"},
        {"role": "user", "content": "什么是列表推导式？请给一个例子。"},
    ]

    tokens = count_messages_tokens(messages)
    print(f"\n消息列表 Token: {tokens}")

    print("\n消息详情：")
    for msg in messages:
        msg_tokens = count_tokens(msg["content"])
        print(f"  [{msg['role']:9s}] {msg_tokens:3d} tokens | {msg['content'][:30]}...")


def demo_cost_estimation():
    """成本估算演示"""
    print("\n" + "=" * 60)
    print("【演示】成本估算")
    print("=" * 60)

    # 场景：翻译 1000 篇文章
    articles = 1000
    avg_input_tokens = 500   # 每篇文章平均 500 token
    avg_output_tokens = 600  # 翻译输出平均 600 token

    total_input = articles * avg_input_tokens
    total_output = articles * avg_output_tokens

    print(f"\n场景：翻译 {articles} 篇文章")
    print(f"  平均输入: {avg_input_tokens} tokens/篇")
    print(f"  平均输出: {avg_output_tokens} tokens/篇")
    print(f"  总输入: {total_input:,} tokens")
    print(f"  总输出: {total_output:,} tokens")

    print("\n各模型成本对比：")
    print("-" * 50)

    for model in ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]:
        cost = estimate_cost(total_input, total_output, model)
        print(f"  {model:15s}: ${cost['total_cost']:.2f}")


def demo_pricing_table():
    """定价表展示"""
    print("\n" + "=" * 60)
    print("【OpenAI 模型定价表】(2024)")
    print("=" * 60)

    print("\n价格单位: 美元 / 1M tokens")
    print("-" * 50)
    print(f"{'模型':<18} {'输入':>10} {'输出':>10}")
    print("-" * 50)

    for model, price in PRICING.items():
        print(f"{model:<18} ${price['input']:>8.2f} ${price['output']:>8.2f}")

    print("-" * 50)
    print("\n💡 成本优化建议：")
    print("  1. 日常任务用 gpt-4o-mini，成本仅为 gpt-4o 的 6%")
    print("  2. 用 max_tokens 限制输出长度")
    print("  3. 精简 System Prompt，减少每次请求的固定开销")
    print("  4. 对重复请求使用缓存")


def main():
    demo_token_counting()
    demo_message_tokens()
    demo_cost_estimation()
    demo_pricing_table()


if __name__ == "__main__":
    main()
