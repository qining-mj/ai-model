"""
01_react_agent.py
ReAct Agent 实现
"""
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool


@tool
def search(query: str) -> str:
    """搜索信息"""
    knowledge = {
        "langchain": "LangChain 是一个用于构建 LLM 应用的框架，支持 Chain 和 Agent。",
        "react": "ReAct 是一种将推理和行动结合的 Agent 模式，交替进行思考和行动。",
        "agent": "Agent 是能够自主决策并执行任务的 AI 系统，可以使用工具。",
        "python": "Python 是一种高级编程语言，语法简洁，广泛用于 AI 开发。",
    }

    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return value

    return f"未找到关于 '{query}' 的信息"


@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {e}"


def react_agent_demo():
    """ReAct Agent 演示"""
    print("=" * 60)
    print("【ReAct Agent 演示】")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [search, calculator]

    # ReAct Prompt
    react_prompt = PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}""")

    agent = create_react_agent(llm, tools, react_prompt)
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )

    questions = [
        "什么是 LangChain？",
        "计算 (50 + 30) * 2 的结果",
        "什么是 Agent？它和 ReAct 有什么关系？",
    ]

    for q in questions:
        print(f"\n{'='*50}")
        print(f"问题: {q}")
        print("=" * 50)
        try:
            result = executor.invoke({"input": q})
            print(f"\n最终答案: {result['output']}")
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    react_agent_demo()
