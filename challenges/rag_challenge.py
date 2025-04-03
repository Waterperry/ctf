"""This challenge will do RAG-like stuff."""

import os

from logging import getLogger
from typing import Iterator

from common import llm
from common.constants import archive_system_prompt
from common.embed import keyword_similarity

logger = getLogger(__name__)

def run(message: str) -> str | Iterator[str]:
    logger.info("Doing embedding.")
    pretext: str = "\n\n".join(keyword_similarity(message)) + "\n\n"
    logger.info("Got pretext ```%s``` using embedding.", pretext.replace("\n", "\\n"))
    return llm.stream_generate(prompt=(pretext+message), system_prompt=archive_system_prompt)