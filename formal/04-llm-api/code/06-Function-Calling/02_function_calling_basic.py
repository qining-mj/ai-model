"""
02_function_calling_basic.py
Function Calling 完整流程

演示如何实现完整的工具调用循环
"""
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# 1. 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气。当用户询问某个城市的天气时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京"
                    }
                },
                "required": ["city"]
            }
        }
    }
]


# 2. 实现工具函数
def get_weather(city: str) -> dict:
    """实际的天气查询函数（模拟）"""
    weather_data = {
        "北京": {"temp": 22, "weather": "晴", "humidity": 45, "wind": "北风3级"},
        "上海": {"temp": 26, "weather": "多云", "humidity": 60, "wind": "东风2级"},
        "广州": {"temp": 30, "weather": "雨", "humidity": 80, "wind": "南风4级"},
        "深圳": {"temp": 28, "weather": "阴", "humidity": 70, "wind": "东南风2级"},
    }
    return weather_data.get(city, {"error": f"未找到城市: {city}"})


def process_tool_call(tool_call) -> str:
    """处理工具调用"""
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"  [执行工具] {name}")
    print(f"  [参数] {args}")

    if name == "get_weather":
        result = get_weather(args["city"])
    else:
        result = {"error": f"未知工具: {name}"}

    result_str = json.dumps(result, ensure_ascii=False)
    print(f"  [结果] {result_str}")

    return result_str


# 3. 完整调用流程
def chat_with_tools(user_message: str) -> str:
    """带工具的聊天"""
    print(f"\n{'='*50}")
    print(f"用户: {user_message}")
    print("="*50)

    messages = [{"role": "user", "content": user_message}]

    # 第一次调用：让模型决定是否使用工具
    print("\n[第一次调用 LLM]")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )

    assistant_message = response.choices[0].message
    print(f"[模型响应] finish_reason={response.choices[0].finish_reason}")

    # 检查是否需要调用工具
    if assistant_message.tool_calls:
        print(f"\n[模型决定调用 {len(assistant_message.tool_calls)} 个工具]")

        # 将助手消息加入历史
        messages.append(assistant_message)

        # 处理每个工具调用
        for tool_call in assistant_message.tool_calls:
            result = process_tool_call(tool_call)

            # 将工具结果加入消息
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        # 第二次调用：让模型基于工具结果生成最终回复
        print("\n[第二次调用 LLM]")
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )

        final_content = final_response.choices[0].message.content
        print(f"\nAI: {final_content}")
        return final_content
    else:
        # 不需要工具，直接返回
        print("\n[无需工具调用]")
        print(f"\nAI: {assistant_message.content}")
        return assistant_message.content


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("未设置 OPENAI_API_KEY")
        exit()

    print("=" * 60)
    print("【Function Calling 基础演示】")
    print("=" * 60)

    # 测试需要工具的问题
    chat_with_tools("北京今天天气怎么样？")

    # 测试不需要工具的问题
    chat_with_tools("你好，介绍一下你自己")

    # 测试未知城市
    chat_with_tools("纽约的天气如何？")
