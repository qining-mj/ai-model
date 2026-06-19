import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 01_json_output_parser.py
# JsonOutputParser：LLM 输出 → dict
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "从用户描述中提取信息，输出严格 JSON。\n{format_instructions}"),
    ("human", "{description}"),
])

prompt = prompt.partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser

result = chain.invoke({
    "description": "我叫李四，手机号 13800138000，住在北京市朝阳区，今年 30 岁"
})
print(f"结果: {result}")
print(f"类型: {type(result)}")
print(f"姓名: {result.get('name', 'N/A')}")
print(f"手机: {result.get('phone', 'N/A')}")
