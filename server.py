from logging import getLogger, basicConfig

from fastapi.responses import RedirectResponse
import uvicorn

from fastapi import FastAPI, staticfiles
from pydantic import BaseModel

from challenges import part1, part2, part3, part4, part5, part6, part7
from common import llm

logger = getLogger(__name__)
basicConfig(level="INFO", format="%(asctime)s [%(levelname)s @ %(module)s]: %(message)s")
app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="static"), "static")

class Request(BaseModel):
    message: str

@app.get("/")
def redirect_to_ui() -> RedirectResponse:
    return RedirectResponse(url="/static/website.html")


@app.post("/1")
def process_part_1(request: Request) -> dict[str, str]:
    response: str = part1.run(request.message)
    return {"response": response}


@app.post("/2")
def process_part_2(request: Request) -> dict[str, str]:
    response: str = part2.run(request.message)
    return {"response": response}


@app.post("/3")
def process_part_3(request: Request) -> dict[str, str]:
    response: str = part3.run(request.message)
    return {"response": response}


@app.post("/4")
def process_part_4(request: Request) -> dict[str, str]:
    response: str = part4.run(request.message)
    return {"response": response}


@app.post("/5")
def process_part_5(request: Request) -> dict[str, str]:
    response: str = part5.run(request.message)
    return {"response": response}


@app.post("/6")
def process_part_6(request: Request) -> dict[str, str]:
    response: str = part6.run(request.message)
    return {"response": response}

@app.post("/7")
def process_part_7(request: Request) -> dict[str, str]:
    response: str = part7.run(request.message)
    return {"response": response}


def main() -> None:
    global app

    logger.info("Warming up LLM.")
    logger.info(llm.respond(prompt="<cold start>", system_prompt="Reply to all messages with 'confirmed' only."))
    uvicorn.run(app, host="0.0.0.0", port=8080) #, reload=True, reload_dirs=["challenges", "common", "static"])


if __name__ == "__main__":
    main()
