import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 01_langserve_app.py
# LangServe：一键部署 Chain 为 REST API
# 运行: python 01_langserve_app.py
# 然后访问: http://localhost:8000/docs
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
from fastapi import FastAPI
import uvicorn

load_dotenv()

# 翻译 Chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是专业翻译官。{source}→{target}。只输出译文，不要解释。"),
    ("human", "{text}"),
])

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

translator = prompt | llm | StrOutputParser()

app = FastAPI(
    title="翻译服务 API",
    version="1.0.0",
    description="基于 LangChain 1.3.4 + DeepSeek 的翻译服务",
)

add_routes(
    app,
    translator,
    path="/translate",
)

if __name__ == "__main__":
    print("翻译服务已启动: http://localhost:8000")
    print("API 文档: http://localhost:8000/docs")
    print("Playground: http://localhost:8000/translate/playground")
    uvicorn.run(app, host="0.0.0.0", port=8000)
