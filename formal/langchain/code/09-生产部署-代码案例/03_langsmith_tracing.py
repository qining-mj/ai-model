import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 03_langsmith_tracing.py
# LangSmith 追踪配置 + 自定义标签
# 首先在 .env 中配置：
#   LANGCHAIN_API_KEY=ls_xxxxxxxxxxxxxx
#   LANGCHAIN_TRACING_V2=true
#   LANGCHAIN_PROJECT=my-production-app
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，用{style}风格回答。"),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

# 给每次调用打标签（在 LangSmith 中可过滤和搜索）
result = chain.with_config(
    tags=["production", "v1.3"],
    metadata={"user_id": "test_user", "feature": "chat"},
    run_name="test_tracing",
).invoke({
    "role": "助手",
    "style": "专业",
    "question": "什么是 RAG？",
})

print(result)
print("\n在 LangSmith 中查看: https://smith.langchain.com/")
print("可以按 tags=production 或 run_name=test_tracing 过滤")
