import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 03_manual_tool_call.py
# 手动执行工具调用流程（理解 Agent 内部原理）
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# 导入工具
import sys
sys.path.insert(0, os.path.dirname(__file__))
from define_tools import get_weather, calculator

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)

tools = [get_weather, calculator]
tools_map = {t.name: t for t in tools}
llm_with_tools = llm.bind_tools(tools)

# 手动执行循环
query = "北京天气怎么样？帮我算一下 25 * 1.8 + 32"
messages = [HumanMessage(content=query)]

print(f"Q: {query}\n")
print("=== Agent 执行流程 ===")

for step in range(3):  # 最多 3 步
    print(f"\n--- Step {step + 1} ---")

    # LLM 推理
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    # 如果没有工具调用 → 结束
    if not ai_msg.tool_calls:
        print(f"最终回复: {ai_msg.content}")
        break

    # 执行工具调用
    for tool_call in ai_msg.tool_calls:
        name = tool_call["name"]
        args = tool_call["args"]
        print(f"调用工具: {name}({args})")

        tool = tools_map.get(name)
        if tool:
            result = tool.invoke(args)
        else:
            result = f"未知工具: {name}"

        print(f"工具返回: {result}")
        messages.append(ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"],
        ))
