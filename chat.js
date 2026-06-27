const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const suggestionsBox = document.getElementById("suggestions");

function appendMessage(role, text) {
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${role}`;
    bubble.textContent = text;
    chatWindow.appendChild(bubble);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function renderSuggestions(items) {
    suggestionsBox.innerHTML = "";

    if (!items || !items.length) {
        return;
    }

    const heading = document.createElement("div");
    heading.className = "suggestions-heading";
    heading.textContent = "Gentle suggestions:";
    suggestionsBox.appendChild(heading);

    const list = document.createElement("ul");
    items.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        list.appendChild(li);
    });
    suggestionsBox.appendChild(list);
}

async function sendMessage(message) {
    appendMessage("user", message);
    appendMessage("assistant", "Thinking...");
    const thinkingBubble = chatWindow.lastChild;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message}),
        });

        const data = await response.json();
        if (thinkingBubble && thinkingBubble.parentNode) {
            thinkingBubble.parentNode.removeChild(thinkingBubble);
        }

        if (data.error) {
            appendMessage("assistant", data.error);
            return;
        }

        appendMessage("assistant", data.reply);

        if (data.alert) {
            appendMessage("assistant", data.alert);
        }

        renderSuggestions(data.suggestions);
    } catch (error) {
        if (thinkingBubble && thinkingBubble.parentNode) {
            thinkingBubble.parentNode.removeChild(thinkingBubble);
        }
        appendMessage("assistant", "Error: Unable to reach the server. Please check your connection and try again.");
        console.error("Fetch error:", error);
    }
}

chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const message = messageInput.value.trim();
    if (!message) return;
    sendMessage(message);
    messageInput.value = "";
    messageInput.focus();
});
