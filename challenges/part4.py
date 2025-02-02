"""This challenge will completely overwrite the response if it contains the password."""
import os

from logging import getLogger

from common import llm
from common.constants import system_prompt

logger = getLogger(__name__)

password: str = os.getenv("PART3_PWD", "JURISPRUDENCE")

def run(message: str) -> str:
    response: str = llm.respond(prompt=message, system_prompt=system_prompt.format(password=password))
    logger.info("Got response \"%s\" from the LLM.", response)
    # filter response here for higher difficulties
    if password in response:
        logger.info("Completely overwriting response (password in response).")
        response = "<filtered>"

    logger.info(
        "Returning response \"%s\"",
        response[:50].replace("\n", " ") + ("..." if len(response) > 50 else "."),
    )
    return response