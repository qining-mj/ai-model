import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 02_pydantic_output_parser.py
# PydanticOutputParser：LLM 输出 → Pydantic 对象
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)

# 定义 Schema
class Person(BaseModel):
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")
    skills: list[str] = Field(description="技能列表")

parser = PydanticOutputParser(pydantic_object=Person)

prompt = ChatPromptTemplate.from_messages([
    ("system", "从简历描述中提取人物信息。\n{format_instructions}"),
    ("human", "{resume}"),
])
prompt = prompt.partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser

result = chain.invoke({
    "resume": "王五，28岁，精通 Python、React、Docker，有 5 年后端开发经验"
})

print(f"类型: {type(result)}")
print(f"姓名: {result.name}")
print(f"年龄: {result.age}")
print(f"技能: {result.skills}")
# result 是真正的 Person 对象！IDE 有自动补全
