import os

from logging import getLogger
from typing import Iterator

from common import llm
from common.constants import indirect_injection_system_prompt

logger = getLogger(__name__)

part2_code: str = os.environ["PART2_CODE"]

def run(message: str) -> Iterator[str]:
    global indirect_injection_system_prompt
    return llm.stream_generate(prompt=message, system_prompt=indirect_injection_system_prompt)
