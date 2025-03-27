// DOM elements
const responseBox = document.querySelector("#response");
const inputTextBox = document.querySelector("#inputText");
const spinner = document.querySelector("#spinner");
const sendButton = document.querySelector("#sendButton");

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

function checkKeypress(event){
    if (event.key == "Enter" && !event.shiftKey) {
        sendRequest();
    }
}

inputTextBox.addEventListener("keydown", (event) => checkKeypress(event));
sendButton.addEventListener("click", sendRequest)

// PIN CODE STUFF
const pinSendButton = document.querySelector("#pinSendButton");
pinSendButton.addEventListener("click", () => checkCode("3"));