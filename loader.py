import textract
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.tools import tool
from config import EMBEDDING_MODEL_NAME
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

file_path="./sample_data/"
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100, add_start_index=True)

def save_data(file_name: str):
    docs=read_data(file_path+file_name)
    print(len(docs))
    splits = text_splitter.split_documents(docs)
    print(len(splits))
    store.add_documents(documents=splits)

save_data("IT2212_AssignmentReport_250506U.docx")
'''
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
'''
