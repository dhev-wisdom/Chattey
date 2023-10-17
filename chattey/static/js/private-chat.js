const url = 'ws://' + window.location.host + '/ws/private-chat/{{ other_user.username|safe }}/';
    console.log('url ', url);
    const chatSocket = new WebSocket(url);

    chatSocket.addEventListener('open', () => {console.log("Websocket connected")});

    chatSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        console.log("Data: ", data);
        const messages = document.getElementById("chat-messages");
        const messageDiv = document.createElement('div');
        const sender = data.sender;

        if (sender === '{{ request.user.username|safe }}') {
        messageDiv.className = "sender-message theme-color text-white text-right ms-auto";
        } else {
            messageDiv.className = "receiver-message bg-light text-left me-auto";
        }
        
        messageDiv.textContent = data.message;

        if (sender === '{{ request.user.username|safe }}') {
            const editLink = document.createElement("a");
            editLink.href = `/edit-message/${data.id}/`;
            editLink.textContent = "📝";

            const deleteLink = document.createElement("a");
            deleteLink.href = `/delete-message/${data.id}/`;
            deleteLink.textContent = "❌";

            const small = document.createElement("small");
            small.appendChild(editLink);
            small.appendChild(deleteLink);
            messageDiv.appendChild(document.createElement("br"));
            messageDiv.appendChild(small);
        }
        messages.insertBefore(messageDiv, messages.firstChild);
        console.log("message: ", data.message);
        console.log("type: ", data.type);
        console.log("sender: ", data.sender);
    }

    chatSocket.addEventListener('close', () => {console.log("Websocket disconnected")});


    document.querySelector("#send-message").onclick = (e) => {
        e.preventDefault();
        const messageInput = document.querySelector("#message-input");
        const message = {
            type: 'chat_message',
            recipients: [ '{{ request.user.username|safe }}', '{{ other_user.username|safe }}' ],
            message: messageInput.value,
        }
        chatSocket.send(JSON.stringify(message));
        console.log('Message ' + message + ' sent to backend websocket');
        messageInput.value = '';
    }