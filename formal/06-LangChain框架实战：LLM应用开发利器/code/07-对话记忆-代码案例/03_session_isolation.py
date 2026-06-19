import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 03_session_isolation.py
# Session 隔离：不同用户/会话的历史互不影响
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
    ("system", "你是客服助手。用户可能提及个人信息，记住上下文。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

store = {}
def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain, get_history,
    input_messages_key="question",
    history_messages_key="history",
)

# 两个"用户"同时对话
users = {
    "张三": "session_001",
    "李四": "session_002",
}

# 张三的对话
c1 = {"configurable": {"session_id": users["张三"]}}
r1 = chain_with_memory.invoke({"question": "你好，我是张三，订单号 A123"}, config=c1)
print(f"张三: 我是张三 → AI: {r1[:40]}...")

# 李四的对话（不同 session，看不到张三的信息）
c2 = {"configurable": {"session_id": users["李四"]}}
r2 = chain_with_memory.invoke({"question": "你好，我是李四，订单号 B456"}, config=c2)
print(f"李四: 我是李四 → AI: {r2[:40]}...")

# 张三回来追问（session_001 的上下文还在）
r3 = chain_with_memory.invoke({"question": "我的订单号是什么？"}, config=c1)
print(f"张三: 我的订单号是什么？ → AI: {r3[:60]}...")

# 李四也问同样问题（session_002 返回李四的订单号）
r4 = chain_with_memory.invoke({"question": "我的订单号是什么？"}, config=c2)
print(f"李四: 我的订单号是什么？ → AI: {r4[:60]}...")

print(f"\n总 session 数: {len(store)}")
for sid, hist in store.items():
    print(f"  {sid}: {len(hist.messages)} 条消息")
