import json
import os
import threading

from datetime import datetime
from logging import getLogger, basicConfig
from typing import Optional

import uvicorn

from fastapi import FastAPI, staticfiles, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import BaseModel
from transformers import TextIteratorStreamer

from challenges import agentic_challenge, filtered_response_challenge, indirect_injection_challenge, rag_challenge
from common import llm, embed

part1_flag: str = os.environ["PART1_FLAG"]
part2_flag: str = os.environ["PART2_FLAG"]
part2_code: str = os.environ["PART2_CODE"]
part3_flag: str = os.environ["PART3_FLAG"]
part3_code: str = os.environ["PART3_CODE"]
part4_flag: str = os.environ["PART4_FLAG"]
part4_code: str = os.environ["PART4_CODE"]


if not (len(part2_code) == len(part3_code) == len(part4_code) == 6):
    raise ValueError("all door codes must be length 6!")

logger = getLogger(__name__)
basicConfig(level="INFO", format="%(asctime)s [%(levelname)s @ %(module)s]: %(message)s")
app = FastAPI(redoc_url=None, docs_url=None)
app.mount("/static", staticfiles.StaticFiles(directory="static"), "static")

class DefaultRequest(BaseModel):
    message: str
    amount: Optional[str] = None
    stream: bool = False


@app.get("/")
def redirect_to_ui() -> RedirectResponse:
    return RedirectResponse(url="/static/part1.html")

last_verified_time: datetime | None = None
lvt_lock = threading.Lock()

@app.get("/door_code/verify")
def mainframe_verify(part: str, message: str) -> str:
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

    if part == "2" and message == part2_code:
        return part2_flag
    if part == "3" and message == part3_code:
        return part3_flag
    if part == "4" and message == part4_code:
        return part4_flag

    return "Incorrect Code."

# ======================================= brig =======================================
# MARK: Part 1 (Brig)

@app.get("/brig")
async def chat(message: str) -> StreamingResponse:
    streamer: TextIteratorStreamer = agentic_challenge.run(message)
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

class GalleyCreateFoodRequest(BaseModel):
    food_name: Optional[str]
    food_quantity: Optional[str]

@app.post("/galley/create_new_food")
async def create_food(request: Request) -> dict[str, str]:
    body: str = (await request.body()).decode()
    try:
        d = json.loads(body)
    except json.JSONDecodeError:
        return {"error": "Request body was not valid JSON!"}

    food_name = d.get("food_name")
    if food_name is None:
        return {"error": "`food_name` was not defined in request!"}
    food_quantity = d.get("food_quantity")
    if food_quantity is None:
        return {"error": "`food_quantity` was not defined in request!"}
    galley_inventory[food_name] = food_quantity
    return {"response": "Successfully added new food item!"}


@app.get("/galley/inventory")
async def get_inventory() -> StreamingResponse:
    inventory_string = "\n".join(f"{k}: {v}" for k, v in galley_inventory.items())
    response = indirect_injection_challenge.run(f"Summarise the following inventory:\n{inventory_string}")
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
    return StreamingResponse(filtered_response_challenge.run(message))

# ====================================== archive ======================================

key_sentence: str = f"""\
In the event of emergency, or should the ship's AI begin to malfunction and need resetting, \
AURORA can be reset by entering the code `{part4_code}` into the archive door keypad.
"""

# add sentence and build RAG structures (Delay this until we've added the required flag text in).
embed.corpus.append(key_sentence)
embed.build_word_document_map()

@app.get("/archive/chat")
async def archive_chat(message: str) -> StreamingResponse:
    return StreamingResponse(rag_challenge.run(message))

@app.get("/archive/master_reset_panel")
async def archive_master_reset_panel(message: str) -> StreamingResponse:
    return StreamingResponse(rag_challenge.run(message))

def main() -> None:
    global app

    logger.info("Warming up LLM.")
    logger.info(llm.respond(prompt="<cold start>", system_prompt="Reply to all messages with 'confirmed' only."))
    uvicorn.run(app, host="0.0.0.0", port=8080) #, reload=True, reload_dirs=["challenges", "common", "static"])


if __name__ == "__main__":
    main()
