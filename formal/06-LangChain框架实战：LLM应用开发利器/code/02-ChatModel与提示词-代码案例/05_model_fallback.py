import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 05_model_fallback.py
# 多模型回退：主模型失败时自动切换备用模型
import os
import sys
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

# === 场景1：跨厂商容灾 ===
# 主模型用一个大模型（不可用的 base_url），备用模型用智谱
print("=== 场景1：跨厂商容灾（主模型不可用 → 自动切备用）===")

primary = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://invalid-api.example.com",  # 故意写错地址，模拟宕机
    api_key="fake-key",
    temperature=0,
    timeout=3,  # 3 秒超时，不让学生等太久
)
backup = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)

resilient_llm = primary.with_fallbacks([backup])

start = time.time()
try:
    response = resilient_llm.invoke("用一句话介绍 Python")
    elapsed = time.time() - start
    print(f"  回答: {response.content}")
    print(f"  耗时: {elapsed:.1f}s")
    print(f"  ✓ 主模型失败，备用模型自动接管，调用方代码无感知")
except Exception as e:
    print(f"  ✗ 全部模型失败: {e}")

# === 场景2：能力降级 — 推理模型 → 快速模型 ===
print("\n=== 场景2：能力降级（推理模型 → 通用模型）===")

reasoner = ChatOpenAI(
    model="deepseek-reasoner",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)
fast_llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)

smart_llm = reasoner.with_fallbacks([fast_llm])

try:
    response = smart_llm.invoke("一个数的2倍加5等于15，这个数是多少？")
    print(f"  回答: {response.content}")
    print(f"  response_metadata 模型: {response.response_metadata.get('model_name', 'N/A')}")
except Exception as e:
    print(f"  ✗ 失败: {e}")

# === 场景3：多级回退链 ===
print("\n=== 场景3：多级回退链（主 → 备用1 → 备用2）===")

primary_bad = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://invalid-endpoint.example.com",
    api_key="fake-key",
    timeout=2,
)
backup1 = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
    timeout=5,
)

# with_fallbacks 可以链式调用，构成多级回退
multi_fallback_llm = primary_bad.with_fallbacks([backup1])

try:
    response = multi_fallback_llm.invoke("你好，请简单介绍一下你自己")
    print(f"  回答: {response.content}")
    print(f"  ✓ 多级回退生效")
except Exception as e:
    print(f"  ✗ 全部失败: {type(e).__name__}")

# === 关键总结 ===
print("\n" + "=" * 50)
print("关键结论:")
print("  1. with_fallbacks([备选列表]) — 为主模型配置后备")
print("  2. 调用方式不变 — invoke/stream/batch 用法完全一样")
print("  3. 按列表顺序依次尝试 — 直到有一个成功或全部失败")
print("  4. 可跨厂商、可跨模型 — DeepSeek → 智谱 / reasoner → chat")
print("  5. 链式调用 — a.with_fallbacks([b]).with_fallbacks([c])")
