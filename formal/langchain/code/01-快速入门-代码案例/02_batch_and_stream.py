import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 02_batch_and_stream.py
# batch() 批量调用 和 stream() 流式调用
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是中→英翻译官。只输出译文。"),
    ("human", "{text}"),
])

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

chain = prompt | llm | StrOutputParser()

# === batch() 批量调用 ===
texts = [
    "今天天气真好",
    "我明天要去北京出差",
    "这道菜怎么做的？",
]

print("=== 批量翻译 ===")
results = chain.batch([{"text": t} for t in texts])
for src, dst in zip(texts, results):
    print(f"  {src} → {dst}")

# === stream() 流式调用 ===
print("\n=== 流式翻译（打字机效果）===")
for chunk in chain.stream({"text": "春眠不觉晓，处处闻啼鸟。"}):
    print(chunk, end="", flush=True)
print()
