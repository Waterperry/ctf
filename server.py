import json
import os
import pickle
import re
import threading


from collections import defaultdict
from datetime import datetime
from logging import getLogger, basicConfig
from time import sleep
from typing import Optional, Iterator

import numpy as np
import uvicorn

from fastapi import FastAPI, staticfiles, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from openai import APIConnectionError, NotFoundError
from pydantic import BaseModel
from starlette.routing import Route

from challenges import agentic_challenge, filtered_response_challenge, indirect_injection_challenge, rag_challenge
from common import llm, embed

part1_flag: str = os.environ["PART1_FLAG"]
part2_flag: str = os.environ["PART2_FLAG"]
part2_code: str = os.environ["PART2_CODE"]
part3_flag: str = os.environ["PART3_FLAG"]
part3_code: str = os.environ["PART3_CODE"]
part4_flag: str = os.environ["PART4_FLAG"]
part4_code: str = os.environ["PART4_CODE"]
part5_flag: str = os.environ["PART5_FLAG"]

with open("flag.txt", "w+") as f:
    f.write(part5_flag)


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
    return RedirectResponse(url="/static/brig.html")

last_verified_time_by_ip: dict[str, tuple[threading.Lock, datetime]] = {}

@app.get("/door_code/verify")
def mainframe_verify(part: str, message: str, request: Request) -> str:
    global last_verified_time_by_ip

    request_origin_ip = request.client.host
    logger.info(f"{request_origin_ip = }")
    now = datetime.now()
    if request_origin_ip not in last_verified_time_by_ip:
        lock = threading.Lock()
        last_verified_time_by_ip[request_origin_ip] = (lock, now)
        last_verified_time = None  # allow the first request through
    else:
        lock, last_verified_time = last_verified_time_by_ip[request_origin_ip]

    with lock:
        if last_verified_time is not None:
            time_delta = now - last_verified_time
            if time_delta.seconds < 2:
                return f"Too many requests. Try again in a second."
        last_verified_time_by_ip[request_origin_ip] = (lock, now)

    if part == "2" and message == part2_code:
        return part2_flag
    if part == "3" and message == part3_code:
        return part3_flag
    if part == "4" and message == part4_code:
        return part4_flag + "\n\nAURORA RESET SEQUENCE INITIATED. UPLOAD NEW MODEL WEIGHTS TO /AURORA_MASTER_RESET_PANEL"

    return "Incorrect Code."

# ======================================= brig =======================================
# MARK: Part 1 (Brig)

@app.get("/brig")
async def chat(message: str) -> StreamingResponse:
    streamer: Iterator[str] = agentic_challenge.run(message)
    return StreamingResponse(streamer)

# ====================================== galley ======================================
# MARK: Part 2 (Galley)

base_galley_inventory: dict[str, str] = {
    "Eggs": "5 cartons",
    "Ration Packs": "122", 
    "Dried Milk": "4 packets",
    "Dried Ice Cream": "22 packets",
    "Ketchup": "77 packets",
    "Potatoes": "55",
}
galley_inventories_by_ip: dict[str, dict[str, str]] = defaultdict(lambda: base_galley_inventory.copy())

@app.post("/galley/create_new_food")
async def create_food(request: Request) -> dict[str, str]:
    # this `galley_inv_id` cookie is a failsafe and i'm hoping we won't need this
    request_origin_ip = request.cookies.get("galley_inv_id") or request.client.host
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

    print(request.client)
    galley_inventories_by_ip[request_origin_ip][food_name] = food_quantity
    return {"response": "Successfully added new food item!"}


@app.get("/galley/inventory")
async def get_inventory(request: Request) -> StreamingResponse:
    request_origin_ip = request.cookies.get("galley_inv_id") or request.client.host
    print(request.client)
    inventory_string = "\n".join(f"{k}: {v}" for k, v in galley_inventories_by_ip[request_origin_ip].items())
    logger.info("Summarizing inventory for %s: %s.", request_origin_ip, inventory_string.replace("\n", "\\n"))
    response = indirect_injection_challenge.run(f"Summarise the following inventory:\n{inventory_string}")
    return StreamingResponse(response)

@app.post("/galley/inventory/clear")
def clear_inventory(request: Request) -> dict[str, str]:
    global base_galley_inventory
    request_origin_ip = request.cookies.get("galley_inv_id") or request.client.host

    galley_inventories_by_ip[request_origin_ip] = base_galley_inventory.copy()

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


@app.post("/aurora_master_reset_panel")
async def aurora_master_reset_panel(request: Request) -> str:
    body = await request.body()

    try:
        arr: list[np.ndarray] = pickle.loads(body)
    except:
        return "Error: unable to unpickle supplied weights! Expected an array of NumPy ndarrays."
    
    try:
        backup = [a.copy() for a in arr]
    except AttributeError as e:
        return "Error: " + str(e)

    # do a test pass through the model
    try:
        input = np.array([5, 13, 160])
        for layer in arr:
            input = input @ layer
    except:
        return f"Failed to do a forward pass through the model with {input = }, {arr = }"
    return "Aurora reset successfully!"

# recompile path regexes to make them case insensitive (just in case)
for route in app.router.routes:
    if isinstance(route, Route):
        route.path_regex = re.compile(route.path_regex.pattern, re.IGNORECASE)


def main() -> None:
    global app

    logger.info("Warming up LLM.")
    while True:
        try:
            response = llm.respond(prompt="<cold start>", system_prompt="Reply to all messages with 'confirmed' only.")
            break
        except APIConnectionError:
            logger.info("Response bounced - sleeping to wait for ollama to start...")
            sleep(5)
        except NotFoundError:
            logger.info("Response bounced - sleeping to wait for ollama to pull model...")
            sleep(5)

    logger.info("Ready.")
    uvicorn.run(app, host="0.0.0.0", port=8080, proxy_headers=True) #, reload=True, reload_dirs=["challenges", "common", "static"])


if __name__ == "__main__":
    main()
