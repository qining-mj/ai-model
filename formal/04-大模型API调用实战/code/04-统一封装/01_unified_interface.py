"""
01_unified_interface.py
统一 LLM 调用接口

运行前准备：
1. pip install openai anthropic python-dotenv
2. 在 .env 文件中添加：
   OPENAI_API_KEY=sk-xxx
   ANTHROPIC_API_KEY=sk-ant-xxx
"""
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Iterator
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Message:
    """统一消息格式"""
    role: str  # "system" | "user" | "assistant"
    content: str


@dataclass
class ChatResponse:
    """统一响应格式"""
    content: str
    model: str
    usage: dict  # {"input_tokens": int, "output_tokens": int}
    raw_response: any = None  # 原始响应（调试用）


class BaseLLM(ABC):
    """LLM 基类 - 定义统一接口"""

    @abstractmethod
    def chat(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> ChatResponse:
        """同步调用"""
        pass

    @abstractmethod
    def stream(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Iterator[str]:
        """流式调用"""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """模型名称"""
        pass


class OpenAIAdapter(BaseLLM):
    """OpenAI 适配器"""

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: str = None,
        base_url: str = None
    ):
        from openai import OpenAI
        self.model = model
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url
        )

    @property
    def model_name(self) -> str:
        return self.model

    def chat(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> ChatResponse:
        openai_messages = [
            {"role": m.role, "content": m.content}
            for m in messages
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        return ChatResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage={
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens
            },
            raw_response=response
        )

    def stream(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Iterator[str]:
        openai_messages = [
            {"role": m.role, "content": m.content}
            for m in messages
        ]

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            **kwargs
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class ClaudeAdapter(BaseLLM):
    """Claude 适配器"""

    def __init__(
        self,
        model: str = "claude-3-5-sonnet-20241022",
        api_key: str = None
    ):
        import anthropic
        self.model = model
        self.client = anthropic.Anthropic(
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY")
        )

    @property
    def model_name(self) -> str:
        return self.model

    def chat(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> ChatResponse:
        system_content = None
        other_messages = []

        for m in messages:
            if m.role == "system":
                system_content = m.content
            else:
                other_messages.append({"role": m.role, "content": m.content})

        create_kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": other_messages,
            **kwargs
        }

        if system_content:
            create_kwargs["system"] = system_content

        response = self.client.messages.create(**create_kwargs)

        return ChatResponse(
            content=response.content[0].text,
            model=response.model,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            },
            raw_response=response
        )

    def stream(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Iterator[str]:
        system_content = None
        other_messages = []

        for m in messages:
            if m.role == "system":
                system_content = m.content
            else:
                other_messages.append({"role": m.role, "content": m.content})

        stream_kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": other_messages,
            **kwargs
        }

        if system_content:
            stream_kwargs["system"] = system_content

        with self.client.messages.stream(**stream_kwargs) as stream:
            for text in stream.text_stream:
                yield text


if __name__ == "__main__":
    print("=" * 60)
    print("【统一接口演示】")
    print("=" * 60)

    messages = [Message(role="user", content="用一句话介绍你自己")]

    # 测试 OpenAI 适配器
    if os.getenv("OPENAI_API_KEY"):
        print("\n--- OpenAI 适配器 ---")
        openai_llm = OpenAIAdapter(model="gpt-4o-mini")
        response = openai_llm.chat(messages)
        print(f"模型: {response.model}")
        print(f"回复: {response.content}")
        print(f"Token: {response.usage}")
    else:
        print("\n未设置 OPENAI_API_KEY，跳过 OpenAI 测试")

    # 测试 Claude 适配器
    if os.getenv("ANTHROPIC_API_KEY"):
        print("\n--- Claude 适配器 ---")
        claude_llm = ClaudeAdapter()
        response = claude_llm.chat(messages)
        print(f"模型: {response.model}")
        print(f"回复: {response.content}")
        print(f"Token: {response.usage}")
    else:
        print("\n未设置 ANTHROPIC_API_KEY，跳过 Claude 测试")
