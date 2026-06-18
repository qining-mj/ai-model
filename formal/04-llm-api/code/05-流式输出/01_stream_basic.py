"""
01_stream_basic.py
各平台流式输出基础示例

运行前准备：
1. pip install openai anthropic python-dotenv
2. 在 .env 文件中添加相应的 API Key
"""
import os
from dotenv import load_dotenv

load_dotenv()


def openai_stream():
    """OpenAI 流式调用"""
    print("=" * 60)
    print("【OpenAI 流式输出】")
    print("=" * 60)

    from openai import OpenAI

    client = OpenAI()

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "写一首关于春天的诗"}],
        stream=True
    )

    print("\n回复: ", end="")
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)

    print("\n[完成]")


def claude_stream():
    """Claude 流式调用"""
    print("\n" + "=" * 60)
    print("【Claude 流式输出】")
    print("=" * 60)

    import anthropic

    client = anthropic.Anthropic()

    print("\n回复: ", end="")

    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": "写一首关于春天的诗"}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n[完成]")


def deepseek_stream():
    """DeepSeek 流式调用（OpenAI 兼容）"""
    print("\n" + "=" * 60)
    print("【DeepSeek 流式输出】")
    print("=" * 60)

    from openai import OpenAI

    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )

    stream = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "写一首关于春天的诗"}],
        stream=True
    )

    print("\n回复: ", end="")
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print("\n[完成]")


def qwen_stream():
    """通义千问流式调用（OpenAI 兼容）"""
    print("\n" + "=" * 60)
    print("【通义千问 流式输出】")
    print("=" * 60)

    from openai import OpenAI

    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    stream = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": "写一首关于春天的诗"}],
        stream=True
    )

    print("\n回复: ", end="")
    for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print("\n[完成]")


if __name__ == "__main__":
    # 测试可用的模型
    if os.getenv("OPENAI_API_KEY"):
        openai_stream()

    if os.getenv("ANTHROPIC_API_KEY"):
        claude_stream()

    if os.getenv("DEEPSEEK_API_KEY"):
        deepseek_stream()

    if os.getenv("DASHSCOPE_API_KEY"):
        qwen_stream()

    if not any([
        os.getenv("OPENAI_API_KEY"),
        os.getenv("ANTHROPIC_API_KEY"),
        os.getenv("DEEPSEEK_API_KEY"),
        os.getenv("DASHSCOPE_API_KEY")
    ]):
        print("未配置任何 API Key，请在 .env 文件中配置")
