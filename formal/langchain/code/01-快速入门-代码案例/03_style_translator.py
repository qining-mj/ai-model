import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 03_style_translator.py
# 练习：带风格参数的翻译器
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是中→英翻译官。输出风格：{style}。只输出译文。"),
    ("human", "{text}"),
])

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

translator = prompt | llm | StrOutputParser()

text = "长风破浪会有时，直挂云帆济沧海。"

for style in ["口语化", "学术化", "诗歌"]:
    result = translator.invoke({"style": style, "text": text})
    print(f"[{style}] {result}")
