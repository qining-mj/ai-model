import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 02_window_memory.py
# Window Memory：只保留最近 N 条消息
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是友好的聊天机器人。用简洁的语言回复。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

class WindowedMemory(BaseChatMessageHistory):
    """只保留最近 max_messages 条消息"""
    def __init__(self, max_messages: int = 6):
        self.messages: list[BaseMessage] = []
        self.max_messages = max_messages

    def add_message(self, message: BaseMessage):
        self.messages.append(message)
        self.messages = self.messages[-self.max_messages:]

    def clear(self):
        self.messages = []

store = {}

def get_window_history(session_id: str) -> WindowedMemory:
    if session_id not in store:
        store[session_id] = WindowedMemory(max_messages=6)  # 最近 3 轮
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain, get_window_history,
    input_messages_key="question",
    history_messages_key="history",
)

session = {"configurable": {"session_id": "user_002"}}

# 10 轮对话，观察窗口滑动效果
for i in range(10):
    q = f"这是第{i+1}轮对话"
    if i == 0:
        q = "我叫张三，今年 30 岁"
    elif i == 8:
        q = "我刚才说我叫什么名字？"  # 早期信息可能已滑出窗口
    resp = chain_with_memory.invoke({"question": q}, config=session)
    history_count = len(store["user_002"].messages)
    print(f"轮{i+1} [历史{history_count}条] Q: {q[:20]}... → A: {resp[:30]}...")
