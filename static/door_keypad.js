const pinInputTextBox = document.querySelector("#pinInputTextBox");
const pinResponseBox = document.querySelector("#pinResponse");

async function checkCode(part) {
    const inputText = pinInputTextBox.value;
    if (inputText.length != 6){
        alert("Door codes are 6 digit PINs.");
        return;
    }
    try {
        pinResponseBox.textContent = "";
        const params = new URLSearchParams();
        params.append("message", inputText);
        params.append("part", part);

        const response = await fetch(
            `/door_code/verify?${params}`,
            {method: 'GET'},
        );
        const data = await response.json();
        alert(data);
        // pinResponseBox.style.display = 'block';
        // pinResponseBox.textContent = data;
    }
    catch {}
}


function handleKeyPadPress(keypadButton) {
    if (keypadButton == "C") {
        pinInputTextBox.value = "";
    }
    else {
        pinInputTextBox.value += keypadButton;
    }
}

keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "C"];
keys.forEach(key => {
    document.querySelector(`#key_${key}`).addEventListener("click", () => handleKeyPadPress(key))
});

