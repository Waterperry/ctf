"""This challenge will filter out the password if it appears in the response."""
import os

from logging import getLogger
from typing import Generator

from common import llm
from common.constants import system_prompt

logger = getLogger(__name__)

password: str = os.getenv("PART3_PWD", "JURISPRUDENCE")

def run(message: str, stream: bool = False) -> str | Generator[str, None, None]:
    _system_prompt = system_prompt.format(password=password)

    response: str = llm.respond(prompt=message, system_prompt=_system_prompt)
    logger.info("Got response \"%s\" from the LLM.", response)

    # filter response here for higher difficulties
    if password in response:
        logger.info("Editing response as password was in it.")
        response = response.replace(password, "<filtered>")

    logger.info(
        "Returning response \"%s\"",
        response[:50].replace("\n", " ") + ("..." if len(response) > 50 else "."),
    )
    return response

