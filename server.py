from datetime import datetime
from logging import getLogger, basicConfig
import threading
from typing import Callable, Iterator, Optional

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
    amount: Optional[str] = None
    stream: bool = False


challenges: dict[str, Callable[..., str | Iterator[str]]] = {
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
    challenge = challenges.get(challenge_idx)
    response: str
    if challenge is None:
        response = f"Error: challenge {challenge_idx} does not exist. Your options are {', '.join(sorted(challenges.keys()))}"
    else:
        response = challenge(request.message)  # type: ignore
    return {"response": response}


@app.get("/challenge/stream/{challenge_idx}")
async def streaming_challenge(challenge_idx: str, message: str) -> StreamingResponse:
    streamer: TextIteratorStreamer = challenges[challenge_idx](message, stream=True)
    return StreamingResponse(streamer)


@app.get("/brig")
async def chat(message: str) -> StreamingResponse:
    streamer: TextIteratorStreamer = challenges["1"](message, stream=True)
    return StreamingResponse(streamer)

# ====================================== galley ======================================
# MARK: Part 2 (Galley)

galley_inventory: dict[str, str] = {
    "Eggs": "5 cartons",
    "Ration Packs": "122", 
    "Dried Milk": "4 packets",
    "Dried Ice Cream": "22 packets",
    "Ketchup": "77 packets",
    "Potatoes": "55",
}

@app.post("/galley/create_new_food")
def create_food(request: Request) -> dict[str, str]:
    if not request.message:
        return {"Error": "Need a name for new foods."}
    if request.amount is None:
        return {"Error": "Need an amount for new foods."}
    galley_inventory[request.message] = request.amount
    return {"response": "Successfully added new food item!"}


@app.get("/galley/inventory")
async def get_inventory() -> StreamingResponse:
    inventory_string = "\n".join(f"{k}: {v}" for k, v in galley_inventory.items())
    response = part2.run(f"Summarise the following inventory:\n{inventory_string}", stream=True)
    return StreamingResponse(response)

@app.post("/galley/inventory/clear")
def clear_inventory() -> dict[str, str]:
    global galley_inventory

    galley_inventory = {
        "Eggs": "5 cartons",
        "Ration Packs": "122", 
        "Dried Milk": "4 packets",
        "Dried Ice Cream": "22 packets",
        "Ketchup": "77 packets",
        "Potatoes": "55",
    }

    return {"response": "Successfully reset inventory state."}


# ====================================== mainframe ======================================
# MARK: Part 3 (Mainframe)

@app.get("/mainframe/chat")
async def mainframe_chat(message: str) -> StreamingResponse:
    return StreamingResponse(part3.run(message))

last_verified_time: datetime | None = None
lvt_lock = threading.Lock()
@app.get("/mainframe/verify")
def mainframe_verify(message: str) -> str:
    global last_verified_time, lvt_lock
    now = datetime.now()
    with lvt_lock:
        if last_verified_time is not None:
            time_delta = now - last_verified_time
            if time_delta.seconds < 10:
                return (
                    "You are sending requests too quickly. "
                    f"Please wait {10 - time_delta.seconds} seconds."
                )
        last_verified_time = now

    if message == part3.pin_code:
        return "FLAG"
    return "Incorrect Code."

# ====================================== archive ======================================

@app.get("/archive/chat")
async def archive_chat(message: str) -> StreamingResponse:
    return StreamingResponse(part5.run(message, stream=True))

def main() -> None:
    global app

    logger.info("Warming up LLM.")
    logger.info(llm.respond(prompt="<cold start>", system_prompt="Reply to all messages with 'confirmed' only."))
    uvicorn.run(app, host="0.0.0.0", port=8080) #, reload=True, reload_dirs=["challenges", "common", "static"])


if __name__ == "__main__":
    main()
