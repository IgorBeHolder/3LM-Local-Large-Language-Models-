document.getElementById("chat-form").addEventListener("submit", function(event) {
    event.preventDefault(); // prevent page reload

    let userMessage = event.target.user_input.value;

    // Append user's message to chat history
    let userBubble = document.createElement("div");
    userBubble.textContent = userMessage;
    userBubble.style.backgroundColor = "#007BFF";
    userBubble.style.color = "white";
    userBubble.style.borderRadius = "5px";
    userBubble.style.padding = "10px";
    userBubble.style.marginBottom = "10px";
    document.getElementById("chat-history").appendChild(userBubble);

    // Scroll to the bottom of the chat history
    let chatHistory = document.getElementById("chat-history");
    chatHistory.scrollTop = chatHistory.scrollHeight;

    // TODO: Send the user's message to the backend using fetch or AJAX
    // Then receive the response and append it to the chat-history like above
    // but with a different bubble style.

    // Clear the input field after sending
    event.target.user_input.value = "";
});
