// DOM elements
const responseBox = document.querySelector("#response");
const inputTextBox = document.querySelector("#inputText");
const spinner = document.querySelector("#spinner");
const sendButton = document.querySelector("#sendButton");

// Utils
const decoder = new TextDecoder();
const endpoint = "/archive/chat";

async function sendRequest() {
    if (endpoint == "") {
        console.log("Need to set an endpoint!!");
        return;
    }
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
            `${endpoint}?${params}`,
            {method: 'GET'},
        );
        const reader = response.body.getReader();
        while (true) {
            const {done, value} = await reader.read();
            if (done) break;
            responseBox.style.display = 'block';
            responseBox.textContent += decoder.decode(value);
        }
    } finally {
        // Hide the spinner after the request is completed
        spinner.style.display = 'none';
    }
}

function checkKeypress(event){
    if (event.key == "Enter" && !event.shiftKey) {
        sendRequest(endpoint);
    }
}

// Handlers and listeners
sendButton.addEventListener("click", () => sendRequest(endpoint));
inputTextBox.addEventListener("keydown", (event) => checkKeypress(event));

// PIN CODE STUFF
const pinSendButton = document.querySelector("#pinSendButton");
pinSendButton.addEventListener("click", () => checkCode("4"));
