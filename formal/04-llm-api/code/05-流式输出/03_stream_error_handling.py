"""
03_stream_error_handling.py
流式输出错误处理

演示如何处理流式调用中的各种错误
"""
import os
from typing import Iterator, Optional
from dotenv import load_dotenv
from openai import OpenAI, APIError, APITimeoutError, RateLimitError

load_dotenv()


def stream_with_error_handling(
    message: str,
    model: str = "gpt-4o-mini",
    timeout: int = 30
) -> Iterator[str]:
    """
    带错误处理的流式调用

    Args:
        message: 用户消息
        model: 模型名称
        timeout: 超时时间（秒）

    Yields:
        流式输出的文本片段
    """
    client = OpenAI(timeout=timeout)
    full_content = ""
    chunk_count = 0

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            stream=True
        )

        for chunk in stream:
            chunk_count += 1
            content = chunk.choices[0].delta.content
            if content:
                full_content += content
                yield content

            # 检查是否完成
            if chunk.choices[0].finish_reason:
                print(f"\n[完成原因: {chunk.choices[0].finish_reason}]")

    except APITimeoutError:
        yield f"\n[超时错误: 请求超过 {timeout} 秒]"

    except RateLimitError as e:
        yield f"\n[限流错误: {e.message}]"

    except APIError as e:
        yield f"\n[API 错误: {e.message}]"

    except Exception as e:
        yield f"\n[未知错误: {str(e)}]"

    finally:
        print(f"[统计] 收到 {chunk_count} 个 chunk，共 {len(full_content)} 字符")


def stream_with_retry(
    message: str,
    max_retries: int = 3,
    **kwargs
) -> Iterator[str]:
    """
    带重试的流式调用

    Args:
        message: 用户消息
        max_retries: 最大重试次数
        **kwargs: 传递给 stream_with_error_handling 的参数

    Yields:
        流式输出的文本片段
    """
    import time

    for attempt in range(max_retries):
        try:
            buffer = []
            for chunk in stream_with_error_handling(message, **kwargs):
                buffer.append(chunk)
                yield chunk

            # 如果成功完成，直接返回
            return

        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                yield f"\n[第 {attempt + 1} 次尝试失败，{wait_time} 秒后重试...]\n"
                time.sleep(wait_time)
            else:
                yield f"\n[所有 {max_retries} 次尝试均失败]"
                raise


def stream_with_callback(
    message: str,
    on_chunk: Optional[callable] = None,
    on_complete: Optional[callable] = None,
    on_error: Optional[callable] = None
) -> str:
    """
    带回调的流式调用

    Args:
        message: 用户消息
        on_chunk: 每个 chunk 的回调函数
        on_complete: 完成时的回调函数
        on_error: 错误时的回调函数

    Returns:
        完整的响应内容
    """
    full_content = ""

    try:
        for chunk in stream_with_error_handling(message):
            full_content += chunk

            if on_chunk:
                on_chunk(chunk)

        if on_complete:
            on_complete(full_content)

    except Exception as e:
        if on_error:
            on_error(e)
        raise

    return full_content


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("未设置 OPENAI_API_KEY")
        exit()

    print("=" * 60)
    print("【流式错误处理演示】")
    print("=" * 60)

    # 演示1：基本错误处理
    print("\n--- 基本流式调用（带错误处理）---")
    print("回复: ", end="")
    for chunk in stream_with_error_handling("写一首四行的诗"):
        print(chunk, end="", flush=True)
    print()

    # 演示2：使用回调
    print("\n--- 使用回调函数 ---")


    def on_chunk(text):
        print(f"[chunk] {repr(text)}")


    def on_complete(full):
        print(f"\n[完成] 总长度: {len(full)} 字符")


    stream_with_callback(
        "说一句话",
        on_chunk=on_chunk,
        on_complete=on_complete
    )
