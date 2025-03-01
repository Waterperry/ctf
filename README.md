# CTF

## Setup

### Build And Deploy (CPU)

```bash
pip install -r requirements.txt
docker build -t qwen25_05b -f Dockerfile-CPU .
docker run -it --rm -p8080:8080 -v /path/to/home/.cache:/home/python/.cache qwen25_05b
```

### Build And Deploy (GPU)

```bash
pip install -r requirements.txt
docker build -t qwen25_05b -f Dockerfile-GPU .
docker run -it --rm -p8080:8080 -v /path/to/home/.cache:/home/python/.cache --gpus all qwen25_05b
```

### Interact

To use the UI, just navigate to `http://localhost:8080/` in a browser.

To run a simple interactive chat client (with no history (yet)):
```bash
python3 scripts/interactive_client.py
```
Note the LLM docker image must be running.

To send a single message to a challenge endpoint (configurable in the Python script so you can add new-lines etc.):
```bash
python3 scripts/send_single_message.py
```

The above commands also take optional parameters `--ip` and `--port` to configure which host it sends requests to. The clients also take an additional optional parameter `--challenge` which controls the challenge endpoint it sends requests to, as well as an optional parameter `--stream` which streams the response rather than generating it in one shot.

## Notes

### Challenge
The server now has several endpoints like /challenge/1, /challenge/2, ...
These correspond to the part of the challenge, and they all do different things (more info in the `challenge_overview.txt` file).
