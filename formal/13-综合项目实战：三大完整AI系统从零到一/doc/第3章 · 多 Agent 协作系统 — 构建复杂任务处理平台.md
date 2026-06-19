# 第3章 · 多 Agent 协作系统 — 构建复杂任务处理平台

> **时长**：约 6 小时 ｜ **难度**：⭐⭐⭐⭐⭐ ｜ **类型**：综合实战
>
> **目标**：构建一个多 Agent 协作的复杂任务处理系统

---

## 项目概述

### 功能需求

- 多角色 Agent 协作
- 任务自动分解和分配
- 结果汇总和质量检查
- 支持自定义工作流

### 应用场景

- 内容创作流水线
- 代码审查系统
- 研究报告生成
- 数据分析流程

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    多 Agent 协作系统                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐                                           │
│  │ Coordinator │  ← 任务协调者：分解任务、分配、汇总        │
│  └──────┬──────┘                                           │
│         │                                                   │
│    ┌────┴────┬────────┬────────┐                          │
│    ↓         ↓        ↓        ↓                          │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                      │
│ │Writer│ │Review│ │Search│ │Coder │  ← 专业 Agent         │
│ └──────┘ └──────┘ └──────┘ └──────┘                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 架构流程图

```mermaid
graph TD
  subgraph User["用户请求"]
    TASK[复杂任务描述] --> COORD
  end

  subgraph Planning["规划层"]
    COORD[Coordinator<br/>任务协调器] --> PLAN[LLM 任务规划<br/>步骤分解 + Agent 分配]
    PLAN --> STEPS[执行步骤列表<br/>TaskPlan: steps=[...]]
  end

  subgraph Agents["Agent 执行层"]
    STEPS --> W[WriterAgent<br/>temp=0.8 · 内容写作]
    STEPS --> R[ReviewerAgent<br/>temp=0.3 · 质量审核]
    STEPS --> RS[ResearcherAgent<br/>temp=0.5 · 研究分析]
    STEPS --> C[CoderAgent<br/>temp=0.2 · 代码开发]

    W --> MSG[共享上下文<br/>Agent 间消息广播]
    R --> MSG
    RS --> MSG
    C --> MSG
    MSG --> CTX[累积上下文 context<br/>用于后续步骤参考]
    CTX --> W
    CTX --> R
    CTX --> RS
    CTX --> C
  end

  subgraph Output["输出层"]
    W & R & RS & C --> RESULT[执行结果汇总]
    RESULT --> FINAL[最终输出 + 执行日志]
  end
```

---

## 核心代码

### 1. Agent 基类

**概念定义**：BaseAgent 是所有专业 Agent 的抽象基类，统一了 LLM 调用、消息记录、上下文管理接口。具体 Agent 只需实现 `get_system_prompt()` 定义角色行为，其余能力由基类自动提供——体现了模板方法设计模式。

```python
"""
base_agent.py
Agent 基类
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dataclasses import dataclass


@dataclass
class AgentMessage:
    """Agent 消息"""
    sender: str
    content: str
    metadata: Dict[str, Any] = None


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
        """获取系统提示"""
        pass

    def process(self, task: str, context: str = "") -> str:
        """处理任务"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", """
任务: {task}

上下文信息:
{context}

请完成任务并给出结果。
""")
        ])

        chain = prompt | self.llm
        response = chain.invoke({"task": task, "context": context})

        # 记录消息
        self.memory.append(AgentMessage(
            sender=self.name,
            content=response.content,
            metadata={"task": task}
        ))

        return response.content

    def receive_message(self, message: AgentMessage):
        """接收消息"""
        self.memory.append(message)

    def get_context(self) -> str:
        """获取上下文"""
        return "\n".join([
            f"[{msg.sender}]: {msg.content[:200]}..."
            for msg in self.memory[-5:]
        ])
```

### 2. 专业 Agent

**核心定位**：专业 Agent 模式——每个 Agent 通过不同的 temperature 和系统提示词定义单一职责角色。Writer 偏创意（temp=0.8），Reviewer 偏严谨（temp=0.3），Researcher 偏分析（temp=0.5），Coder 偏精确（temp=0.2）。各司其职，协同完成任务。

