"""
04_multi_tool_agent.py
多工具 Agent 实战

实现一个具有多种能力的 Agent
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# 定义多个工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前时间。当用户询问现在几点或当前时间时使用。",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算。当用户需要计算数学表达式时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如：2+3*4、sqrt(16)、15%4"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "搜索知识库。当用户询问特定领域知识时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "category": {
                        "type": "string",
                        "enum": ["tech", "science", "history", "general"],
                        "description": "知识分类"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取天气信息。当用户询问某地天气时使用。",
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


def execute_function(name: str, args: dict) -> str:
    """执行工具函数"""
    if name == "get_current_time":
        result = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()],
            "timezone": "UTC+8"
        }

    elif name == "calculate":
        try:
            import math
            safe_dict = {
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow,
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
                "tan": math.tan, "log": math.log, "log10": math.log10,
                "pi": math.pi, "e": math.e
            }
            expression = args["expression"]
            calc_result = eval(expression, {"__builtins__": {}}, safe_dict)
            result = {"expression": expression, "result": calc_result}
        except Exception as e:
            result = {"error": f"计算错误: {str(e)}"}

    elif name == "search_knowledge":
        knowledge_db = {
            "Python": "Python是一种解释型、高级编程语言，以简洁易读著称。",
            "机器学习": "机器学习是人工智能的子领域，让计算机从数据中学习。",
            "深度学习": "深度学习使用多层神经网络处理复杂的模式识别任务。",
            "大模型": "大语言模型(LLM)是基于Transformer架构的大规模神经网络。"
        }
        query = args["query"]
        results = [
            {"title": k, "content": v}
            for k, v in knowledge_db.items()
            if query.lower() in k.lower() or query.lower() in v.lower()
        ]
        result = {"query": query, "results": results if results else [{"title": "无结果", "content": "未找到相关内容"}]}

    elif name == "get_weather":
        city = args["city"]
        weather_db = {
            "北京": {"temp": 22, "weather": "晴", "humidity": 45},
            "上海": {"temp": 26, "weather": "多云", "humidity": 60},
            "广州": {"temp": 30, "weather": "雨", "humidity": 80},
        }
        result = weather_db.get(city, {"city": city, "error": "未找到该城市的天气数据"})
        result["city"] = city

    else:
        result = {"error": f"未知工具: {name}"}

    return json.dumps(result, ensure_ascii=False)


class MultiToolAgent:
    """多工具 Agent"""

    def __init__(self, system_prompt: str = None):
        self.messages: List[Dict[str, Any]] = []
        self.max_tool_iterations = 5  # 防止无限循环

        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
        else:
            self.messages.append({
                "role": "system",
                "content": "你是一个智能助手，可以查询时间、计算数学表达式、搜索知识库和查询天气。请根据用户的问题选择合适的工具来回答。"
            })

    def chat(self, user_input: str) -> str:
        """处理用户输入并返回响应"""
        self.messages.append({"role": "user", "content": user_input})

        iteration = 0
        while iteration < self.max_tool_iterations:
            iteration += 1

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages,
                tools=tools
            )

            assistant_message = response.choices[0].message

            if assistant_message.tool_calls:
                self.messages.append(assistant_message)

                for tool_call in assistant_message.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)

                    print(f"  [调用工具] {name}({args})")
                    result = execute_function(name, args)
                    print(f"  [工具结果] {result[:100]}...")

                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
            else:
                self.messages.append(assistant_message)
                return assistant_message.content

        return "[错误] 工具调用次数超过限制"

    def clear_history(self):
        """清空对话历史（保留系统提示）"""
        system_msg = self.messages[0] if self.messages and self.messages[0]["role"] == "system" else None
        self.messages = [system_msg] if system_msg else []


def interactive_demo():
    """交互式演示"""
    print("\n" + "=" * 60)
    print("【交互式多工具 Agent】")
    print("=" * 60)
    print("\n可用能力：时间查询、数学计算、知识搜索、天气查询")
    print("输入 'quit' 退出，输入 'clear' 清空历史\n")

    agent = MultiToolAgent()

    while True:
        try:
            user_input = input("你: ").strip()
        except KeyboardInterrupt:
            print("\n退出")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "clear":
            agent.clear_history()
            print("[历史已清空]\n")
            continue

        response = agent.chat(user_input)
        print(f"\nAI: {response}\n")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("未设置 OPENAI_API_KEY")
        exit()

    print("=" * 60)
    print("【多工具 Agent 演示】")
    print("=" * 60)

    # 自动演示
    agent = MultiToolAgent()

    test_questions = [
        "现在几点了？",
        "计算 (15 + 27) * 3 - 10",
        "帮我搜索一下机器学习相关的知识",
        "北京今天天气怎么样？",
        "sqrt(144) + 10 等于多少？"
    ]

    for q in test_questions:
        print(f"\n{'='*50}")
        print(f"用户: {q}")
        response = agent.chat(q)
        print(f"\nAI: {response}")

    # 取消注释以启用交互模式
    # interactive_demo()
