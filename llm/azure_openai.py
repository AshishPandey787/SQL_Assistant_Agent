from openai import AzureOpenAI
from core.config import settings

_client = AzureOpenAI(
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_version=settings.AZURE_OPENAI_API_VERSION,
)

def embed(texts: list[str]) -> list[list[float]]:
    resp = _client.embeddings.create(
        model=settings.AZURE_OPENAI_EMBED_DEPLOYMENT,
        input=texts
    )
    return [d.embedding for d in resp.data]

def chat_json(system: str, user: str, temperature: float = 0.1) -> str:
    # We enforce JSON by instruction; you can also use "response_format"
    resp = _client.chat.completions.create(
        model=settings.AZURE_OPENAI_CHAT_DEPLOYMENT,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content