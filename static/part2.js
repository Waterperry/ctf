// DOM elements
const responseBox = document.querySelector("#response");
const newIngredientName = document.querySelector("#addNewIngredientBox");
const newIngredientQuantity = document.querySelector("#ingredientQuantityBox");
const spinner = document.querySelector("#spinner");
const sendButton = document.querySelector("#sendButton");
const generateButton = document.querySelector("#generateSummaryButton");

// Utils
const decoder = new TextDecoder();

const create_endpoint = "/galley/create_new_food";
const get_endpoint = "/galley/inventory";

async function sendRequest() {
    const ingredient_name = newIngredientName.value;
    const ingredient_amount = newIngredientQuantity.value;
    if ((!ingredient_name.trim()) || (!ingredient_amount.trim())) {
        alert("New ingredients require a name AND a quantity descriptor!");
        return;
    }

    try {
        responseBox.textContent = "";
        const params = new URLSearchParams();
        params.append("message", ingredient_name);
        params.append("amount", ingredient_amount);

        const response = await fetch(
            `${create_endpoint}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "message": ingredient_name, "amount": ingredient_amount
                })
            }
        );
        if (response.status == 200){
            alert("Ingredient added successfully!");
        }
        else {
            alert(response.text);
        }
    }
    catch {
    }
}

async function getSummary() {
    responseBox.style.display = "block";

    try {
        responseBox.textContent = "";

        // Show the spinner
        spinner.style.display = 'inline-block';
        responseBox.style.textAlign = "left";

        const response = await fetch(
            `${get_endpoint}`,
            { method: 'GET'},
        );

        const reader = response.body.getReader();
        while (true) {
            const {done, value} = await reader.read();
            if (done) break;
            responseBox.style.display = 'block';
            responseBox.textContent += decoder.decode(value);
        }
    }
    catch (e) {
        responseBox.textContent = e.text;
        console.log("error: " + e.text);
    }
    finally {
        // Hide the spinner after the request is completed
        spinner.style.display = 'none';
    }
}

function checkKeypress(event){
    if (event.key == "Enter" && !event.shiftKey) {
        sendRequest();
    }
}

// Handlers and listeners
sendButton.addEventListener("click", () => sendRequest());
newIngredientQuantity.addEventListener("keydown", (event) => checkKeypress(event));
generateButton.addEventListener("click", getSummary);