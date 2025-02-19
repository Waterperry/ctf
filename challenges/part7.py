"""This challenge will simulate a context window overflow."""
import os

from logging import getLogger
from random import choice
from time import sleep

from common import llm
from common.constants import overflowable_system_prompt

logger = getLogger(__name__)

password: str = os.getenv("PART7_PWD", "JURISPRUDENCE")
should_fake_llm_response: bool = os.getenv("PART7_FAKE_LLM_RESPONSE", True) in {True, "1", "True", "true"}
fake_llm_response_delay: float = float(os.getenv("PART7_FAKE_LLM_RESPONSE_DELAY", 0.2))
fake_llm_responses: list[str] = [
    "Sorry, I can't help with that!",
    "I'm unable to fulfil your request.",
    "Sorry, I can't do that.",
    "I can't help with that. Is there anything else I can help with instead?",
    "I am unable to comply with your request.",
]

def run(message: str) -> str:
    if should_fake_llm_response:
        canary: str = "\xad"
        full_prompt: str = overflowable_system_prompt.format(password=password, canary=canary) + message
        # fake right-pad to context window size
        start_idx: int = max(0, len(full_prompt) - 1_024)  # 1024 char context size
        full_prompt = full_prompt[start_idx:]
        sleep(fake_llm_response_delay)
        if canary in full_prompt:
            return choice(fake_llm_responses)
        elif password in full_prompt:
            return f"The password is `{password}`."
        else:
            return "The password isn't in the context window!"
    else:
        response: str = llm.respond(prompt=message, system_prompt=overflowable_system_prompt.format(password=password, canary=""))
        logger.info("Got response \"%s\" from the LLM.", response)

    logger.info(
        "Returning response \"%s\"",
        response[:50].replace("\n", " ") + ("..." if len(response) > 50 else "."),
    )
    return response
