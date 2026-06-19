"""
04_multi_turn_chat.py
多轮对话示例

演示如何维护对话历史，实现连续对话
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def simple_multi_turn():
    """简单的多轮对话演示"""
    print("=" * 60)
    print("【演示】多轮对话 - 模型记住上下文")
    print("=" * 60)

    # 维护对话历史
    conversation = [
        {"role": "system", "content": "你是一个友好的助手，回答简洁。"}
    ]

    def chat(user_input: str) -> str:
        # 添加用户消息
        conversation.append({"role": "user", "content": user_input})

        # 调用API（传入完整历史）
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation,
            temperature=0.7
        )

        # 提取回复
        assistant_message = response.choices[0].message.content

        # 将回复加入历史（重要！否则下一轮对话模型不知道自己说过什么）
        conversation.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    # 模拟多轮对话
    exchanges = [
        "你好，我叫小明",
        "我今年25岁，是一名程序员",
        "你还记得我叫什么名字吗？",
        "我的职业是什么？"
    ]

    for user_msg in exchanges:
        print(f"\n用户: {user_msg}")
        response = chat(user_msg)
        print(f"AI: {response}")

    # 打印完整对话历史
    print("\n" + "=" * 60)
    print("【对话历史记录】")
    print("=" * 60)
    for msg in conversation:
        role = msg["role"].upper()
        content = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
        print(f"[{role}] {content}")


def context_length_management():
    """上下文长度管理示例"""
    print("\n" + "=" * 60)
    print("【演示】上下文长度管理")
    print("=" * 60)

    def manage_context(messages: list, max_messages: int = 10) -> list:
        """
        保留系统提示 + 最近的N条消息

        Args:
            messages: 完整消息列表
            max_messages: 保留的最大消息数（不含系统消息）
        """
        # 分离系统消息和其他消息
        system_msgs = [m for m in messages if m["role"] == "system"]
        other_msgs = [m for m in messages if m["role"] != "system"]

        # 只保留最近的 max_messages 条
        if len(other_msgs) > max_messages:
            other_msgs = other_msgs[-max_messages:]
            print(f"  ⚠️ 消息过多，裁剪为最近 {max_messages} 条")

        return system_msgs + other_msgs

    # 模拟长对话
    conversation = [
        {"role": "system", "content": "你是助手"},
    ]

    # 添加15轮对话
    for i in range(15):
        conversation.append({"role": "user", "content": f"问题{i+1}"})
        conversation.append({"role": "assistant", "content": f"回答{i+1}"})

    print(f"原始消息数: {len(conversation)}")

    # 裁剪
    managed = manage_context(conversation, max_messages=6)
    print(f"裁剪后消息数: {len(managed)}")
    print("\n保留的消息:")
    for msg in managed:
        print(f"  [{msg['role']}] {msg['content']}")


class ChatBot:
    """完整的聊天机器人类"""

    def __init__(
        self,
        system_prompt: str = "你是一个有帮助的助手",
        model: str = "gpt-4o-mini",
        max_history: int = 20
    ):
        self.client = OpenAI()
        self.model = model
        self.max_history = max_history
        self.conversation = [{"role": "system", "content": system_prompt}]

    def chat(self, user_input: str) -> str:
        """发送消息并获取回复"""
        self.conversation.append({"role": "user", "content": user_input})

        # 管理上下文长度
        self._manage_context()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation,
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": reply})

        return reply

    def _manage_context(self):
        """管理对话历史长度"""
        system_msg = self.conversation[0]
        other_msgs = self.conversation[1:]

        if len(other_msgs) > self.max_history:
            self.conversation = [system_msg] + other_msgs[-self.max_history:]

    def clear_history(self):
        """清空对话历史，保留系统提示"""
        self.conversation = [self.conversation[0]]

    def get_history(self) -> list:
        """获取对话历史"""
        return self.conversation.copy()


def interactive_chat():
    """交互式聊天演示"""
    print("\n" + "=" * 60)
    print("【交互式聊天】")
    print("=" * 60)
    print("输入 'quit' 退出, 'clear' 清空历史, 'history' 查看历史\n")

    bot = ChatBot("你是一个Python编程专家，回答简洁专业。")

    while True:
        try:
            user_input = input("你: ").strip()
        except KeyboardInterrupt:
            print("\n再见！")
            break

        if not user_input:
            continue
        elif user_input.lower() == 'quit':
            print("再见！")
            break
        elif user_input.lower() == 'clear':
            bot.clear_history()
            print("对话历史已清空\n")
            continue
        elif user_input.lower() == 'history':
            print("\n--- 对话历史 ---")
            for msg in bot.get_history():
                print(f"[{msg['role']}] {msg['content'][:100]}")
            print("--- 结束 ---\n")
            continue

        response = bot.chat(user_input)
        print(f"AI: {response}\n")


if __name__ == "__main__":
    simple_multi_turn()
    context_length_management()

    # 取消下面的注释以启动交互式聊天
    # interactive_chat()
