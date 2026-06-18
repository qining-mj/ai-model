"""
multi_agent_system.py
多 Agent 协作系统
"""
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


# ============ 数据结构 ============

@dataclass
class AgentMessage:
    """Agent 消息"""
    sender: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class TaskPlan(BaseModel):
    """任务计划"""
    steps: List[Dict[str, str]] = Field(description="执行步骤列表")


# ============ Agent 基类 ============

class BaseAgent(ABC):
    """Agent 基类"""

    def __init__(
        self,
        name: str,
        role: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7
    ):
        self.name = name
        self.role = role
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.memory: List[AgentMessage] = []

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    def process(self, task: str, context: str = "") -> str:
        """处理任务"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", "任务: {task}\n\n上下文:\n{context}\n\n请完成任务。")
        ])

        chain = prompt | self.llm
        response = chain.invoke({"task": task, "context": context})

        self.memory.append(AgentMessage(
            sender=self.name,
            content=response.content,
            metadata={"task": task}
        ))

        return response.content

    def receive_message(self, message: AgentMessage):
        """接收消息"""
        self.memory.append(message)


# ============ 专业 Agent ============

class WriterAgent(BaseAgent):
    """写作 Agent"""

    def __init__(self):
        super().__init__(name="Writer", role="专业写作者", temperature=0.8)

    def get_system_prompt(self) -> str:
        return """你是一位专业的内容写作者。
擅长：撰写清晰、有条理的文章，适应不同风格。
要求：结构清晰，逻辑连贯，语言流畅。"""


class ReviewerAgent(BaseAgent):
    """审核 Agent"""

    def __init__(self):
        super().__init__(name="Reviewer", role="内容审核者", temperature=0.3)

    def get_system_prompt(self) -> str:
        return """你是一位严格的内容审核者。
职责：检查准确性、发现问题、提供改进建议。
要求：指出具体问题，解释原因，给出建议。"""


class ResearcherAgent(BaseAgent):
    """研究 Agent"""

    def __init__(self):
        super().__init__(name="Researcher", role="研究分析师", temperature=0.5)

    def get_system_prompt(self) -> str:
        return """你是一位资深研究分析师。
擅长：深入分析问题、整理信息、提供洞察。
要求：多角度分析，结构化输出。"""


class CoderAgent(BaseAgent):
    """编程 Agent"""

    def __init__(self):
        super().__init__(name="Coder", role="软件开发者", temperature=0.2)

    def get_system_prompt(self) -> str:
        return """你是一位经验丰富的软件开发者。
擅长：编写高质量代码、设计架构、调试优化。
要求：遵循最佳实践，考虑边界情况。"""


# ============ 协调器 ============

class Coordinator:
    """任务协调器"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.agents: Dict[str, BaseAgent] = {
            "writer": WriterAgent(),
            "reviewer": ReviewerAgent(),
            "researcher": ResearcherAgent(),
            "coder": CoderAgent(),
        }
        self.execution_log: List[Dict] = []

    def plan_task(self, task: str) -> TaskPlan:
        """规划任务"""
        prompt = ChatPromptTemplate.from_template("""
你是任务规划专家。为以下任务制定执行计划。

任务: {task}

可用 Agent:
- writer: 写作内容
- reviewer: 审核内容
- researcher: 研究分析
- coder: 编写代码

返回 JSON 格式:
{{"steps": [{{"agent": "名称", "task": "描述"}}, ...]}}
""")

        structured_llm = self.llm.with_structured_output(TaskPlan)
        chain = prompt | structured_llm

        return chain.invoke({"task": task})

    def execute_plan(self, plan: TaskPlan, task: str) -> Dict[str, Any]:
        """执行计划"""
        results = []
        context = f"原始任务: {task}\n\n"

        print(f"\n执行计划 ({len(plan.steps)} 个步骤):")
        print("-" * 40)

        for i, step in enumerate(plan.steps, 1):
            agent_name = step["agent"]
            step_task = step["task"]

            print(f"\n步骤 {i}: [{agent_name}] {step_task[:40]}...")

            if agent_name not in self.agents:
                print(f"  未知 Agent: {agent_name}，跳过")
                continue

            agent = self.agents[agent_name]
            result = agent.process(step_task, context)

            context += f"\n[{agent_name}输出]:\n{result}\n"

            step_result = {
                "step": i,
                "agent": agent_name,
                "task": step_task,
                "result": result
            }
            results.append(step_result)
            self.execution_log.append(step_result)

            print(f"  完成 ({len(result)} 字符)")

            # 广播消息
            message = AgentMessage(sender=agent_name, content=result)
            for other in self.agents.values():
                if other.name != agent_name:
                    other.receive_message(message)

        return {
            "task": task,
            "results": results,
            "final_output": results[-1]["result"] if results else ""
        }

    def run(self, task: str) -> Dict[str, Any]:
        """运行完整流程"""
        print(f"\n任务: {task}")
        print("=" * 50)

        print("\n规划中...")
        plan = self.plan_task(task)

        print(f"生成 {len(plan.steps)} 个步骤:")
        for i, step in enumerate(plan.steps, 1):
            print(f"  {i}. [{step['agent']}] {step['task'][:35]}...")

        result = self.execute_plan(plan, task)

        print("\n" + "=" * 50)
        print("任务完成!")

        return result


def demo():
    """演示"""
    print("=" * 60)
    print("【多 Agent 协作系统】")
    print("=" * 60)

    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        return

    coordinator = Coordinator()

    # 示例任务
    task = "写一篇关于 Python 异步编程的技术文章，要求有代码示例，并进行质量审核"

    result = coordinator.run(task)

    print("\n" + "=" * 60)
    print("最终输出:")
    print("=" * 60)

    output = result["final_output"]
    if len(output) > 1500:
        print(output[:1500] + "\n\n... (已截断)")
    else:
        print(output)


if __name__ == "__main__":
    demo()
