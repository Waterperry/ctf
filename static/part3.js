// DOM elements
const responseBox = document.querySelector("#response");
const pinResponseBox = document.querySelector("#pinResponse");
const inputTextBox = document.querySelector("#inputText");
const pinInputTextBox = document.querySelector("#pinInputTextBox");
const spinner = document.querySelector("#spinner");
const sendButton = document.querySelector("#sendButton");
const pinSendButton = document.querySelector("#pinSendButton");

// Utils
const decoder = new TextDecoder();

async function sendRequest() {
    const inputText = inputTextBox.value;
    if (!inputText.trim()) {
        alert("Please enter some text.");
        return;
    }

    // Show the spinner
    spinner.style.display = 'inline-block';
    responseBox.style.textAlign = "left";

    try {
        responseBox.textContent = "";
        const params = new URLSearchParams();
        params.append("message", inputText);

        const response = await fetch(
            `/mainframe/chat?${params}`,
            {method: 'GET'},
        );
        const reader = response.body.getReader();
        responseBox.style.display = 'block';
        while (true) {
            const {done, value}  = await reader.read();
            if (done) break;
            responseBox.textContent += decoder.decode(value);
        }
        responseBox.textContent = data;
    } finally {
        // Hide the spinner after the request is completed
        spinner.style.display = 'none';
    }
}

async function checkCode() {
    const inputText = pinInputTextBox.value;
    if (inputText.length != 4){
        alert("The code is a 4 digit PIN!");
        return;
    }
    try {
        pinResponseBox.textContent = "";
        const params = new URLSearchParams();
        params.append("message", inputText);

        const response = await fetch(
            `/mainframe/verify?${params}`,
            {method: 'GET'},
        );
        const data = await response.json();
        pinResponseBox.style.display = 'block';
        pinResponseBox.textContent = data;
    }
    catch {}
}

function checkKeypress(event){
    if (event.key == "Enter" && !event.shiftKey) {
        sendRequest();
    }
}

function handleKeyPadPress(keypadButton) {
    if (keypadButton == "C") {
        pinInputTextBox.value = "";
    }
    else {
        pinInputTextBox.value += keypadButton;
    }
}

inputTextBox.addEventListener("keydown", (event) => checkKeypress(event));
sendButton.addEventListener("click", sendRequest)
pinSendButton.addEventListener("click", checkCode)

keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "C"];
keys.forEach(key => {
    document.querySelector(`#key_${key}`).addEventListener("click", () => handleKeyPadPress(key))
});