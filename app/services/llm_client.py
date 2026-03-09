import os
from openai import OpenAI

_client = None


def get_llm() -> OpenAI:
    """
    Singleton OpenAI client.
    """
    global _client

    if _client is None:
        _client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    return _client
