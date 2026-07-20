import os
from dotenv import load_dotenv
load_dotenv()
CHAT_MODEL_NAME=os.getenv("CHAT_MODEL_NAME")
ACTUAL_FILE_PATH="./user_data/"
EMBEDDING_MODEL_NAME=os.getenv("EMBEDDING_MODEL_NAME")
CHUNK_SIZE=int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP=int(os.getenv("CHUNK_OVERLAP"))
EMBEDDING_BATCH_SIZE=int(os.getenv("EMBEDDING_BATCH_SIZE"))
