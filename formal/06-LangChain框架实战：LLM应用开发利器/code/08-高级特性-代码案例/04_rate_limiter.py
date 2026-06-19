import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 04_rate_limiter.py
# Rate Limiter：限流保护
import os, time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.rate_limiters import InMemoryRateLimiter

load_dotenv()

# 限流：每秒最多 2 次请求
limiter = InMemoryRateLimiter(
    requests_per_second=2,
    check_every_n_seconds=0.1,
    max_bucket_size=5,
)

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
    rate_limiter=limiter,
)

print("带限流的批量调用（每秒最多 2 次）")
start = time.time()

questions = ["1+1=?", "2+2=?", "3+3=?", "4+4=?", "5+5=?"]
for i, q in enumerate(questions):
    t0 = time.time()
    r = llm.invoke(q)
    elapsed = time.time() - t0
    total = time.time() - start
    print(f"  请求{i+1}: {q} → {r.content} (耗时{elapsed:.2f}s, 累计{total:.1f}s)")

print(f"\n总耗时: {time.time() - start:.1f}s")
print("如果无限流，5 个请求会同时发出；有了限流，请求被均匀分散。")
