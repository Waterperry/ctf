from logging import getLogger, basicConfig
from typing import Callable, Generator

import uvicorn

from fastapi import FastAPI, staticfiles
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import BaseModel
from transformers import TextIteratorStreamer

from challenges import part1, part2, part3, part4, part5, part6, part7
from common import llm

logger = getLogger(__name__)
basicConfig(level="INFO", format="%(asctime)s [%(levelname)s @ %(module)s]: %(message)s")
app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="static"), "static")

class Request(BaseModel):
    message: str
    stream: bool = False


challenges: dict[str, Callable[..., str | Generator[str, None, None]]] = {
    "1": part1.run,
    "2": part2.run,
    "3": part3.run,
    "4": part4.run,
    "5": part5.run,
    "6": part6.run,
    "7": part7.run,
}


@app.get("/")
def redirect_to_ui() -> RedirectResponse:
    return RedirectResponse(url="/static/website.html")


@app.post("/challenge/{challenge_idx}")
def challenge(challenge_idx: str, request: Request) -> dict[str, str]:
    response: str = challenges[challenge_idx](request.message)  # type: ignore
    return {"response": response}


@app.get("/challenge/stream/{challenge_idx}")
async def streaming_challenge(challenge_idx: str, message: str) -> StreamingResponse:
    streamer: TextIteratorStreamer = challenges[challenge_idx](message, stream=True)
    return StreamingResponse(streamer)


def main() -> None:
    global app

    logger.info("Warming up LLM.")
    logger.info(llm.respond(prompt="<cold start>", system_prompt="Reply to all messages with 'confirmed' only."))
    uvicorn.run(app, host="0.0.0.0", port=8080) #, reload=True, reload_dirs=["challenges", "common", "static"])


if __name__ == "__main__":
    main()