```python
"""
specialized_agents.py
专业 Agent
"""
from .base_agent import BaseAgent


class WriterAgent(BaseAgent):
    """写作 Agent"""

    def __init__(self):
        super().__init__(
            name="Writer",
            role="专业写作者",
            temperature=0.8
        )

    def get_system_prompt(self) -> str:
        return """你是一位专业的内容写作者。
你擅长：
- 撰写清晰、有条理的文章
- 根据主题生成高质量内容
- 适应不同的写作风格和语气

写作时请注意：
- 结构清晰，逻辑连贯
- 语言流畅，表达准确
- 根据目标受众调整风格"""


class ReviewerAgent(BaseAgent):
    """审核 Agent"""

    def __init__(self):
        super().__init__(
            name="Reviewer",
            role="内容审核者",
            temperature=0.3
        )

    def get_system_prompt(self) -> str:
        return """你是一位严格的内容审核者。
你的职责：
- 检查内容的准确性和完整性
- 发现逻辑错误和表述问题
- 提供具体的改进建议

审核时请：
- 指出具体问题的位置
- 解释问题的原因
- 给出改进建议"""


class ResearcherAgent(BaseAgent):
    """研究 Agent"""

    def __init__(self):
        super().__init__(
            name="Researcher",
            role="研究分析师",
            temperature=0.5
        )

    def get_system_prompt(self) -> str:
        return """你是一位资深研究分析师。
你擅长：
- 深入分析问题和主题
- 整理和总结信息
- 提供有洞察力的观点

研究时请：
- 多角度分析问题
- 引用相关知识
- 给出结构化的分析结果"""


class CoderAgent(BaseAgent):
    """编程 Agent"""

    def __init__(self):
        super().__init__(
            name="Coder",
            role="软件开发者",
            temperature=0.2
        )

    def get_system_prompt(self) -> str:
        return """你是一位经验丰富的软件开发者。
你擅长：
- 编写高质量的代码
- 设计系统架构
- 调试和优化

编程时请：
- 遵循最佳实践
- 添加必要的注释
- 考虑边界情况"""
```

### 3. 协调器

**概念定义**：任务协调器采用"规划-执行"两阶段模式——先由 LLM 将复杂任务自动分解为可执行的步骤计划（TaskPlan），再按步骤分派给对应 Agent 顺序执行。**核心定位**：协调器是系统的"大脑"，负责任务理解、资源调度和结果汇聚。

