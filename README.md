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

To send a single message (configurable in the Python script so you can add new-lines etc.):
```bash
python3 scripts/send_single_message.py
```

## Notes

### Challenge
The Dockerfiles have some environment variables that control the challenge difficulty. Set them to 1 to enable, or anything else to disable.
