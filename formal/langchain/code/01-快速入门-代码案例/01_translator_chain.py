import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 01_translator_chain.py
# 第一个完整 Chain：翻译官
import os
import sys
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 修复 Windows 终端输出乱码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是专业的{source}到{target}翻译官。只输出译文，不要解释。"),
    ("human", "{text}"),
])

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

translator = prompt | llm | StrOutputParser()

results = [
    translator.invoke({
        "source": "中文", "target": "英文",
        "text": "海内存知己，天涯若比邻。",
    }),
    translator.invoke({
        "source": "中文", "target": "日文",
        "text": "今天天气真好。",
    }),
]

for r in results:
    print(r)
    print("---")
