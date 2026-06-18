"""
01_human_approval.py
人工审批
"""
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


class State(TypedDict):
    task: str
    proposal: str
    approved: bool
    result: str


def generate_proposal(state: State) -> dict:
    """生成方案"""
    proposal = f"针对 '{state['task']}' 的执行方案"
    print(f"\n[AI] 生成方案: {proposal}")
    return {"proposal": proposal}


def wait_approval(state: State) -> dict:
    """等待审批"""
    print("\n[系统] 等待人工审批...")
    return {}


def process_result(state: State) -> dict:
    """处理结果"""
    if state["approved"]:
        return {"result": f"已批准执行: {state['proposal']}"}
    else:
        return {"result": "方案被拒绝"}


def main():
    """主函数"""
    print("=" * 60)
    print("【人工审批】")
    print("=" * 60)

    workflow = StateGraph(State)

    workflow.add_node("generate", generate_proposal)
    workflow.add_node("wait", wait_approval)
    workflow.add_node("process", process_result)

    workflow.set_entry_point("generate")
    workflow.add_edge("generate", "wait")
    workflow.add_edge("wait", "process")
    workflow.add_edge("process", END)

    memory = MemorySaver()
    app = workflow.compile(
        checkpointer=memory,
        interrupt_after=["wait"]
    )

    config = {"configurable": {"thread_id": "approval-1"}}

    # 阶段1: 生成方案
    print("\n=== 阶段1: 生成方案 ===")
    result = app.invoke({
        "task": "开发新功能",
        "proposal": "",
        "approved": False,
        "result": ""
    }, config)

    # 阶段2: 人工审批
    print("\n=== 阶段2: 人工审批 ===")
    user_input = input("批准? (y/n): ").strip().lower()
    approved = user_input == 'y'

    app.update_state(config, {"approved": approved})

    # 阶段3: 处理结果
    print("\n=== 阶段3: 处理结果 ===")
    result = app.invoke(None, config)
    print(f"\n结果: {result['result']}")


if __name__ == "__main__":
    main()
