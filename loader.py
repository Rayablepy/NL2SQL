import pypdf
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

def load_data(file_path: str) -> list[Document]:
    reader = pypdf.PdfReader(file_path)
    return [
        Document(
            page_content=page.extract_text() or "",
            metadata={"source": file_path, "page": i},
        )
        for i, page in enumerate(reader.pages)
    ]
file_path = "./sample_data/testpdf.pdf"
docs = load_data(file_path)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
splits = text_splitter.split_documents(docs)
index = store.add_documents(documents=splits)

@tool
def query_data(query: str) -> str:
    """Query a local RAG database for information matching the query

    Args:
        query (str): The query string to search for in the database

    Returns:
        str: The matching results from the database
    """
    results = store.similarity_search(query)
    return "Results:\n" + "\n".join([doc.page_content for doc in results])
