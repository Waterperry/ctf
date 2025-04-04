import os

from logging import getLogger
from threading import Thread
from typing import Iterator

from openai import OpenAI

logger = getLogger(__name__)
model: str = os.environ["MODEL_NAME"]
llm_endpoint: str = os.getenv("LLM_ENDPOINT", "http://localhost:11434/v1")
llm_api_key: str = os.getenv("LLM_API_KEY", "ollama")

client = OpenAI(base_url=llm_endpoint, api_key=llm_api_key)

def respond(prompt: str, system_prompt: str) -> str:
    global client, model
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    logger.info("Generating response.")
    response = client.chat.completions.create(
        model=model,
        max_tokens=512,
        messages=messages,
        temperature=0.,
    )

    logger.info("Decoding output.")

    return response.choices[0].message.content

def stream_generate(prompt: str, system_prompt: str) -> Iterator[str]:
    """
    Return an Iterator object which yields chunks of text.
    This spawns a new thread in which the generation occurs, and so might cause problems with FastAPI...
    """
    global client, model
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    logger.info("Generating response.")
    response = client.chat.completions.create(
        model=model,
        max_tokens=512,
        messages=messages,
        temperature=0.,
        stream=True,
    )

    for chunk in response:
        yield chunk.choices[0].delta.content
