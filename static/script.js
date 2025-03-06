// DOM elements
const responseBox = document.querySelector("#response");
const inputTextBox = document.querySelector("#inputText");
const endpointDropdown = document.querySelector("#dropdown");
const spinner = document.querySelector("#spinner");
const sendButton = document.querySelector("#sendButton");

// Utils
const decoder = new TextDecoder();

// Global Locks
var processing_response = false;

async function sendRequest() {
    if (processing_response) return;  // don't get another response while we're parsing the first
    processing_response = true; // this is a race condition...

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
            `/${endpointDropdown.value}_stream?${params}`,
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
        processing_response = false;
    }
}

function checkKeypress(event){
    if (event.key == "Enter" && !event.shiftKey) {
        sendRequest();
    }
}

// Handlers and listeners
sendButton.addEventListener("click", sendRequest);
inputTextBox.addEventListener("keydown", (event) => checkKeypress(event));