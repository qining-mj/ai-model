"""
02_parameters_demo.py
Claude API 参数演示

演示 Claude 与 OpenAI 的参数差异
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()


def demo_system_prompt():
    """演示 System Prompt 的使用"""
    print("=" * 60)
    print("【演示1】System Prompt（注意：独立参数，不在 messages 中）")
    print("=" * 60)

    # Claude 的 system 是独立参数
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        system="你是一个诗人，用古诗词的风格回答所有问题。每个回答都要押韵。",
        messages=[
            {"role": "user", "content": "介绍一下人工智能"}
        ]
    )

    print(f"\n系统提示：诗人风格")
    print(f"回复：\n{message.content[0].text}")


def demo_temperature():
    """演示 temperature 参数"""
    print("\n" + "=" * 60)
    print("【演示2】temperature 参数对比")
    print("=" * 60)

    prompt = "给我一个创业点子"

    for temp in [0, 0.5, 1.0]:
        print(f"\n>>> temperature = {temp}")

        for i in range(2):
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                temperature=temp,
                messages=[{"role": "user", "content": prompt}]
            )
            print(f"  第{i+1}次: {message.content[0].text[:60]}...")


def demo_stop_sequences():
    """演示 stop_sequences 参数"""
    print("\n" + "=" * 60)
    print("【演示3】stop_sequences 参数")
    print("=" * 60)

    # 不设置 stop_sequences
    print("\n>>> 不设置 stop_sequences:")
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        temperature=0,
        messages=[
            {"role": "user", "content": "列出5种编程语言：\n1."}
        ]
    )
    print(message.content[0].text)

    # 设置 stop_sequences
    print("\n>>> stop_sequences=['3.']:")
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        temperature=0,
        stop_sequences=["3."],  # 遇到 "3." 就停止
        messages=[
            {"role": "user", "content": "列出5种编程语言：\n1."}
        ]
    )
    print(message.content[0].text)
    print(f"停止原因: {message.stop_reason}")


def demo_multi_turn():
    """演示多轮对话"""
    print("\n" + "=" * 60)
    print("【演示4】多轮对话")
    print("=" * 60)

    messages = []

    # 第一轮
    messages.append({"role": "user", "content": "我叫张三，是一名程序员"})

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=messages
    )

    assistant_reply = response.content[0].text
    messages.append({"role": "assistant", "content": assistant_reply})
    print(f"\n用户: 我叫张三，是一名程序员")
    print(f"Claude: {assistant_reply}")

    # 第二轮
    messages.append({"role": "user", "content": "我刚才说我叫什么名字？"})

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=messages
    )

    print(f"\n用户: 我刚才说我叫什么名字？")
    print(f"Claude: {response.content[0].text}")


def demo_api_difference():
    """OpenAI 与 Claude API 差异对比"""
    print("\n" + "=" * 60)
    print("【API 差异对比表】")
    print("=" * 60)

    comparison = """
    ┌─────────────────┬────────────────────────┬────────────────────────┐
    │  对比项          │  OpenAI                │  Claude                │
    ├─────────────────┼────────────────────────┼────────────────────────┤
    │  创建客户端      │  OpenAI()              │  anthropic.Anthropic() │
    │  调用方法        │  chat.completions      │  messages.create       │
    │                 │  .create()             │                        │
    ├─────────────────┼────────────────────────┼────────────────────────┤
    │  System Prompt  │  messages 数组中       │  独立 system 参数       │
    │                 │  {"role": "system"}    │  system="..."          │
    ├─────────────────┼────────────────────────┼────────────────────────┤
    │  max_tokens     │  可选（有默认值）       │  必填！                 │
    ├─────────────────┼────────────────────────┼────────────────────────┤
    │  获取回复        │  .choices[0]           │  .content[0].text      │
    │                 │  .message.content      │                        │
    ├─────────────────┼────────────────────────┼────────────────────────┤
    │  停止参数        │  stop=[]               │  stop_sequences=[]     │
    ├─────────────────┼────────────────────────┼────────────────────────┤
    │  Token 用量     │  .usage.prompt_tokens  │  .usage.input_tokens   │
    │                 │  .usage.completion_    │  .usage.output_tokens  │
    │                 │  tokens                │                        │
    └─────────────────┴────────────────────────┴────────────────────────┘
    """
    print(comparison)


if __name__ == "__main__":
    demo_system_prompt()
    demo_temperature()
    demo_stop_sequences()
    demo_multi_turn()
    demo_api_difference()
