import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 03_runnable_branch.py
# RunnableBranch 条件路由
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

# 各分支 Chain
translate_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "你是翻译官。{source}→{target}。只输出译文。"),
        ("human", "{content}"),
    ]) | llm | StrOutputParser()
)

summarize_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "用一句话总结以下内容。"),
        ("human", "{content}"),
    ]) | llm | StrOutputParser()
)

qa_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "简洁回答以下问题。"),
        ("human", "{content}"),
    ]) | llm | StrOutputParser()
)

# 条件路由
router = RunnableBranch(
    (lambda x: "翻译" in x["action"], translate_chain),
    (lambda x: "总结" in x["action"], summarize_chain),
    qa_chain,  # 默认
)

full_chain = router

tests = [
    {"action": "翻译成英文", "content": "今天天气很好", "source": "中文", "target": "英文"},
    {"action": "帮我总结一下", "content": "LangChain是一个用于构建LLM应用的框架，提供了组件化和链式调用的能力..."},
    {"action": "随便聊聊", "content": "什么是人工智能？"},
]

for t in tests:
    print(f"\n{'='*40}")
    print(f"动作: {t['action']}")
    result = full_chain.invoke(t)
    print(f"结果: {result}")
