
import textract
from langchain_text_splitters import TokenTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.tools import tool
from config import ACTUAL_FILE_PATH, EMBEDDING_MODEL_NAME, EMBEDDING_MODEL_CONTEXT, EMBEDDING_MODEL_CHUNK
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL_NAME,
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="lm-studio",
    check_embedding_ctx_length=False,
)

store = Chroma(
    collection_name="NL2SQL",
    embedding_function=embeddings,
    persist_directory="./chroma_NL2SQL",
)

def read_data(file_path: str) -> list[Document]:
    text = textract.process(file_path).decode("utf-8")
    return [
        Document(
            page_content=text,
            metadata={"source": file_path},
        )
    ]

file_path=ACTUAL_FILE_PATH
text_splitter = TokenTextSplitter(encoding_name=EMBEDDING_MODEL_NAME,chunk_size=EMBEDDING_MODEL_CONTEXT,chunk_overlap=EMBEDDING_MODEL_CHUNK)

def save_data(file_name: str):
    docs=read_data(file_path+file_name)
    splits = text_splitter.split_documents(docs)
    store.add_documents(documents=splits,batch_size=50)

@tool
async def query_data(query: str) -> str:
    """Query a local RAG database for information matching the query

    Args:
        query (str): The query string to search for in the database

    Returns:
        str: The matching results from the database
    """
    results = await store.asimilarity_search(query)
    return "Results:\n" + "\n".join([doc.page_content for doc in results])
