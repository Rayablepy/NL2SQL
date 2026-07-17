import os
from dotenv import load_dotenv
load_dotenv()
CHAT_MODEL_NAME=os.getenv("CHAT_MODEL_NAME")

EMBEDDING_MODEL_NAME=os.getenv("EMBEDDING_MODEL_NAME")
