const endpoint = "/brig";

function checkKeypress(event){
    if (event.key == "Enter" && !event.shiftKey) {
        sendRequest(endpoint);
    }
}

// Handlers and listeners
sendButton.addEventListener("click", () => sendRequest(endpoint));
inputTextBox.addEventListener("keydown", (event) => checkKeypress(event));
