
from langchain.chat_models import init_chat_model
model=init_chat_model(
    model="qwen/qwen3.5-9b",
    model_provider="openai",
    base_url="http://localhost:1234/v1",
    api_key="not-needed",
    temperature=0.5,
)

response=model.invoke("Hello")
print(response)
