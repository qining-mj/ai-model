import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 04_complex_extraction.py
# 复杂 Schema：嵌套对象的简历提取
# 注意：复杂嵌套 Schema 推荐使用 PydanticOutputParser，format_instructions 能精确传达字段名
import os
import sys
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)

class WorkExperience(BaseModel):
    company: str = Field(description="公司名称")
    position: str = Field(description="职位")
    duration_years: float = Field(description="工作年限")
    highlights: list[str] = Field(description="关键成就")

class Resume(BaseModel):
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")
    education: str = Field(description="最高学历")
    total_years: int = Field(description="总工作年限")
    experiences: list[WorkExperience] = Field(description="工作经历")
    skills: list[str] = Field(description="技能列表")
    expected_position: Optional[str] = Field(None, description="期望职位")

# 复杂嵌套 Schema 推荐 PydanticOutputParser — format_instructions 精确传达字段名
parser = PydanticOutputParser(pydantic_object=Resume)
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个简历信息提取助手。从用户描述中提取信息。\n{format_instructions}"),
    ("human", "{text}"),
])
prompt = prompt.partial(format_instructions=parser.get_format_instructions())
chain = prompt | llm | parser

resume_text = """
张三，30岁，硕士学历，共8年工作经验。
曾在腾讯做后端开发3年，主导设计了一套高并发消息系统；
后在字节跳动做技术负责人2年，带领10人团队；
精通 Go、Python、K8s。
期望做后端架构师。
"""

result = chain.invoke({"text": resume_text})

print(f"姓名: {result.name}")
print(f"学历: {result.education}")
print(f"总年限: {result.total_years}年")
print(f"技能: {', '.join(result.skills)}")
print(f"期望: {result.expected_position}")
for exp in result.experiences:
    print(f"  - {exp.company}: {exp.position} ({exp.duration_years}年)")
