"""
03_parallel_tool_calls.py
并行工具调用示例

演示模型同时调用多个工具的场景
"""
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# 定义多个工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取城市天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取城市当前时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_air_quality",
            "description": "获取城市空气质量",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名"}
                },
                "required": ["city"]
            }
        }
    }
]


def execute_tool(name: str, args: dict) -> str:
    """执行工具并返回结果"""
    if name == "get_weather":
        result = {"temp": 25, "weather": "晴", "humidity": 50}
    elif name == "get_time":
        from datetime import datetime
        result = {"time": datetime.now().strftime("%H:%M:%S"), "timezone": "UTC+8"}
    elif name == "get_air_quality":
        result = {"aqi": 65, "level": "良", "pm25": 45}
    else:
        result = {"error": f"未知工具: {name}"}

    return json.dumps(result, ensure_ascii=False)


def chat_with_parallel_tools(user_message: str) -> str:
    """支持并行工具调用的聊天"""
    print(f"\n{'='*60}")
    print(f"用户: {user_message}")
    print("="*60)

    messages = [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        parallel_tool_calls=True  # 允许并行调用（默认开启）
    )

    assistant_message = response.choices[0].message

    if assistant_message.tool_calls:
        tool_count = len(assistant_message.tool_calls)
        print(f"\n[并行调用 {tool_count} 个工具]")

        messages.append(assistant_message)

        # 处理所有工具调用
        for i, tool_call in enumerate(assistant_message.tool_calls, 1):
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            print(f"\n  工具 {i}: {name}")
            print(f"  参数: {args}")

            result = execute_tool(name, args)
            print(f"  结果: {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        # 生成最终回复
        print("\n[生成最终回复]")
        final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )

        final_content = final.choices[0].message.content
        print(f"\nAI: {final_content}")
        return final_content

    print(f"\nAI: {assistant_message.content}")
    return assistant_message.content


def demo_tool_choice():
    """演示 tool_choice 参数"""
    print("\n" + "=" * 60)
    print("【tool_choice 参数演示】")
    print("=" * 60)

    message = "你好"
    messages = [{"role": "user", "content": message}]

    # auto（默认）：模型自己决定
    print("\n1. tool_choice='auto' - 模型自己决定")
    r1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    print(f"   tool_calls: {r1.choices[0].message.tool_calls is not None}")

    # none：禁止使用工具
    print("\n2. tool_choice='none' - 禁止使用工具")
    r2 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "北京天气怎么样"}],
        tools=tools,
        tool_choice="none"
    )
    print(f"   tool_calls: {r2.choices[0].message.tool_calls is not None}")
    print(f"   content: {r2.choices[0].message.content[:50]}...")

    # required：必须使用工具
    print("\n3. tool_choice='required' - 必须使用工具")
    r3 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="required"
    )
    print(f"   tool_calls: {r3.choices[0].message.tool_calls is not None}")

    # 指定工具：强制使用特定工具
    print("\n4. tool_choice={function} - 强制使用特定工具")
    r4 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_weather"}}
    )
    print(f"   tool_calls: {r4.choices[0].message.tool_calls[0].function.name}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("未设置 OPENAI_API_KEY")
        exit()

    print("=" * 60)
    print("【并行工具调用演示】")
    print("=" * 60)

    # 测试并行调用
    chat_with_parallel_tools("北京现在几点了？天气怎么样？空气质量如何？")

    # 演示 tool_choice
    demo_tool_choice()
