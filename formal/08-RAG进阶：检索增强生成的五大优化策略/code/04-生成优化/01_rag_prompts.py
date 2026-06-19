"""
01_rag_prompts.py
RAG Prompt 模板
"""
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# 基础 RAG Prompt
BASIC_RAG_PROMPT = """基于以下上下文回答问题。如果上下文中没有相关信息，请明确说明。

上下文：
{context}

问题：{question}

回答："""


# 带引用的 RAG Prompt
CITATION_RAG_PROMPT = """基于以下带编号的上下文回答问题。回答时请引用相关来源的编号。

上下文：
{context}

问题：{question}

请按以下格式回答：
1. 直接回答问题
2. 在答案中用 [1], [2] 等标注引用来源

回答："""


# 严格模式 RAG Prompt
STRICT_RAG_PROMPT = """你是一个严谨的问答助手。请仅根据提供的上下文回答问题。

规则：
1. 只使用上下文中的信息
2. 不要添加上下文中没有的内容
3. 如果上下文不足以回答，明确说明
4. 对于不确定的内容，表明不确定性

上下文：
{context}

问题：{question}

回答："""


def test_prompts():
    """测试不同 Prompt"""
    print("=" * 60)
    print("【RAG Prompt 模板测试】")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    context = """
[1] LangChain 是一个用于开发 LLM 应用的框架。
[2] LangChain 由 Harrison Chase 于 2022 年创建。
[3] LCEL 是 LangChain Expression Language 的缩写。
"""

    question = "LangChain 是什么？谁创建的？"

    prompts = {
        "基础": BASIC_RAG_PROMPT,
        "引用": CITATION_RAG_PROMPT,
        "严格": STRICT_RAG_PROMPT,
    }

    for name, template in prompts.items():
        print(f"\n【{name}模式】")
        print("-" * 40)

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm

        response = chain.invoke({
            "context": context,
            "question": question
        })

        print(response.content)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    test_prompts()
