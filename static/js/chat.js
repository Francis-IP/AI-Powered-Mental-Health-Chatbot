// Add this new function at the top of your file
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

// Your existing sendMessage function should be updated to:
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

// Keep your existing addMessage function and event listener