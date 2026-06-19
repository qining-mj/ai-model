"""
04_async_stream.py
异步流式调用示例

演示使用异步方式进行流式调用，支持取消操作
"""
import os
import asyncio
from typing import AsyncIterator
from dotenv import load_dotenv

load_dotenv()


async def async_stream(message: str, model: str = "gpt-4o-mini") -> AsyncIterator[str]:
    """
    异步流式调用

    Args:
        message: 用户消息
        model: 模型名称

    Yields:
        流式输出的文本片段
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI()

    stream = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message}],
        stream=True
    )

    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content


async def async_stream_with_cancel(
    message: str,
    cancel_event: asyncio.Event
) -> AsyncIterator[str]:
    """
    支持取消的异步流式调用

    Args:
        message: 用户消息
        cancel_event: 取消事件

    Yields:
        流式输出的文本片段
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI()

    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
        stream=True
    )

    async for chunk in stream:
        # 检查是否需要取消
        if cancel_event.is_set():
            print("\n[用户取消]")
            break

        content = chunk.choices[0].delta.content
        if content:
            yield content


async def parallel_streams(messages: list[str]) -> list[str]:
    """
    并行执行多个流式调用

    Args:
        messages: 消息列表

    Returns:
        响应列表
    """
    async def collect_stream(message: str) -> str:
        result = []
        async for chunk in async_stream(message):
            result.append(chunk)
        return "".join(result)

    # 并行执行所有流式调用
    results = await asyncio.gather(*[
        collect_stream(msg) for msg in messages
    ])

    return results


async def demo_basic():
    """基本异步流式调用"""
    print("=" * 60)
    print("【基本异步流式调用】")
    print("=" * 60)

    print("\n回复: ", end="")
    async for chunk in async_stream("写一句关于编程的话"):
        print(chunk, end="", flush=True)
    print()


async def demo_with_cancel():
    """演示取消功能"""
    print("\n" + "=" * 60)
    print("【支持取消的流式调用】")
    print("=" * 60)

    cancel_event = asyncio.Event()

    async def auto_cancel():
        """3秒后自动取消"""
        await asyncio.sleep(3)
        print("\n[触发取消]")
        cancel_event.set()

    # 启动自动取消任务
    cancel_task = asyncio.create_task(auto_cancel())

    print("\n回复: ", end="")
    async for chunk in async_stream_with_cancel(
        "写一篇500字的文章",
        cancel_event
    ):
        print(chunk, end="", flush=True)

    cancel_task.cancel()
    print()


async def demo_parallel():
    """演示并行调用"""
    print("\n" + "=" * 60)
    print("【并行流式调用】")
    print("=" * 60)

    messages = [
        "用一句话介绍 Python",
        "用一句话介绍 JavaScript",
        "用一句话介绍 Rust"
    ]

    print(f"\n并行发送 {len(messages)} 个请求...")

    import time
    start = time.time()

    results = await parallel_streams(messages)

    elapsed = time.time() - start

    for msg, result in zip(messages, results):
        print(f"\n问: {msg}")
        print(f"答: {result}")

    print(f"\n[并行完成，耗时: {elapsed:.2f}秒]")


async def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("未设置 OPENAI_API_KEY")
        return

    await demo_basic()
    await demo_with_cancel()
    await demo_parallel()


if __name__ == "__main__":
    asyncio.run(main())
