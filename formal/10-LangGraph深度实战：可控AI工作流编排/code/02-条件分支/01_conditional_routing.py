"""
01_conditional_routing.py
条件路由
"""
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


class State(TypedDict):
    input: str
    category: str
    output: str


def classify(state: State) -> dict:
    """分类"""
    text = state["input"].lower()

    if "天气" in text:
        category = "weather"
    elif "计算" in text:
        category = "math"
    else:
        category = "general"

    return {"category": category}


def handle_weather(state: State) -> dict:
    return {"output": f"[天气] 处理: {state['input']}"}


def handle_math(state: State) -> dict:
    return {"output": f"[数学] 处理: {state['input']}"}


def handle_general(state: State) -> dict:
    return {"output": f"[一般] 处理: {state['input']}"}


def route(state: State) -> Literal["weather", "math", "general"]:
    """路由函数"""
    return state["category"]


def main():
    """主函数"""
    print("=" * 60)
    print("【条件路由】")
    print("=" * 60)

    workflow = StateGraph(State)

    workflow.add_node("classify", classify)
    workflow.add_node("weather", handle_weather)
    workflow.add_node("math", handle_math)
    workflow.add_node("general", handle_general)

    workflow.set_entry_point("classify")

    workflow.add_conditional_edges(
        "classify",
        route,
        {
            "weather": "weather",
            "math": "math",
            "general": "general"
        }
    )

    workflow.add_edge("weather", END)
    workflow.add_edge("math", END)
    workflow.add_edge("general", END)

    app = workflow.compile()

    # 测试
    test_inputs = [
        "今天天气怎么样",
        "计算 1+1",
        "你好",
    ]

    for text in test_inputs:
        print(f"\n输入: {text}")
        result = app.invoke({
            "input": text,
            "category": "",
            "output": ""
        })
        print(f"分类: {result['category']}")
        print(f"输出: {result['output']}")


if __name__ == "__main__":
    main()
