import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 01_runnable_passthrough.py
# RunnablePassthrough 透传与数据增强
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

# 模拟检索函数
def mock_retrieve(question: str) -> str:
    kb = {
        "年假": "员工入职满1年享5天年假，满3年享10天年假。",
        "加班": "工作日加班1.5倍工资，周末2倍，法定假日3倍。",
    }
    for key, val in kb.items():
        if key in question:
            return val
    return "未找到相关制度信息。"

# 用 RunnablePassthrough.assign 注入检索结果
prompt = ChatPromptTemplate.from_messages([
    ("system", "根据公司制度回答问题。\n\n制度内容：\n{context}"),
    ("human", "{question}"),
])

rag_chain = (
    RunnablePassthrough.assign(
        context=lambda x: mock_retrieve(x["question"])
    )
    | prompt
    | llm
    | StrOutputParser()
)

print(rag_chain.invoke({"question": "年假有多少天？"}))
print()
print(rag_chain.invoke({"question": "加班费怎么算？"}))
