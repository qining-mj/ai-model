"""
02_fastapi_stream.py
FastAPI 流式响应服务

运行方式：
1. pip install fastapi uvicorn openai python-dotenv
2. python 02_fastapi_stream.py
3. 访问 http://localhost:8000/docs 测试接口
"""
import os
import json
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

app = FastAPI(title="流式 API 服务", description="LLM 流式输出演示")

# 添加 CORS 支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()


class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000


def generate_stream(message: str, model: str, temperature: float, max_tokens: int):
    """生成器函数 - 产生 SSE 格式数据"""
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """流式聊天接口"""
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="未配置 OPENAI_API_KEY")

    return StreamingResponse(
        generate_stream(
            request.message,
            request.model,
            request.temperature,
            request.max_tokens
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 nginx 缓冲
        }
    )


@app.get("/", response_class=HTMLResponse)
async def index():
    """演示页面"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>流式聊天演示</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        #output { white-space: pre-wrap; border: 1px solid #ccc; padding: 15px; min-height: 200px; background: #f9f9f9; }
        input { width: 70%; padding: 10px; font-size: 16px; }
        button { padding: 10px 20px; font-size: 16px; cursor: pointer; }
        .status { color: #666; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>流式输出演示</h1>
    <p>
        <input type="text" id="input" placeholder="输入消息..." value="写一首关于编程的诗">
        <button onclick="sendMessage()">发送</button>
    </p>
    <div id="output">等待输入...</div>
    <div class="status" id="status"></div>

    <script>
    async function sendMessage() {
        const input = document.getElementById('input').value;
        const output = document.getElementById('output');
        const status = document.getElementById('status');

        output.textContent = '';
        status.textContent = '正在生成...';

        const startTime = Date.now();

        try {
            const response = await fetch('/chat/stream', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input })
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const text = decoder.decode(value);
                const lines = text.split('\\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') {
                            const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
                            status.textContent = `完成！耗时: ${elapsed}秒`;
                        } else {
                            try {
                                const json = JSON.parse(data);
                                if (json.content) {
                                    output.textContent += json.content;
                                } else if (json.error) {
                                    output.textContent += '\\n错误: ' + json.error;
                                }
                            } catch (e) {}
                        }
                    }
                }
            }
        } catch (error) {
            output.textContent = '错误: ' + error.message;
            status.textContent = '失败';
        }
    }
    </script>
</body>
</html>
    """


if __name__ == "__main__":
    import uvicorn
    print("启动流式 API 服务...")
    print("访问 http://localhost:8000 查看演示页面")
    print("访问 http://localhost:8000/docs 查看 API 文档")
    uvicorn.run(app, host="0.0.0.0", port=8000)
