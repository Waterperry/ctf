"""This challenge will do RAG-like stuff."""

# NOTE: This challenge doesn't really fit in with the progression from before?
import os

from logging import getLogger

from common import llm
from common.constants import system_prompt
from common.embed import keyword_similarity

logger = getLogger(__name__)

password: str = os.getenv("PART5_PWD", "JURISPRUDENCE")

def run(message: str) -> str:
    logger.info("Doing embedding.")
    pretext: str = "\n\n".join(keyword_similarity(message)) + "\n\n"
    logger.info("Got pretext ```%s``` using embedding.", pretext)

    response: str = llm.respond(prompt=(pretext + message), system_prompt=system_prompt.format(password=password))
    logger.info("Got response \"%s\" from the LLM.", response)

    logger.info(
        "Returning response \"%s\"",
        response[:50].replace("\n", " ") + ("..." if len(response) > 50 else "."),
    )
    return response
