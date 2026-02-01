from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI

# mostly done for multimodal project
def get_genai_apikey():
    return settings.GENAI_API_KEY

def get_google_ai_model(model="gemini-2.5-flash"):
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=0,
        max_retries=3,
        api_key=get_genai_apikey()
    )
