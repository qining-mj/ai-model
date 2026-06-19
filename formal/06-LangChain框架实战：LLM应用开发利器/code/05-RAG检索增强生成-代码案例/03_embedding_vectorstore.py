import warnings; warnings.filterwarnings('ignore', message=r'Core Pydantic V1|langchain-community')
# 03_embedding_vectorstore.py
# Embeddings + VectorStore：文本向量化与存储
import os
from dotenv import load_dotenv
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
员工入职满1年可享受5天带薪年假。
满3年可享受10天带薪年假。
年假需提前1周申请，经主管批准后生效。
未使用的年假可累积到次年，上限15天。

第二章 考勤制度
工作时间：周一至周五 9:00-18:00，午休12:00-13:00。
迟到30分钟以内扣除半天工资，超过30分钟按旷工处理。
每月可申请2次弹性工作时间。

第三章 报销制度
差旅报销需提供正规发票。
交通费实报实销，住宿标准：一线城市400元/晚，其他城市300元/晚。
招待费需提前申请，单次不超过1000元。
""")

# 1. 加载 + 切分
docs = TextLoader("./data/employee_handbook.txt", encoding="utf-8").load()
chunks = RecursiveCharacterTextSplitter(
    chunk_size=300, chunk_overlap=50,
    separators=["\n\n", "\n", "。"],
).split_documents(docs)
print(f"文档切分为 {len(chunks)} 个 chunk")

# 2. 向量化（使用智谱 Embedding API）
embeddings = OpenAIEmbeddings(
    model="embedding-2",
    base_url=os.getenv("ZHIPU_BASE_URL"),
    api_key=os.getenv("ZHIPU_API_KEY"),
)

# 3. 存入 Chroma
persist_dir = "./chroma_db"
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=persist_dir,
)
print(f"向量库已持久化到 {persist_dir}")

# 4. 检索测试
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

queries = ["年假怎么申请？", "上班时间是什么？", "出差住宿怎么报销？"]
for q in queries:
    print(f"\n查询: {q}")
    results = retriever.invoke(q)
    for i, doc in enumerate(results):
        print(f"  [{i}] {doc.page_content[:100].strip()}...")
