import os
from openai import AzureOpenAI

_client = None

def get_azure_openai_client():
    global _client
    if _client is None:
        _client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )
    return _client
