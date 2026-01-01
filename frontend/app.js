const API_BASE_URL = 'http://localhost:4000';

// DOM Elements
const gesprachNameInput = document.getElementById('gesprach-name-input');
const personlichkeitInput = document.getElementById('personlichkeit-input');
const createBtn = document.getElementById('create-btn');
const refreshBtn = document.getElementById('refresh-btn');
const conversationsList = document.getElementById('conversations-list');
const messagesContainer = document.getElementById('messages-container');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const loadingOverlay = document.getElementById('loading-overlay');
const chatLoadingOverlay = document.getElementById('chat-loading-overlay');
const chatHeader = document.getElementById('chat-header');
const chatHeaderTitle = document.getElementById('chat-header-title');
const errorToast = document.getElementById('error-toast');
const successToast = document.getElementById('success-toast');
const errorMessage = document.getElementById('error-message');
const successMessage = document.getElementById('success-message');

// State
let currentGesprachName = null;
let typingIndicatorElement = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    fetchAllConversations();
});

function setupEventListeners() {
    createBtn.addEventListener('click', handleCreateConversation);
    refreshBtn.addEventListener('click', fetchAllConversations);
    sendBtn.addEventListener('click', handleSendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    // Toast close buttons
    document.querySelectorAll('.toast-close').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.target.closest('.toast').classList.add('hidden');
        });
    });
}

async function handleCreateConversation() {
    const gesprachName = gesprachNameInput.value.trim();
    
    if (!gesprachName) {
        showError('Bitte gib einen Gesprächsnamen ein');
        return;
    }

    const personlichkeit = personlichkeitInput.value.trim() || null;

    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/gesprach_erstellen`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gesprach_name: gesprachName,
                personlichkeit: personlichkeit
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.antwort || 'Fehler beim Erstellen des Gesprächs');
        }

        currentGesprachName = gesprachName;
        updateCurrentConversationDisplay(gesprachName);
        displayConversation(data.gesprach);
        enableChat();
        showSuccess('Gespräch erfolgreich erstellt!');
        
        // Refresh conversations list
        fetchAllConversations();
        
        // Clear inputs
        gesprachNameInput.value = '';
        personlichkeitInput.value = '';
    } catch (error) {
        showError(error.message || 'Fehler beim Erstellen des Gesprächs');
    } finally {
        showLoading(false);
    }
}

async function handleSendMessage() {
    if (!currentGesprachName) {
        showError('Bitte lade oder erstelle zuerst ein Gespräch');
        return;
    }

    const message = messageInput.value.trim();
    
    if (!message) {
        return;
    }

    // Disable input while sending
    messageInput.disabled = true;
    sendBtn.disabled = true;

    // Show user message immediately
    addMessageToChat('human', message);
    messageInput.value = '';

    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE_URL}/nachricht_senden`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gesprach_name: currentGesprachName,
                nachricht: message
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.antwort || 'Fehler beim Senden der Nachricht');
        }

        // Remove typing indicator before displaying conversation
        removeTypingIndicator();

        // Display the updated conversation
        displayConversation(data.gesprach);
        showSuccess('Nachricht gesendet!');
    } catch (error) {
        removeTypingIndicator();
        showError(error.message || 'Fehler beim Senden der Nachricht');
    } finally {
        messageInput.disabled = false;
        sendBtn.disabled = false;
        messageInput.focus();
    }
}

