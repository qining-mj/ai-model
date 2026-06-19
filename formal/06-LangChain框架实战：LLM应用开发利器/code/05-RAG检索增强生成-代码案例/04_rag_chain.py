import warnings; warnings.filterwarnings('ignore', message=r'Core Pydantic V1|langchain-community')
# 04_rag_chain.py
# 完整 RAG Chain：检索 + 生成
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# 准备数据（首次运行）
os.makedirs("./data", exist_ok=True)
if not os.path.exists("./data/employee_handbook.txt"):
    with open("./data/employee_handbook.txt", "w", encoding="utf-8") as f:
        f.write("""员工手册

第一章 年假制度
员工入职满1年可享受5天带薪年假。满3年可享受10天带薪年假。
年假需提前1周申请，经主管批准后生效。未使用的年假可累积到次年，上限15天。

第二章 考勤制度
工作时间：周一至周五 9:00-18:00，午休12:00-13:00。
迟到30分钟以内扣除半天工资，超过30分钟按旷工处理。每月可申请2次弹性工作时间。

第三章 报销制度
差旅报销需提供正规发票。交通费实报实销，住宿标准：一线城市400元/晚，其他城市300元/晚。招待费需提前申请，单次不超过1000元。
""")

# 构建索引
docs = TextLoader("./data/employee_handbook.txt", encoding="utf-8").load()
chunks = RecursiveCharacterTextSplitter(
    chunk_size=300, chunk_overlap=50, separators=["\n\n", "\n", "。"],
).split_documents(docs)
embeddings = OpenAIEmbeddings(
    model="embedding-2",
    base_url=os.getenv("ZHIPU_BASE_URL"),
    api_key=os.getenv("ZHIPU_API_KEY"),
)
vectorstore = Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# RAG Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """根据以下文档内容回答用户问题。
如果文档内容不足以回答，请如实说"文档中未找到相关信息"。

文档内容：
{context}"""),
    ("human", "{question}"),
])

# LLM
llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

# 格式化检索结果
def format_docs(docs) -> str:
    return "\n\n".join(d.page_content for d in docs)

# RAG Chain
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

# 问答
questions = [
    "年假怎么申请？",
    "上班时间是什么？",
    "公司有团建政策吗？",
]
for q in questions:
    print(f"\n{'='*40}")
    print(f"Q: {q}")
    print(f"A: {rag_chain.invoke(q)}")
