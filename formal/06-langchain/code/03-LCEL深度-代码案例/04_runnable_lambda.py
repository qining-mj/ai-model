import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 04_runnable_lambda.py
# RunnableLambda 自定义函数 + with_fallbacks
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
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

# 自定义预处理函数
def clean_input(data: dict) -> dict:
    """去除多余空白、统一小写"""
    text = data["text"].strip().lower()
    return {"text": text, "style": data.get("style", "正式")}

# 自定义后处理函数
def add_timestamp(result: str) -> str:
    """给结果加上时间戳"""
    from datetime import datetime
    t = datetime.now().strftime("%H:%M:%S")
    return f"[{t}] {result}"

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{style}的助手。简洁回答。"),
    ("human", "{text}"),
])

# 函数变成 Runnable 融入管道
chain = (
    RunnableLambda(clean_input)
    | prompt
    | llm
    | StrOutputParser()
    | RunnableLambda(add_timestamp)
)

print(chain.invoke({"text": "  什么是 LangChain？  ", "style": "专业"}))
print(chain.invoke({"text": "  推荐一首诗  "}))
