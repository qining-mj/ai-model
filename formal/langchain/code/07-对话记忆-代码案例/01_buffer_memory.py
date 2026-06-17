import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 01_buffer_memory.py
# Buffer Memory：全量记忆
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是友好的聊天机器人。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

# 存储所有 session 的历史
store = {}

def get_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain, get_history,
    input_messages_key="question",
    history_messages_key="history",
)

# 对话
session = {"configurable": {"session_id": "user_001"}}

rounds = [
    "你好！我叫张三，我喜欢编程。",
    "我刚才说我叫什么？",
    "我喜欢什么来着？",
    "总结一下到目前为止我们的对话。",
]

for r in rounds:
    print(f"\n👤: {r}")
    resp = chain_with_memory.invoke({"question": r}, config=session)
    print(f"🤖: {resp}")

print(f"\n历史消息数: {len(store['user_001'].messages)}")
