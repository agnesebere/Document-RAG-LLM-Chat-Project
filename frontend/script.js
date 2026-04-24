async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const message = input.value;

    if (!message) return;

    chatBox.innerHTML += `<div class="user">${message}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    input.value = "";

    try {
        // Updated to use the Render cloud backend URL
        let response = await fetch("https://securebank-api-i53h.onrender.com/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                customer_id: "cust_001",
                message: message
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        chatBox.innerHTML += `<div class="bot">${data.answer}</div>`;
    } catch (error) {
        console.error("Error fetching chat response:", error);
        chatBox.innerHTML += `<div class="bot error">Connection Error: Could not reach the backend. <br><br> 1. Ensure all other terminal scripts are closed.<br> 2. Refresh the page.<br> 3. Check if the backend terminal shows any errors.</div>`;
    }
    
    chatBox.scrollTop = chatBox.scrollHeight;
}