import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 02_agent_basic.py
# 基础 Agent：自动调用工具
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

# 导入工具（定义在 define_tools.py 中）
import sys
sys.path.insert(0, os.path.dirname(__file__))
from define_tools import get_weather, calculator, search_knowledge_base

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)

tools = [get_weather, calculator, search_knowledge_base]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="你是智能助手，可以查询天气、计算、搜索公司知识库。请用中文回复。",
)

# 测试多种场景
test_cases = [
    "今天北京天气怎么样？",
    "帮我算一下 15 * 8 + 27",
    "公司年假政策是什么？",
    "北京天气热还是上海天气热？比较一下",
]

for question in test_cases:
    print(f"\n{'='*50}")
    print(f"Q: {question}")
    result = agent.invoke({
        "messages": [HumanMessage(content=question)]
    })
    answer = result["messages"][-1].content
    print(f"A: {answer}")
