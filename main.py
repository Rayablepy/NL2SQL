
from config import CHAT_MODEL_NAME
from loader import query_data
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
tools = [query_data]
model=init_chat_model(
    model=CHAT_MODEL_NAME,
    model_provider="openai",
    base_url="http://localhost:1234/v1",
    api_key="not-needed",
    temperature=0.5,
)
agent = create_agent(
    model=model,
    tools=tools
)
def getresponse(user:str) -> str:
    response = agent.invoke(user)
    return response.content
