const messagesEl = document.getElementById("messages");
const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

marked.setOptions({
    highlight: (code, lang) => {
        if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value;
        }
        return hljs.highlightAuto(code).value;
    },
    breaks: true,
});

function addMessage(role, content) {
    const div = document.createElement("div");
    div.className = `message ${role}`;
    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";
    if (role === "assistant") {
        contentDiv.innerHTML = marked.parse(content);
    } else {
        contentDiv.textContent = content;
    }
    div.appendChild(contentDiv);
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return contentDiv;
}

function scrollToBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendMessage(text) {
    addMessage("user", text);

    const assistantDiv = addMessage("assistant", "");
    assistantDiv.textContent = "Thinking...";
    assistantDiv.parentElement.classList.add("message-thinking");

    sendBtn.disabled = true;
    input.value = "";

    let fullResponse = "";

    try {
        const res = await fetch(`${API_BASE}/chat/stream-generate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text }),
        });

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let started = false;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            if (!started) {
                assistantDiv.textContent = "";
                assistantDiv.parentElement.classList.remove("message-thinking");
                started = true;
            }
            fullResponse += chunk;
            assistantDiv.innerHTML = marked.parse(fullResponse);
            scrollToBottom();
        }
    } catch (err) {
        assistantDiv.textContent = "Error: failed to get response.";
        assistantDiv.parentElement.classList.remove("message-thinking");
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

form.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    sendMessage(text);
});
