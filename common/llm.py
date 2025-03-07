import os

from logging import getLogger
from threading import Thread

from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

logger = getLogger(__name__)
model_name: str = os.environ["MODEL_NAME"]
model: AutoModelForCausalLM = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def respond(prompt: str, system_prompt: str) -> str:
    global model, tokenizer

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    logger.info("Applying chat template.")
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    logger.info(
        "Tokenizing input %s",
        prompt[:50].replace("\n", " ") + ("..." if len(prompt) > 50 else ""),
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    logger.info("Generating response.")
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512,
        temperature=1e-5,
    )
    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    logger.info("Decoding output.")
    response: str = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return response

def stream_generate(prompt: str, system_prompt: str) -> TextIteratorStreamer:
    """
    Return an Iterator object which yields chunks of text.
    This spawns a new thread in which the generation occurs, and so might cause problems with FastAPI...
    """
    global model, tokenizer

    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    logger.info("Applying chat template.")
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    logger.info(
        "Tokenizing input %s",
        prompt[:50].replace("\n", " ") + ("..." if len(prompt) > 50 else ""),
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    logger.info("Generating response.")
    generation_thread = Thread(target=model.generate, kwargs=dict(model_inputs, max_new_tokens=512, temperature=1e-5, streamer=streamer))
    generation_thread.start()

    return streamer
