
import textract
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.tools import tool
from config import ACTUAL_FILE_PATH, EMBEDDING_MODEL_NAME, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_BATCH_SIZE
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL_NAME,
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="lm-studio",
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

text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, add_start_index=True)

def save_data(file_name: str):
    docs=read_data(ACTUAL_FILE_PATH+file_name)
    splits = text_splitter.split_documents(docs)
    for i in range(0, len(splits), EMBEDDING_BATCH_SIZE):
        batch = splits[i:i + EMBEDDING_BATCH_SIZE]
        store.add_documents(documents=batch)

@tool
async def query_data(query: str, k: int = 4) -> str:
    """Query a local RAG database for information matching the query

    Args:
        query (str): The query string to search for in the database
        k (int): Number of top results to return (default: 4)

    Returns:
        str: The matching results from the database
    """
    results = await store.asimilarity_search(query, k=k)
    return "Results:\n" + "\n".join([doc.page_content for doc in results])

async def remove_data(file_path: str) -> str:
    """Remove all document chunks from the RAG database that were ingested from a specific file

    Args:
        file_path (str): The source file path to remove (as stored in document metadata)

    Returns:
        str: A message confirming how many chunks were removed, or that no matching chunks were found
    """
    existing = store.get(where={"source": file_path})
    if existing and existing["ids"]:
        count = len(existing["ids"])
        store.delete(ids=existing["ids"])
        return f"Removed {count} chunks sourced from '{file_path}'."
    return f"No chunks found for source '{file_path}'."

def list_files() -> list[str]:
    all_data = store.get(include=["metadatas"])
    sources = set()
    if all_data and all_data["metadatas"]:
        for meta in all_data["metadatas"]:
            if "source" in meta:
                sources.add(meta["source"])
    return sorted(sources)