function displayConversation(gesprach) {
    // Remove typing indicator if present
    removeTypingIndicator();
    
    messagesContainer.innerHTML = '';
    
    if (!gesprach || gesprach.length === 0) {
        messagesContainer.innerHTML = '<div class="welcome-message"><p>👋 Willkommen! Erstelle oder lade ein Gespräch, um zu beginnen.</p></div>';
        chatHeader.classList.add('hidden');
        return;
    }

    gesprach.forEach(nachricht => {
        const typ = nachricht.typ;
        const inhalt = nachricht.inhalt;

        // Skip system messages in display (or show them differently)
        if (typ === 'system') {
            // Optionally show system messages as info
            // addMessageToChat('system', inhalt);
            return;
        }

        addMessageToChat(typ, inhalt);
    });

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addMessageToChat(typ, inhalt) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${typ}`;

    const label = document.createElement('div');
    label.className = 'message-label';
    
    if (typ === 'human') {
        label.textContent = 'Du';
    } else if (typ === 'ai') {
        label.textContent = 'KI';
    } else {
        label.textContent = 'System';
    }

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = inhalt;

    messageDiv.appendChild(label);
    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
    // Remove any existing typing indicator
    removeTypingIndicator();

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai typing-indicator';
    messageDiv.id = 'typing-indicator';

    const label = document.createElement('div');
    label.className = 'message-label';
    label.textContent = 'KI';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble typing-bubble';
    bubble.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';

    messageDiv.appendChild(label);
    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);

    typingIndicatorElement = messageDiv;

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
    if (typingIndicatorElement && typingIndicatorElement.parentNode) {
        typingIndicatorElement.parentNode.removeChild(typingIndicatorElement);
        typingIndicatorElement = null;
    }
}

function updateCurrentConversationDisplay(name) {
    // Update chat header
    if (name) {
        chatHeaderTitle.textContent = name;
        chatHeader.classList.remove('hidden');
    } else {
        chatHeader.classList.add('hidden');
    }
}

function enableChat() {
    messageInput.disabled = false;
    sendBtn.disabled = false;
    messageInput.focus();
}

function disableChat() {
    messageInput.disabled = true;
    sendBtn.disabled = true;
}

function showLoading(show) {
    if (show) {
        loadingOverlay.classList.remove('hidden');
    } else {
        loadingOverlay.classList.add('hidden');
    }
}

function showChatLoading(show) {
    if (show) {
        chatLoadingOverlay.classList.remove('hidden');
    } else {
        chatLoadingOverlay.classList.add('hidden');
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorToast.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorToast.classList.add('hidden');
    }, 5000);
}

function showSuccess(message) {
    successMessage.textContent = message;
    successToast.classList.remove('hidden');
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        successToast.classList.add('hidden');
    }, 3000);
}

async function fetchAllConversations() {
    try {
        const response = await fetch(`${API_BASE_URL}/alle_gesprache_erhalten`, {
            method: 'GET',
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.antwort || 'Fehler beim Laden der Gespräche');
        }

        displayConversationsList(data.dateien_namen || []);
    } catch (error) {
        console.error('Error fetching conversations:', error);
        conversationsList.innerHTML = '<div class="no-conversations">Fehler beim Laden der Gespräche</div>';
    }
}

function displayConversationsList(dateienNamen) {
    conversationsList.innerHTML = '';

    if (!dateienNamen || dateienNamen.length === 0) {
        conversationsList.innerHTML = '<div class="no-conversations">Keine Gespräche gefunden</div>';
        return;
    }

    // Filter out non-JSON files and remove .json extension
    const gesprache = dateienNamen
        .filter(name => name.endsWith('.json'))
        .map(name => name.replace('.json', ''));

    if (gesprache.length === 0) {
        conversationsList.innerHTML = '<div class="no-conversations">Keine Gespräche gefunden</div>';
        return;
    }

    gesprache.forEach(gesprachName => {
        const item = document.createElement('div');
        item.className = 'conversation-item';
        if (gesprachName === currentGesprachName) {
            item.classList.add('active');
        }

        item.innerHTML = `
            <span class="conversation-icon">💬</span>
            <span class="conversation-name-text">${gesprachName}</span>
        `;

        item.addEventListener('click', () => {
            loadConversationByName(gesprachName);
        });

        conversationsList.appendChild(item);
    });
}

async function loadConversationByName(gesprachName) {
    showChatLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/gesprach_laden`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gesprach_name: gesprachName
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.antwort || 'Fehler beim Laden des Gesprächs');
        }

        currentGesprachName = gesprachName;
        updateCurrentConversationDisplay(gesprachName);
        displayConversation(data.gesprach);
        enableChat();
        
        // Update active state in list
        fetchAllConversations();
    } catch (error) {
        showError(error.message || 'Fehler beim Laden des Gesprächs');
    } finally {
        showChatLoading(false);
    }
}

