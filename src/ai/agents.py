from langchain.agents import create_agent
from ai.llms import get_google_ai_model
from ai.tools import document_tools

def get_document_agent():
    model = get_google_ai_model()
    return create_agent(
        model=model,
        tools=document_tools,
        system_prompt="You are helpful assistant in managing the users documents in this app"
    )