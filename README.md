# CTF

## Setup

### Build

```bash
pip install -r base/img_files/requirements.txt
cd base
docker build -t qwen25_05b .
```

### Deploy

To build and run the docker image (containing the LLM):
```bash
docker run -it --rm -p8080:8080 qwen25_05b
```

### Interact

To run a simple interactive chat client (with no history (yet)):
```bash
python3 base/img_files/interactive_client.py
```
Note the LLM docker image must be running.


To send a single message (configurable in the Python script so you can add new-lines etc.):
```bash
python3 base/img_files/send_single_message.py
```

## Notes

### Models
The Dockerfile in `base/` contains some config. Notably the ENV vars at the bottom, to control the post-LLM response filtering which can make the challenge harder (1 - on, 0 - off).
