import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 02_chat_prompt_template.py
# ChatPromptTemplate 多角色消息模板
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7,
)

# 基础多角色模板
basic_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，用{language}回答。"),
    ("human", "{question}"),
])

chain = basic_prompt | llm | StrOutputParser()
result = chain.invoke({
    "role": "Python 技术专家",
    "language": "中文",
    "question": "什么是列表推导式？用一句话说明。",
})
print(f"基础模板: {result}")

# 带 MessagesPlaceholder 的模板（用于多轮对话）
history_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是智能客服助手。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

# 模拟历史
history = [
    HumanMessage(content="我的订单号是 12345"),
    AIMessage(content="好的，正在为您查询订单 12345 的状态..."),
]

chain2 = history_prompt | llm | StrOutputParser()
result2 = chain2.invoke({
    "history": history,
    "question": "到哪了？",
})
print(f"\n带历史模板: {result2}")
