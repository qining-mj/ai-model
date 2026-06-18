"""
01_multi_agent.py
多 Agent 协作
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict


class Expert:
    """专家 Agent"""

    def __init__(self, name: str, expertise: str):
        self.name = name
        self.expertise = expertise
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    def respond(self, question: str, context: str = "") -> str:
        """回应问题"""
        prompt = ChatPromptTemplate.from_template("""
你是一位 {expertise} 专家，名叫 {name}。

{context}

问题: {question}

请从你的专业角度简要回答（2-3句话）:
""")
        chain = prompt | self.llm
        response = chain.invoke({
            "name": self.name,
            "expertise": self.expertise,
            "context": context,
            "question": question
        })
        return response.content


class Supervisor:
    """协调者"""

    def __init__(self, experts: List[Expert]):
        self.experts = experts
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def route(self, question: str) -> List[str]:
        """决定咨询哪些专家"""
        expert_list = ", ".join([f"{e.name}({e.expertise})" for e in self.experts])

        prompt = ChatPromptTemplate.from_template("""
根据问题决定需要咨询哪些专家。

可用专家: {experts}
问题: {question}

请列出需要咨询的专家名字（用逗号分隔，最多3个）:
""")
        chain = prompt | self.llm
        response = chain.invoke({"experts": expert_list, "question": question})

        names = [n.strip() for n in response.content.split(",")]
        return [n for n in names if any(e.name == n for e in self.experts)][:3]

    def synthesize(self, question: str, responses: Dict[str, str]) -> str:
        """综合意见"""
        responses_text = "\n\n".join([
            f"【{name}】: {response}"
            for name, response in responses.items()
        ])

        prompt = ChatPromptTemplate.from_template("""
请综合以下专家意见，给出最终答案。

问题: {question}

专家意见:
{responses}

综合答案（3-5句话）:
""")
        chain = prompt | self.llm
        return chain.invoke({
            "question": question,
            "responses": responses_text
        }).content


class ExpertTeam:
    """专家团队"""

    def __init__(self):
        self.experts = [
            Expert("技术专家", "软件开发"),
            Expert("产品专家", "产品设计"),
            Expert("商业专家", "商业策略"),
        ]
        self.supervisor = Supervisor(self.experts)

    def consult(self, question: str) -> str:
        """咨询团队"""
        print(f"\n问题: {question}")
        print("=" * 50)

        # 1. 路由
        selected = self.supervisor.route(question)
        print(f"咨询专家: {', '.join(selected)}")

        # 2. 收集意见
        responses = {}
        for expert in self.experts:
            if expert.name in selected:
                print(f"\n【{expert.name}】分析中...")
                response = expert.respond(question)
                responses[expert.name] = response
                print(f"  {response}")

        # 3. 综合
        print("\n【综合分析】")
        final = self.supervisor.synthesize(question, responses)

        return final


def multi_agent_demo():
    """演示"""
    print("=" * 60)
    print("【专家团队协作】")
    print("=" * 60)

    team = ExpertTeam()

    questions = [
        "如何开发一个成功的 AI 产品？",
    ]

    for q in questions:
        result = team.consult(q)
        print(f"\n最终答案:\n{result}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    multi_agent_demo()
