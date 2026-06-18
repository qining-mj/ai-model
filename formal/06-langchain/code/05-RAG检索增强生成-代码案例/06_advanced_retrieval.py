import warnings; warnings.filterwarnings('ignore', message=r'Core Pydantic V1|langchain-community')
# 06_advanced_retrieval.py
# 高级检索策略：MMR、相似度阈值过滤
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
员工入职满1年可享受5天带薪年假。满3年可享受10天带薪年假。
年假需提前1周申请，经主管批准后生效。未使用的年假可累积到次年，上限15天。

第二章 考勤制度
工作时间：周一至周五 9:00-18:00。迟到30分钟以内扣除半天工资。

第三章 报销制度
差旅报销需提供正规发票。住宿标准：一线城市400元/晚，其他城市300元/晚。
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
vectorstore = Chroma.from_documents(docs, embeddings)

query = "年假政策"

# 1. 普通相似度检索
basic_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
print("=== 相似度检索 ===")
for doc in basic_retriever.invoke(query):
    print(f"  {doc.page_content[:80]}...")

# 2. MMR 检索（增加多样性）
mmr_retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5},
)
print("\n=== MMR 检索（多样性优先）===")
for doc in mmr_retriever.invoke(query):
    print(f"  {doc.page_content[:80]}...")

# 3. 相似度阈值过滤
threshold_retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.2, "k": 3},
)
print("\n=== 相似度阈值过滤 ===")
results = threshold_retriever.invoke(query)
print(f"找到 {len(results)} 个结果（阈值 0.2）")
for doc in results:
    print(f"  {doc.page_content[:80]}...")
