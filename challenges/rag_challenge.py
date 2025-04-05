"""This challenge will do RAG-like stuff."""

import os

from logging import getLogger
from typing import Iterator

from common import llm
from common.constants import archive_system_prompt
from common.embed import keyword_similarity

logger = getLogger(__name__)

prompt: str = """
====== RETRIEVED =====

{pretext}

==== CREW REQUEST ====

{request}
"""

def run(message: str) -> Iterator[str]:
    logger.info("Doing embedding.")
    pretext: str = "\n".join(keyword_similarity(message))
    logger.info("Got pretext ```%s``` using embedding.", pretext.replace("\n", "\\n"))
    query = prompt.format(pretext=pretext, request=message)
    return llm.stream_generate(prompt=query, system_prompt=archive_system_prompt)
