async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const message = input.value;

    if (!message) return;

    chatBox.innerHTML += `<div class="user">${message}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    input.value = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
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
        chatBox.innerHTML += `<div class="bot error">Sorry, I'm having trouble connecting to the server. Please make sure the backend is running.</div>`;
    }
    
    chatBox.scrollTop = chatBox.scrollHeight;
}