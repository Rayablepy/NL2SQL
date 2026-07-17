from config import CHAT_MODEL_NAME
from langchain.chat_models import init_chat_model
model=init_chat_model(
    model=CHAT_MODEL_NAME,
    model_provider="openai",
    base_url="http://localhost:1234/v1",
    api_key="not-needed",
    temperature=0.5,
)

def getresponse(user:str) -> str:
    response = model.invoke(user)
    return response.content
