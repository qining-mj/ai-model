import warnings; warnings.filterwarnings('ignore', message=r'Core Pydantic V1|langchain-community')
# 05_rag_with_source.py
# 带来源引用的 RAG
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

os.makedirs("./data", exist_ok=True)
if not os.path.exists("./data/employee_handbook.txt"):
    with open("./data/employee_handbook.txt", "w", encoding="utf-8") as f:
        f.write("""员工手册

第一章 年假制度
员工入职满1年可享受5天带薪年假。满3年可享受10天带薪年假。
年假需提前1周申请，经主管批准后生效。

第二章 考勤制度
工作时间：周一至周五 9:00-18:00。迟到30分钟以内扣除半天工资。
""")

docs = TextLoader("./data/employee_handbook.txt", encoding="utf-8").load()
chunks = RecursiveCharacterTextSplitter(
    chunk_size=300, chunk_overlap=50,
).split_documents(docs)
embeddings = OpenAIEmbeddings(
    model="embedding-2",
    base_url=os.getenv("ZHIPU_BASE_URL"),
    api_key=os.getenv("ZHIPU_API_KEY"),
)
vectorstore = Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_messages([
    ("system", """根据文档回答问题，并在答案末尾注明引用的文档编号和内容。

文档：
{context}"""),
    ("human", "{question}"),
])

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

def format_docs_with_id(docs) -> str:
    """格式化时加上编号，方便 LLM 引用"""
    result = []
    for i, doc in enumerate(docs):
        result.append(f"[文档{i+1}] {doc.page_content}")
    return "\n\n".join(result)

rag_with_source = (
    {
        "context": retriever | format_docs_with_id,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

print(rag_with_source.invoke("年假怎么申请？"))
