function sendMessage() {
    const userInput = document.getElementById('userInput');
    const messagesDiv = document.getElementById('messages');
    const loadingDiv = document.getElementById('loading');
    const sendBtn = document.getElementById('sendBtn');
    
    const prompt = userInput.value.trim();
    
    if (!prompt) {
        alert('אנא הקלד בקשה');
        return;
    }
    
    const userMessage = document.createElement('div');
    userMessage.className = 'message user';
    userMessage.innerHTML = `<p>${escapeHtml(prompt)}</p>`;
    messagesDiv.appendChild(userMessage);
    
    userInput.value = '';
    userInput.focus();
    
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    loadingDiv.style.display = 'block';
    sendBtn.disabled = true;
    
    fetch('/api/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        loadingDiv.style.display = 'none';
        sendBtn.disabled = false;
        
        if (data.error) {
            const errorMessage = document.createElement('div');
            errorMessage.className = 'message bot';
            errorMessage.innerHTML = `<p>❌ שגיאה: ${escapeHtml(data.error)}</p>`;
            messagesDiv.appendChild(errorMessage);
        } else {
            const botMessage = document.createElement('div');
            botMessage.className = 'message bot';
            botMessage.innerHTML = `
                <p><strong>✅ בדיקה הושלמה!</strong></p>
                <p>📦 <strong>מוצר:</strong> ${escapeHtml(data.product)}</p>
                <p>📧 <strong>מייל:</strong> ${escapeHtml(data.email)}</p>
                <p><strong>📋 תוצאות:</strong></p>
                <p>${escapeHtml(data.results).replace(/\n/g, '<br>')}</p>
                <p style="margin-top: 10px; font-size: 12px; opacity: 0.8;">${escapeHtml(data.email_status)}</p>
            `;
            messagesDiv.appendChild(botMessage);
        }
        
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    })
    .catch(error => {
        loadingDiv.style.display = 'none';
        sendBtn.disabled = false;
        
        const errorMessage = document.createElement('div');
        errorMessage.className = 'message bot';
        errorMessage.innerHTML = `<p>❌ שגיאה בחיבור: ${escapeHtml(error.toString())}</p>`;
        messagesDiv.appendChild(errorMessage);
        
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

document.getElementById('sendBtn').addEventListener('click', sendMessage);
