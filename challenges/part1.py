"""This challenge just has a password in the system prompt. No filtering, etc."""
import os

from logging import getLogger
from typing import Generator

from common import llm
from common.constants import easy_system_prompt

logger = getLogger(__name__)
password: str = os.getenv("PART1_PWD", "JURISPRUDENCE")

def run(message: str, stream: bool = False) -> str | Generator[str, None, None]:
    system_prompt = easy_system_prompt.format(password=password)

    if stream:
        return llm.stream_generate(prompt=message, system_prompt=system_prompt)

    response: str = llm.respond(prompt=message, system_prompt=system_prompt)
    logger.info("Got response \"%s\" from the LLM.", response)

    logger.info(
        "Returning response \"%s\"",
        response[:50].replace("\n", " ") + ("..." if len(response) > 50 else "."),
    )
    return response

