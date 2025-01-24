import requests


def main() -> None:
    while True:
        message: str = input("enter prompt > ")
        if not message:
            continue
        try:
            response: requests.Response = requests.post(
                "http://localhost:8080/llm",
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
    main()