```python
"""
coordinator.py
任务协调器
"""
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from .base_agent import BaseAgent, AgentMessage
from .specialized_agents import (
    WriterAgent, ReviewerAgent, ResearcherAgent, CoderAgent
)


class TaskPlan(BaseModel):
    """任务计划"""
    steps: List[Dict[str, str]] = Field(description="执行步骤列表")


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
        available_agents = ", ".join(self.agents.keys())

        prompt = ChatPromptTemplate.from_template("""
你是一个任务规划专家。请为以下任务制定执行计划。

任务: {task}

可用的 Agent: {agents}
- writer: 写作内容
- reviewer: 审核内容
- researcher: 研究分析
- coder: 编写代码

请返回一个执行计划，格式为 JSON:
{{
  "steps": [
    {{"agent": "agent名称", "task": "具体任务描述"}},
    ...
  ]
}}

注意：
1. 合理安排步骤顺序
2. 每个步骤分配给合适的 Agent
3. 考虑步骤之间的依赖关系
""")

        structured_llm = self.llm.with_structured_output(TaskPlan)
        chain = prompt | structured_llm

        return chain.invoke({"task": task, "agents": available_agents})

    def execute_plan(self, plan: TaskPlan, task: str) -> Dict[str, Any]:
        """执行计划"""
        results = []
        context = f"原始任务: {task}\n\n"

        print(f"\n执行计划 ({len(plan.steps)} 个步骤):")
        print("=" * 50)

        for i, step in enumerate(plan.steps, 1):
            agent_name = step["agent"]
            step_task = step["task"]

            print(f"\n步骤 {i}: [{agent_name}] {step_task[:50]}...")

            if agent_name not in self.agents:
                print(f"  ⚠️ 未知 Agent: {agent_name}，跳过")
                continue

            agent = self.agents[agent_name]

            # 执行任务
            result = agent.process(step_task, context)

            # 更新上下文
            context += f"\n[{agent_name}的输出]:\n{result}\n"

            # 记录结果
            step_result = {
                "step": i,
                "agent": agent_name,
                "task": step_task,
                "result": result
            }
            results.append(step_result)
            self.execution_log.append(step_result)

            print(f"  ✓ 完成 ({len(result)} 字符)")

            # 广播消息给其他 Agent
            message = AgentMessage(
                sender=agent_name,
                content=result,
                metadata={"step": i}
            )
            for other_agent in self.agents.values():
                if other_agent.name != agent_name:
                    other_agent.receive_message(message)

        return {
            "task": task,
            "plan": plan.dict(),
            "results": results,
            "final_output": results[-1]["result"] if results else ""
        }

    def run(self, task: str) -> Dict[str, Any]:
        """运行完整流程"""
        print(f"\n任务: {task}")
        print("=" * 50)

        # 规划
        print("\n📋 规划任务...")
        plan = self.plan_task(task)

        print(f"  生成 {len(plan.steps)} 个步骤:")
        for i, step in enumerate(plan.steps, 1):
            print(f"    {i}. [{step['agent']}] {step['task'][:40]}...")

        # 执行
        print("\n🚀 执行计划...")
        result = self.execute_plan(plan, task)

        print("\n✅ 任务完成!")
        return result
```

### 4. 主程序

**概念定义**：主程序作为系统入口，初始化 Coordinator 并传入任务描述。每个 Agent 执行结果通过消息广播同步给其他 Agent，实现信息共享和上下文感知的协作——类似"黑板架构"模式。

```python
"""
main.py
主程序
"""
import os
from coordinator import Coordinator


def main():
    """主函数"""
    print("=" * 60)
    print("【多 Agent 协作系统】")
    print("=" * 60)

    coordinator = Coordinator()

    # 示例任务
    tasks = [
        "写一篇关于人工智能在医疗领域应用的文章，要求有深度分析，并进行质量审核",
        # "设计一个用户登录系统，包含需求分析、代码实现和代码审查",
    ]

    for task in tasks:
        result = coordinator.run(task)

        print("\n" + "=" * 60)
        print("最终输出:")
        print("=" * 60)
        print(result["final_output"][:1000] + "..." if len(result["final_output"]) > 1000 else result["final_output"])


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    main()
```

---

## 高级功能

### 自定义工作流

**概念定义**：自定义工作流模式——在 Coordinator 基础上封装领域特定的流程模板。通过预定义任务 Prompt 结构，将"研究→写作→审核→修改"等通用流水线固化为可复用的工作流类。

```python
"""
custom_workflow.py
自定义工作流
"""
from coordinator import Coordinator


class ContentCreationWorkflow:
    """内容创作工作流"""

    def __init__(self):
        self.coordinator = Coordinator()

    def create_blog_post(self, topic: str) -> dict:
        """创建博客文章"""
        task = f"""
创建一篇关于 "{topic}" 的博客文章：

1. 首先进行主题研究，收集相关信息
2. 根据研究结果，撰写文章初稿
3. 对文章进行审核，提出修改建议
4. 根据建议优化文章

最终输出一篇高质量的博客文章。
"""
        return self.coordinator.run(task)

    def create_technical_doc(self, subject: str) -> dict:
        """创建技术文档"""
        task = f"""
创建关于 "{subject}" 的技术文档：

1. 研究技术细节和最佳实践
2. 撰写技术说明文档
3. 编写示例代码
4. 审核文档和代码的准确性

输出完整的技术文档，包含说明和代码示例。
"""
        return self.coordinator.run(task)


if __name__ == "__main__":
    workflow = ContentCreationWorkflow()

    # 创建博客文章
    result = workflow.create_blog_post("LangChain 入门指南")
    print(result["final_output"])
```

