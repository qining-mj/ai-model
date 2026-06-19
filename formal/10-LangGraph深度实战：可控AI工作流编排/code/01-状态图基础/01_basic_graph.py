"""
01_basic_graph.py
基础 LangGraph 示例
"""
from typing import TypedDict
from langgraph.graph import StateGraph, END


class State(TypedDict):
    input: str
    step1_result: str
    step2_result: str
    final_output: str


def step1(state: State) -> dict:
    """步骤1"""
    result = f"[Step1] 处理: {state['input']}"
    print(result)
    return {"step1_result": result}


def step2(state: State) -> dict:
    """步骤2"""
    result = f"[Step2] 基于: {state['step1_result']}"
    print(result)
    return {"step2_result": result}


def final_step(state: State) -> dict:
    """最终步骤"""
    result = f"[Final] 完成: {state['step2_result']}"
    print(result)
    return {"final_output": result}


def main():
    """主函数"""
    print("=" * 60)
    print("【基础 LangGraph 示例】")
    print("=" * 60)

    # 创建图
    workflow = StateGraph(State)

    # 添加节点
    workflow.add_node("step1", step1)
    workflow.add_node("step2", step2)
    workflow.add_node("final", final_step)

    # 设置入口和边
    workflow.set_entry_point("step1")
    workflow.add_edge("step1", "step2")
    workflow.add_edge("step2", "final")
    workflow.add_edge("final", END)

    # 编译
    app = workflow.compile()

    # 运行
    print("\n执行流程:")
    print("-" * 40)

    result = app.invoke({
        "input": "Hello LangGraph",
        "step1_result": "",
        "step2_result": "",
        "final_output": ""
    })

    print(f"\n最终输出: {result['final_output']}")


if __name__ == "__main__":
    main()
