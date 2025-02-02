# CTF

## Setup

### Build And Deploy (CPU)

```bash
pip install -r requirements.txt
docker build -t qwen25_05b -f Dockerfile-CPU .
docker run -it --rm -p8080:8080 qwen25_05b
```

### Build And Deploy (GPU)

```bash
pip install -r requirements.txt
docker build -t qwen25_05b -f Dockerfile-GPU .
docker run -it --rm -p8080:8080 --gpus all qwen25_05b
```

### Interact

To run a simple interactive chat client (with no history (yet)):
```bash
python3 scripts/interactive_client.py
```
Note the LLM docker image must be running.

To send a single message to each challenge endpoint (configurable in the Python script so you can add new-lines etc.):
```bash
python3 scripts/send_single_message.py
```

## Notes

### Challenge
The server now has several endpoints like /1, /2, ...
These correspond to the part of the challenge, and they all do different things (more info in the `challenge_overview.txt` file).
