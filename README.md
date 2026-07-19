# NL2RAG
An AI powered, simple RAG pipeline that runs completely within your local system. It uses a streamlit based frontend that supports file uploads of basically any file type, as well as a basic user to agent chat flow. 



Uploaded files are passed into an embbedding model of your choice that can be configured in a .env file, and stored in a local chromaDB database that the agent can perform similarity searches on to search for data when needed.

Due to said capability being saved as a tool, the local model only queries it when necessary, reducing performance overhead. The local model can be configured to use different models in your .env file.

Right now, the model is intitialised using a generic langchain init_chat_model harness that connects to a localhost server by lmstudio. Lmstudio also utilises Just In Time(JIT) loading, hence you need not manually load your models prior to using this app. Similarly, the embedding model uses the OpenAI embeddings harness to obtain embeddings from the model in LMstudio. 

The overall aim of this project is just as a segment for my larger projects, but it can be used for other applications. Simply clone the repo and set your environment variables as per the .env.example, then cd to the root project directory and run "streamlit run gui.py"
