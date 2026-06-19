import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 02_callbacks.py
# 自定义 Callback Handler：Token 统计 + 成本计算
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

# === 自定义 Callback ===

class CostTracker(BaseCallbackHandler):
    """统计 Token 用量和成本"""

    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.call_count = 0
        # DeepSeek 价格（示例）：prompt ¥1/M, completion ¥2/M
        self.prompt_price_per_m = 1.0
        self.completion_price_per_m = 2.0

    def on_llm_end(self, response: LLMResult, **kwargs):
        self.call_count += 1
        for gen in response.generations:
            info = gen[0].generation_info or {}
            usage = info.get("token_usage", {})
            pt = usage.get("prompt_tokens", 0)
            ct = usage.get("completion_tokens", 0)
            self.total_prompt_tokens += pt
            self.total_completion_tokens += ct

    @property
    def total_cost(self):
        cost_p = self.total_prompt_tokens / 1_000_000 * self.prompt_price_per_m
        cost_c = self.total_completion_tokens / 1_000_000 * self.completion_price_per_m
        return cost_p + cost_c

    def report(self):
        return (
            f"LLM 调用次数: {self.call_count}\n"
            f"Prompt Tokens: {self.total_prompt_tokens}\n"
            f"Completion Tokens: {self.total_completion_tokens}\n"
            f"总计 Tokens: {self.total_prompt_tokens + self.total_completion_tokens}\n"
            f"预估成本: ¥{self.total_cost:.6f}"
        )

tracker = CostTracker()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是有用的助手。"),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

# 绑定 callback
chain_with_tracker = chain.with_config(callbacks=[tracker])

questions = [
    "介绍 Python",
    "什么是机器学习？",
    "解释一下量子计算",
]

for q in questions:
    result = chain_with_tracker.invoke({"question": q})
    print(f"Q: {q}")
    print(f"A: {result[:50]}...\n")

print("=" * 40)
print(tracker.report())
