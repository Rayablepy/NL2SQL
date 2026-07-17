import pypdf
from langchain_core.documents import Document
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
print(len(docs))
