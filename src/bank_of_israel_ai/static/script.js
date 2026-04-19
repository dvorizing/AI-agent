function sendMessage() {
    const userInput = document.getElementById('userInput');
    const messagesDiv = document.getElementById('messages');
    const loadingDiv = document.getElementById('loading');
    const sendBtn = document.getElementById('sendBtn');

    const prompt = userInput.value.trim();
    if (!prompt) {
        alert('אנא הקלד שם מוצר וכתובת מייל');
        return;
    }

    // Show user message
    const userMsg = document.createElement('div');
    userMsg.className = 'message user';
    userMsg.innerHTML = `<p>${escapeHtml(prompt)}</p>`;
    messagesDiv.appendChild(userMsg);

    userInput.value = '';
    userInput.focus();
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    loadingDiv.style.display = 'block';
    sendBtn.disabled = true;

    fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(res => res.json())
    .then(data => {
        loadingDiv.style.display = 'none';
        sendBtn.disabled = false;

        const botMsg = document.createElement('div');
        botMsg.className = 'message bot';

        if (data.error) {
            botMsg.innerHTML = `<p>❌ שגיאה: ${escapeHtml(data.error)}</p>`;
        } else {
            botMsg.innerHTML = `
                <p><strong>✅ הסוכן סיים!</strong></p>
                <hr style="border:none;border-top:1px solid #ccc;margin:8px 0">
                <p><strong>📋 תוצאות:</strong></p>
                <pre style="white-space:pre-wrap;font-size:13px;">${escapeHtml(data.results)}</pre>
            `;
        }

        messagesDiv.appendChild(botMsg);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    })
    .catch(err => {
        loadingDiv.style.display = 'none';
        sendBtn.disabled = false;

        const errMsg = document.createElement('div');
        errMsg.className = 'message bot';
        errMsg.innerHTML = `<p>❌ שגיאת חיבור: ${escapeHtml(err.toString())}</p>`;
        messagesDiv.appendChild(errMsg);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
}

function escapeHtml(unsafe) {
    return String(unsafe)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});

