"""
01_loop_workflow.py
循环工作流
"""
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END


class State(TypedDict):
    count: int
    max_count: int
    history: list


def increment(state: State) -> dict:
    """增加计数"""
    new_count = state["count"] + 1
    history = state["history"] + [f"count={new_count}"]
    print(f"  迭代: count = {new_count}")
    return {"count": new_count, "history": history}


def should_continue(state: State) -> Literal["continue", "end"]:
    """检查是否继续"""
    if state["count"] < state["max_count"]:
        return "continue"
    return "end"


def main():
    """主函数"""
    print("=" * 60)
    print("【循环工作流】")
    print("=" * 60)

    workflow = StateGraph(State)

    workflow.add_node("increment", increment)
    workflow.set_entry_point("increment")

    workflow.add_conditional_edges(
        "increment",
        should_continue,
        {
            "continue": "increment",
            "end": END
        }
    )

    app = workflow.compile()

    print("\n执行循环 (max=5):")
    result = app.invoke({
        "count": 0,
        "max_count": 5,
        "history": []
    })

    print(f"\n最终状态:")
    print(f"  count: {result['count']}")
    print(f"  history: {result['history']}")


if __name__ == "__main__":
    main()
