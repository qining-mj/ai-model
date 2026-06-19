import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 02_fastapi_manual.py
# FastAPI 手动集成：更灵活的 API 控制（含流式接口）
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
import asyncio

load_dotenv()

# === Chain 初始化 ===
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{source}→{target}翻译官。只输出译文。"),
    ("human", "{text}"),
])

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

chain = prompt | llm | StrOutputParser()

# === API ===
app = FastAPI(title="翻译服务", version="1.0")

class TranslateRequest(BaseModel):
    text: str
    source: str = "中文"
    target: str = "英文"

class TranslateResponse(BaseModel):
    success: bool
    result: str
    error: str | None = None

# 普通接口
@app.post("/translate", response_model=TranslateResponse)
async def translate(req: TranslateRequest):
    try:
        result = await chain.ainvoke({
            "text": req.text,
            "source": req.source,
            "target": req.target,
        })
        return TranslateResponse(success=True, result=result)
    except Exception as e:
        return TranslateResponse(success=False, result="", error=str(e))

# 流式接口（SSE）
@app.post("/translate/stream")
async def translate_stream(req: TranslateRequest):
    async def event_stream():
        try:
            async for chunk in chain.astream({
                "text": req.text,
                "source": req.source,
                "target": req.target,
            }):
                yield f"data: {chunk}\n\n"
                await asyncio.sleep(0)
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: ERROR: {e}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    print("翻译服务已启动: http://localhost:8000")
    print("POST /translate — 普通翻译")
    print("POST /translate/stream — 流式翻译（SSE）")
    uvicorn.run(app, host="0.0.0.0", port=8000)
