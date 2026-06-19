"""
05_error_handling.py
错误处理与重试机制

演示如何优雅地处理 API 调用中的各种错误
"""
import os
import time
from dotenv import load_dotenv
from openai import (
    OpenAI,
    APIError,
    APIConnectionError,
    RateLimitError,
    AuthenticationError,
    BadRequestError
)

load_dotenv()


def demo_error_types():
    """演示不同错误类型"""
    print("=" * 60)
    print("【常见错误类型】")
    print("=" * 60)

    errors = """
    ┌──────────────────────┬────────┬────────────────────────────┐
    │  错误类型             │ 状态码 │  常见原因                   │
    ├──────────────────────┼────────┼────────────────────────────┤
    │  AuthenticationError │  401   │  API Key 无效或过期         │
    │  RateLimitError      │  429   │  请求频率超限 / 额度用完     │
    │  BadRequestError     │  400   │  请求参数错误               │
    │  APIConnectionError  │   -    │  网络连接问题               │
    │  InternalServerError │  500   │  OpenAI 服务器错误          │
    └──────────────────────┴────────┴────────────────────────────┘

    处理策略：
    - 401: 检查 API Key 是否正确
    - 429: 等待后重试（指数退避）
    - 400: 检查请求参数
    - 网络错误: 重试
    - 500: 等待后重试
    """
    print(errors)


def safe_chat_basic(client, messages: list) -> str:
    """基础版：简单的 try-except"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"发生错误: {e}")
        return None


def safe_chat_with_retry(
    client,
    messages: list,
    max_retries: int = 3,
    initial_delay: float = 1.0
) -> str:
    """
    进阶版：带指数退避重试的 API 调用

    Args:
        client: OpenAI 客户端
        messages: 消息列表
        max_retries: 最大重试次数
        initial_delay: 初始等待时间（秒）

    Returns:
        模型回复文本，失败返回 None
    """
    delay = initial_delay

    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                timeout=30  # 设置超时时间
            )
            return response.choices[0].message.content

        except AuthenticationError as e:
            # 认证错误，不重试
            print(f"❌ 认证失败: {e.message}")
            print("   请检查 API Key 是否正确")
            return None

        except BadRequestError as e:
            # 请求错误，不重试
            print(f"❌ 请求参数错误: {e.message}")
            return None

        except RateLimitError as e:
            if attempt < max_retries:
                print(f"⚠️ 触发限流，{delay:.1f}秒后重试 (第{attempt+1}次)")
                time.sleep(delay)
                delay *= 2  # 指数退避
            else:
                print(f"❌ 重试{max_retries}次后仍然限流")
                return None

        except APIConnectionError as e:
            if attempt < max_retries:
                print(f"⚠️ 网络错误，{delay:.1f}秒后重试 (第{attempt+1}次)")
                time.sleep(delay)
                delay *= 2
            else:
                print(f"❌ 网络错误，重试{max_retries}次后仍失败")
                return None

        except APIError as e:
            if e.status_code and e.status_code >= 500:
                # 服务器错误，可重试
                if attempt < max_retries:
                    print(f"⚠️ 服务器错误({e.status_code})，{delay:.1f}秒后重试")
                    time.sleep(delay)
                    delay *= 2
                else:
                    print(f"❌ 服务器错误，重试{max_retries}次后仍失败")
                    return None
            else:
                # 其他 API 错误
                print(f"❌ API错误: {e.status_code} - {e.message}")
                return None

    return None


class RobustChatClient:
    """健壮的聊天客户端封装"""

    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        max_retries: int = 3,
        timeout: float = 30.0
    ):
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url=base_url or os.getenv("OPENAI_BASE_URL")
        )
        self.max_retries = max_retries
        self.timeout = timeout

    def chat(
        self,
        messages: list,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        **kwargs
    ) -> dict:
        """
        发送聊天请求

        Returns:
            {
                "success": bool,
                "content": str or None,
                "usage": dict or None,
                "error": str or None
            }
        """
        delay = 1.0

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    timeout=self.timeout,
                    **kwargs
                )

                return {
                    "success": True,
                    "content": response.choices[0].message.content,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    },
                    "error": None
                }

            except (RateLimitError, APIConnectionError) as e:
                if attempt < self.max_retries:
                    time.sleep(delay)
                    delay *= 2
                    continue
                return {
                    "success": False,
                    "content": None,
                    "usage": None,
                    "error": f"重试{self.max_retries}次后失败: {str(e)}"
                }

            except (AuthenticationError, BadRequestError) as e:
                return {
                    "success": False,
                    "content": None,
                    "usage": None,
                    "error": str(e)
                }

            except Exception as e:
                return {
                    "success": False,
                    "content": None,
                    "usage": None,
                    "error": f"未知错误: {str(e)}"
                }

        return {"success": False, "content": None, "usage": None, "error": "未知错误"}


def main():
    """主函数：演示错误处理"""
    demo_error_types()

    print("\n" + "=" * 60)
    print("【演示】正常请求")
    print("=" * 60)

    client = OpenAI()
    messages = [{"role": "user", "content": "你好，请用一句话介绍自己"}]

    # 方式1：简单调用
    print("\n>>> 基础版调用:")
    result = safe_chat_basic(client, messages)
    if result:
        print(f"  回复: {result}")

    # 方式2：带重试调用
    print("\n>>> 带重试版调用:")
    result = safe_chat_with_retry(client, messages)
    if result:
        print(f"  回复: {result}")

    # 方式3：封装类调用
    print("\n>>> 封装类调用:")
    robust_client = RobustChatClient()
    result = robust_client.chat(messages)
    if result["success"]:
        print(f"  回复: {result['content']}")
        print(f"  Token: {result['usage']}")
    else:
        print(f"  错误: {result['error']}")


if __name__ == "__main__":
    main()
