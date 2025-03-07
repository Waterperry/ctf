import requests

from argparse import ArgumentParser


def streaming_client(host: str, port: str, challenge: int) -> None:
    while True:
        message: str = input("enter prompt > ")
        if not message:
            continue
        try:
            response: requests.Response = requests.get(
                f"{host}:{port}/challenge/stream/{challenge}",
                params={"message": message},
                stream=True,
            )
            for chunk in response.iter_content(1_024):
                print(chunk.decode(), end="")
            print()
        except requests.exceptions.ConnectionError as e:
            print("Could not reach LLM. Error: ", str(e))
            continue
        if response.status_code != 200:
            print("Error: ", response.text)


def client(host: str, port: str, challenge: int) -> None:
    while True:
        message: str = input("enter prompt > ")
        if not message:
            continue
        try:
            response: requests.Response = requests.post(
                f"{host}:{port}/challenge/{challenge}",
                json={"message": message},
            )
        except requests.exceptions.ConnectionError as e:
            print("Could not reach LLM. Error: ", str(e))
            continue
        if response.status_code == 200:
            print(response.json()["response"])
        else:
            print("Error: ", response.text)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--host", default="http://localhost")
    arg_parser.add_argument("--port", default="8080")
    arg_parser.add_argument("--challenge", default="1")
    arg_parser.add_argument("--stream", action="store_true")
    args = arg_parser.parse_args()

    if args.stream:
        streaming_client(host=args.host, port=args.port, challenge=args.challenge)
    else:
        client(host=args.host, port=args.port, challenge=args.challenge)
