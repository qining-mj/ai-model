import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 02_runnable_parallel.py
# RunnableParallel 并行执行
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

# 两个分析维度
emotion_prompt = ChatPromptTemplate.from_messages([
    ("system", "分析以下文本的情感（正面/负面/中性），只输出一个词。"),
    ("human", "{text}"),
])

keyword_prompt = ChatPromptTemplate.from_messages([
    ("system", "提取以下文本的3个关键词，用逗号分隔。"),
    ("human", "{text}"),
])

summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "用一句话总结以下文本。"),
    ("human", "{text}"),
])

# 三路并行
parallel_chain = (
    RunnableParallel(
        emotion=emotion_prompt | llm | StrOutputParser(),
        keywords=keyword_prompt | llm | StrOutputParser(),
        summary=summary_prompt | llm | StrOutputParser(),
    )
)

text = "今天的项目会议非常高效，团队就新功能的设计方案达成了共识，下周一启动开发。"
result = parallel_chain.invoke({"text": text})

print(f"原文: {text}\n")
print(f"情感: {result['emotion']}")
print(f"关键词: {result['keywords']}")
print(f"摘要: {result['summary']}")
