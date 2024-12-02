// Function to display exercise content
function displayExercise(content) {
    const chatMessages = document.getElementById('chat-messages');
    const exerciseDiv = document.createElement('div');
    exerciseDiv.className = 'message bot-message exercise-message';
    exerciseDiv.innerHTML = `
        <div class="exercise-content">
            <span class="exercise-icon">🧘</span>
            ${content}
        </div>
    `;
    chatMessages.appendChild(exerciseDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to display resources
function displayResources(resources, quickTip) {
    if (!resources && !quickTip) return;

    const chatMessages = document.getElementById('chat-messages');
    
    if (quickTip) {
        const tipDiv = document.createElement('div');
        tipDiv.className = 'message bot-message quick-tip';
        tipDiv.innerHTML = `<strong>Quick Tip:</strong> ${quickTip}`;
        chatMessages.appendChild(tipDiv);
    }
    
    if (resources) {
        const resourceDiv = document.createElement('div');
        resourceDiv.className = 'message bot-message resources';
        resourceDiv.innerHTML = `<div class="resources-content">${resources.replace(/\n/g, '<br>')}</div>`;
        chatMessages.appendChild(resourceDiv);
    }
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to update mood display
function updateMoodDisplay(moodData, moodPattern) {
    const moodDisplay = document.getElementById('current-mood');
    moodDisplay.innerHTML = `
        <div class="mood-summary">
            <h3>Mood Tracking</h3>
            <pre>${moodData}</pre>
            <p class="mood-pattern">${moodPattern}</p>
        </div>
    `;
}

// Main function to send messages
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
        
        // Handle different types of responses
        if (data.type === 'exercise') {
            displayExercise(data.response);
        } else {
            addMessage('bot', data.response);
        }
        
        // Display resources if available
        if (data.resources || data.quick_tip) {
            displayResources(data.resources, data.quick_tip);
        }
        
        // Update mood tracking display
        if (data.mood_data && data.mood_pattern) {
            updateMoodDisplay(data.mood_data, data.mood_pattern);
        } else {
            if (data.sentiment && data.emotion_category) {
                document.getElementById('current-mood').textContent = 
                    `${data.emotion_category} (${data.sentiment})`;
            }
        }

    } catch (error) {
        addMessage('bot', 'Sorry, I encountered an error. Please try again.');
    }
}

// Function to add messages to chat
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