"""This challenge just has a password in the system prompt. No filtering, etc."""
import os

from logging import getLogger

from common import llm
from common.constants import easy_system_prompt

logger = getLogger(__name__)
password: str = os.getenv("PART1_PWD", "JURISPRUDENCE")

def run(message: str) -> str:
    response: str = llm.respond(prompt=message, system_prompt=easy_system_prompt.format(password=password))
    logger.info("Got response \"%s\" from the LLM.", response)

    logger.info(
        "Returning response \"%s\"",
        response[:50].replace("\n", " ") + ("..." if len(response) > 50 else "."),
    )
    return response

