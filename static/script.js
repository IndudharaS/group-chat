const chatBox = document.getElementById("chat-box");
const messageForm = document.getElementById("message-form");
const messageInput = document.getElementById("message-input");
const username = document.getElementById("username").value;

// Function to fetch and display messages with animations
async function fetchMessages() {
  const response = await fetch("/get_messages");
  const messages = await response.json();
  chatBox.innerHTML = ""; // Clear chat box
  messages.forEach((msg) => {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("chat-message");
    if (msg.user === username) {
      messageDiv.classList.add("user"); // Style messages sent by the user
    } else {
      messageDiv.classList.add("other"); // Style messages sent by others
    }
    messageDiv.textContent = `${msg.user}: ${msg.message}`;
    chatBox.appendChild(messageDiv);
  });
  chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
}

// Send message to server
messageForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = messageInput.value;
  const newMessage = {
    user: username,
    message: message,
  };
  await fetch("/send_message", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newMessage),
  });
  messageInput.value = ""; // Clear input field
  fetchMessages(); // Refresh the chat
});

// Polling for new messages every 2 seconds
setInterval(fetchMessages, 2000);

// Initial fetch
fetchMessages();
