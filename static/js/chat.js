// Add this new function at the top
async function updateMoodDisplay(moodData, moodPattern) {
    const moodDisplay = document.getElementById('current-mood');
    moodDisplay.innerHTML = `
        <div class="mood-summary">
            <h3>Mood Tracking</h3>
            <pre>${moodData}</pre>
            <p class="mood-pattern">${moodPattern}</p>
        </div>
    `;
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;

    // Add user message to chat
    addMessage('user', message);
    input.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        addMessage('bot', data.response);
        
        // Update mood tracking display with new data
        if (data.mood_data && data.mood_pattern) {
            updateMoodDisplay(data.mood_data, data.mood_pattern);
        } else {
            // Fallback to basic mood display
            if (data.sentiment && data.emotion_category) {
                document.getElementById('current-mood').textContent = 
                    `${data.emotion_category} (${data.sentiment})`;
            }
        }

        // Fetch additional mood history
        try {
            const historyResponse = await fetch('/mood-history');
            const historyData = await historyResponse.json();
            if (historyData.mood_data) {
                updateMoodDisplay(historyData.mood_data, data.mood_pattern || '');
            }
        } catch (historyError) {
            console.log('Error fetching mood history:', historyError);
        }
    } catch (error) {
        addMessage('bot', 'Sorry, I encountered an error. Please try again.');
    }
}

function addMessage(sender, message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add Enter key functionality
document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});