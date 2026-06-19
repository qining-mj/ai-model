"""
01_basic_agent.py
基础 Agent 实现
"""
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """计算数学表达式。输入一个数学表达式字符串，返回计算结果。"""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"


@tool
def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def search_info(query: str) -> str:
    """搜索信息"""
    knowledge = {
        "python": "Python 是一种高级编程语言",
        "langchain": "LangChain 是 LLM 应用开发框架",
        "agent": "Agent 是自主决策的 AI 系统",
    }

    for key, value in knowledge.items():
        if key in query.lower():
            return value

    return f"未找到关于 '{query}' 的信息"


def basic_agent():
    """基础 Agent 示例"""
    print("=" * 60)
    print("【基础 Agent 示例】")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    tools = [calculator, get_current_time, search_info]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个有用的助手，可以使用工具来帮助用户解决问题。"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5
    )

    questions = [
        "现在几点了？",
        "计算 (123 + 456) * 2 的结果",
        "什么是 Python？",
        "先告诉我现在的时间，然后计算 100 的平方",
    ]

    for q in questions:
        print(f"\n问题: {q}")
        print("-" * 40)
        result = agent_executor.invoke({"input": q})
        print(f"答案: {result['output']}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    basic_agent()
