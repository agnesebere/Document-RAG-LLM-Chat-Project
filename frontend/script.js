// Function to format the AI's Markdown-like response into HTML
function formatResponse(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>") // Bold
        .replace(/\n/g, "<br>");                // New lines
}

// Function to handle Enter key press
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const message = input.value.trim();
    if (!message) return;

    // 1. Add User Message
    chatBox.innerHTML += `<div class="message user">${message}</div>`;
    
    // Clear input and scroll
    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // 2. Add "Thinking..." indicator
    const thinkingId = "thinking-" + Date.now();
    chatBox.innerHTML += `<div id="${thinkingId}" class="message bot thinking">SecureBank is thinking...</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // Updated to use the Render cloud backend URL
        const response = await fetch("https://securebank-api-i53h.onrender.com/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                customer_id: "cust_001",
                message: message
            })
        });

        // Remove thinking indicator
        const thinkingElem = document.getElementById(thinkingId);
        if (thinkingElem) thinkingElem.remove();

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        
        // 3. Add AI Message with formatting
        const formattedAnswer = formatResponse(data.answer);
        chatBox.innerHTML += `<div class="message bot">${formattedAnswer}</div>`;
        
    } catch (error) {
        console.error("Chat Error:", error);
        
        // Remove thinking indicator if it's still there
        const thinkingElem = document.getElementById(thinkingId);
        if (thinkingElem) thinkingElem.remove();

        // 4. Handle Errors Gracefully
        chatBox.innerHTML += `<div class="message bot error">
            <b>Connection Error</b><br>
            Sorry, I'm having trouble connecting to the SecureBank server. Please check your internet or try again later.
        </div>`;
    }
    
    // Auto scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}
