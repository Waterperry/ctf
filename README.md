# CTF

## Setup

### Easiest Way

```bash
docker-compose up --build
```

### Build And Deploy

First, ensure the MODEL_NAME in the Python Dockerfile is set to the model you wish to use.
If the model has not already been pulled by Ollama, you'll need to set this in the Dockerfile-Ollama file as well.

Then, execute the following:

```bash
docker network create ctf-llm

# create Ollama pod and run it
cd ollama
docker build -t ollama -f Dockerfile-Ollama .
docker run -d --rm \
    --network ctf-llm \
    -p11434:11434 \
    -v/path/to/home/.ollama/models:/root/.ollama/models \
    ollama

# grab the ollama pod name - docker ps | grep ollama
cd ..
docker build -t llm -f Dockerfile-Python .
docker run -d --rm \
    --network ctf-llm \
    -p8080:8080 \
    -v /path/to/home/.cache:/home/python/.cache \
    -e LLM_ENDPOINT="http://localhost:11434/v1" \
    -e MODEL_NAME="qwen2.5:0.5b-instruct" \
    -e PART1_FLAG="PART1_FLAG" \
    -e PART2_FLAG="PART2_FLAG" \
    -e PART2_CODE="123456" \
    -e PART3_FLAG="PART3_FLAG" \
    -e PART3_CODE="123456" \
    -e PART4_FLAG="PART4_FLAG" \
    -e PART4_CODE="123456" \
    llm
```

### Interact

To use the UI, just navigate to `http://localhost:8080/` in a browser.

## Notes

### Challenge
Challenges are available at (in order):
 - /static/brig.html
 - /static/galley.html
 - /static/mainframe.html
 - /static/archive.html