---

## 常见踩坑

1. **Agent 角色定义模糊导致输出混乱**：如果系统提示词描述过于宽泛（如"你是一位助手"），Writer 可能输出技术代码，Coder 可能写散文。必须为每个 Agent 定义明确的职责边界、输出格式约束和具体范例。建议在 prompt 中用"你擅长..."和"你不需要..."正反两方面界定。

2. **任务分解粒度过粗或过细**：Coordinator 的 LLM 规划可能生成 10+ 个微步骤（每步只写一行代码）或仅 1-2 个大步骤（一步要求写整个系统）。建议在规划 prompt 中显式限定步骤数量在 3-6 步，并规定每步必须有明确的产出物描述。

3. **Agent 间上下文截断丢失关键信息**：`get_context()` 仅截取每条消息前 200 字符，若 Agent 在消息后半部分输出关键结论，后续 Agent 无法感知。建议改为按 Token 数截断（保留 2000 Token），或让每个 Agent 在输出末尾主动生成"摘要"供传递。

4. **消息广播导致无限循环**：Reviewer 的修改意见触发 Writer 重新生成，Writer 的新版本再次触发 Reviewer 审核，形成"修改→审核→再修改"的无限循环。Coordinator 中必须设置最大迭代次数（如 2 轮）或变更检测（内容无变化时停止）。

5. **API 调用次数与成本失控**：每个 Agent 独立实例化 ChatOpenAI，4 个 Agent 处理一个任务可能产生 10+ 次 API 请求，Token 消耗远超预期。建议在 Coordinator 中统计每次调用的 Token 用量，设置预算上限，并在 prompt 中要求 Agent 尽量合并输出。

---

## 课后练习

1. **新增 DebuggerAgent**：在 CoderAgent 输出代码后自动执行单元测试，将测试结果反馈给 CoderAgent 修复错误，实现"编码→测试→修复"的自动化闭环。

2. **实现任务并行执行**：修改 Coordinator 使无依赖的步骤可并行执行（如 Researcher 和 Coder 同时工作），使用 `concurrent.futures` 线程池加速，减少整体响应时间。

3. **添加人工审核节点**：在关键步骤之间插入人工确认环节——Agent 输出结果后暂停，等待人工确认或修改后再传递给下一 Agent。适用于生产级内容发布流程。

4. **接入外部搜索工具**：让 ResearcherAgent 具备调用 Web Search API 或数据库查询的能力，通过 LangChain Tool 接口注册外部工具，使 Agent 能获取实时信息而非仅依赖 LLM 内部知识。

---

## 本章小结

- ✅ 实现了多 Agent 协作框架
- ✅ 构建了任务自动分解和分配机制
- ✅ 支持 Agent 间的消息传递
- ✅ 提供了可扩展的工作流模式

---

## 模块总结

恭喜完成 **模块12：项目实战**！

你已经实践了：
- ✅ 企业知识库问答系统
- ✅ 多功能文档智能助手
- ✅ 多 Agent 协作系统

这些项目综合运用了之前学习的所有技术，包括 LangChain、RAG、Agent、LangGraph 等。

---

## 课程总结

恭喜你完成了 **LLM 应用开发从入门到精通** 的全部学习！

### 学习路径回顾

```
基础篇                  进阶篇                   实战篇
├─ Python 环境          ├─ 向量数据库            ├─ 智能问答
├─ LLM API 调用        ├─ RAG 高级技术          ├─ 文档助手
├─ Prompt 工程         ├─ Agent 开发            └─ 多 Agent 系统
└─ LangChain 基础      ├─ LangGraph
                       └─ MCP 协议
```

### 后续学习建议

1. **深入特定领域**：选择感兴趣的方向深入研究
2. **动手实践**：用所学技术解决实际问题
3. **关注前沿**：跟踪 AI 领域的最新发展
4. **参与社区**：加入开源社区，分享和学习

祝你在 AI 应用开发的道路上越走越远！🚀
