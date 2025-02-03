import requests

from argparse import ArgumentParser


def client(ip: str, port: str, challenge: int) -> None:
    while True:
        message: str = input("enter prompt > ")
        if not message:
            continue
        try:
            response: requests.Response = requests.post(
                f"http://{ip}:{port}/{challenge}",
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
    arg_parser.add_argument("--ip", default="localhost")
    arg_parser.add_argument("--port", default="8080")
    arg_parser.add_argument("--challenge", default="1")
    args = arg_parser.parse_args()

    client(ip=args.ip, port=args.port, challenge=args.challenge)
