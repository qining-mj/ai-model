import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 02_chat_prompt_template.py
# ChatPromptTemplate 多角色消息模板与 MessagesPlaceholder
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7,
)

# 1. 基础多角色模板
basic_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，用{language}回答。"),
    ("human", "{question}"),
])
chain1 = basic_prompt | llm | StrOutputParser()
print("=== 基础多角色模板 ===")
print(chain1.invoke({
    "role": "Python 专家", "language": "中文",
    "question": "列表推导式是什么？一句话说明。",
}))

# 2. 带历史消息的模板
history_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是智能客服助手。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])
chain2 = history_prompt | llm | StrOutputParser()

history = [
    HumanMessage(content="我的订单号是 12345"),
    AIMessage(content="正在查询订单 12345 的状态，请稍候..."),
]
print("\n=== 带历史消息的模板 ===")
print(chain2.invoke({"history": history, "question": "到哪了？"}))
