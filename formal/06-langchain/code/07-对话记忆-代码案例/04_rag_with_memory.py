import warnings; warnings.filterwarnings('ignore', message=r'Core Pydantic V1|langchain-community')
# 04_rag_with_memory.py
# RAG + Memory：上下文感知的文档问答
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
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
年假需提前1周申请，经主管批准后生效。未使用年假可累积到次年，上限15天。

第二章 考勤制度
工作时间：周一至周五 9:00-18:00。迟到30分钟以内扣除半天工资。

第三章 报销制度
差旅住宿标准：一线城市400元/晚，其他城市300元/晚。招待费单次不超过1000元。
""")

# 构建检索器
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

# RAG + Memory Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """根据文档内容和对话历史回答问题。
如果文档没有相关信息，说明"文档未提及"。

文档内容：
{context}"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

def format_docs(docs) -> str:
    return "\n\n".join(d.page_content for d in docs)

chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

store = {}
def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain, get_history,
    input_messages_key="question",
    history_messages_key="history",
)

session = {"configurable": {"session_id": "hr_qa"}}

# 多轮 RAG 问答
rounds = [
    "年假怎么申请？",
    "那没休完的能攒到下一年吗？",  # 追问（知道在说年假）
    "加班费怎么算？",               # 切换话题
]

for q in rounds:
    resp = chain_with_memory.invoke({"question": q}, config=session)
    print(f"Q: {q}")
    print(f"A: {resp}\n")
