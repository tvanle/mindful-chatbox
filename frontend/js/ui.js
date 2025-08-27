// UI Management
class UIManager {
    constructor() {
        this.messagesArea = document.getElementById('messagesArea');
        this.messageInput = document.getElementById('messageInput');
        this.chatForm = document.getElementById('chatForm');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.charCount = document.getElementById('charCount');
        this.feedbackModal = document.getElementById('feedbackModal');
        this.currentFeedbackConversationId = null;
        
        this.init();
    }

    init() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSendMessage();
        });

        // Character count
        this.messageInput.addEventListener('input', () => {
            this.updateCharCount();
            this.autoResizeTextarea();
        });

        // Quick actions
        document.querySelectorAll('.quick-action').forEach(button => {
            button.addEventListener('click', () => {
                const message = button.dataset.message;
                this.messageInput.value = message;
                this.handleSendMessage();
            });
        });

        // Theme toggle
        document.getElementById('themeToggle').addEventListener('click', () => {
            this.toggleTheme();
        });

        // Feedback modal
        document.querySelectorAll('.feedback-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const helpful = btn.dataset.helpful === 'true';
                this.handleFeedback(helpful);
            });
        });

        // Load theme
        this.loadTheme();
        
        // Load history
        this.loadHistory();
    }

    async handleSendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) return;
        
        // Disable input
        this.setInputState(false);
        
        // Add user message
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        this.updateCharCount();
        this.autoResizeTextarea();
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send message
            const response = await chatService.sendMessage(message);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add bot response
            this.addMessage(response.response, 'bot', {
                conversationId: response.conversation_id,
                intent: response.intent,
                isCrisis: response.is_crisis
            });
            
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Xin lỗi, đã xảy ra lỗi. Vui lòng thử lại sau.', 'bot', {
                isError: true
            });
        } finally {
            // Re-enable input
            this.setInputState(true);
            this.messageInput.focus();
        }
    }

    addMessage(text, sender = 'bot', options = {}) {
        // Remove welcome message if exists
        const welcomeMsg = this.messagesArea.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        if (options.isCrisis) {
            messageDiv.classList.add('crisis');
        }
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Format text (preserve line breaks)
        const formattedText = text.replace(/\n/g, '<br>');
        contentDiv.innerHTML = formattedText;
        
        // Add timestamp
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit'
        });
        contentDiv.appendChild(timeDiv);
        
        // Add actions for bot messages
        if (sender === 'bot' && !options.isError && options.conversationId) {
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'message-actions';
            
            const feedbackBtn = document.createElement('button');
            feedbackBtn.className = 'action-btn';
            feedbackBtn.textContent = '💬 Đánh giá';
            feedbackBtn.onclick = () => {
                this.openFeedbackModal(options.conversationId);
            };
            
            actionsDiv.appendChild(feedbackBtn);
            contentDiv.appendChild(actionsDiv);
        }
        
        messageDiv.appendChild(contentDiv);
        this.messagesArea.appendChild(messageDiv);
        
        // Auto scroll
        if (CONFIG.AUTO_SCROLL) {
            this.scrollToBottom();
        }
    }

    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }

    setInputState(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
    }

    updateCharCount() {
        const length = this.messageInput.value.length;
        this.charCount.textContent = `${length}/${CONFIG.MAX_MESSAGE_LENGTH}`;
        
        if (length > CONFIG.MAX_MESSAGE_LENGTH * 0.9) {
            this.charCount.style.color = 'var(--danger-color)';
        } else {
            this.charCount.style.color = 'var(--text-secondary)';
        }
    }

    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }

    scrollToBottom() {
        this.messagesArea.scrollTop = this.messagesArea.scrollHeight;
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem(CONFIG.THEME_KEY, newTheme);
    }

    loadTheme() {
        const savedTheme = localStorage.getItem(CONFIG.THEME_KEY) || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
    }

    async loadHistory() {
        try {
            const history = await chatService.getHistory();
            
            if (history.length > 0) {
                // Remove welcome message
                const welcomeMsg = this.messagesArea.querySelector('.welcome-message');
                if (welcomeMsg) {
                    welcomeMsg.remove();
                }
                
                // Add history messages
                history.reverse().forEach(conv => {
                    this.addMessage(conv.message, 'user');
                    this.addMessage(conv.response, 'bot', {
                        conversationId: conv.id,
                        intent: conv.intent,
                        isCrisis: conv.is_crisis
                    });
                });
            }
        } catch (error) {
            console.error('Failed to load history:', error);
        }
    }

    openFeedbackModal(conversationId) {
        this.currentFeedbackConversationId = conversationId;
        this.feedbackModal.style.display = 'flex';
    }

    closeFeedbackModal() {
        this.feedbackModal.style.display = 'none';
        this.currentFeedbackConversationId = null;
        document.getElementById('feedbackComment').value = '';
    }

    async handleFeedback(helpful) {
        if (!this.currentFeedbackConversationId) return;
        
        const comment = document.getElementById('feedbackComment').value;
        
        try {
            await chatService.sendFeedback(
                this.currentFeedbackConversationId,
                helpful,
                comment
            );
            
            this.closeFeedbackModal();
            
            // Show thank you message
            this.showNotification('Cảm ơn bạn đã đánh giá!');
        } catch (error) {
            this.showNotification('Không thể gửi đánh giá. Vui lòng thử lại.', 'error');
        }
    }

    showNotification(message, type = 'success') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: ${type === 'success' ? 'var(--secondary-color)' : 'var(--danger-color)'};
            color: white;
            border-radius: var(--radius);
            z-index: 2000;
            animation: slideIn 0.3s;
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Global functions for modal
function closeFeedbackModal() {
    uiManager.closeFeedbackModal();
}

function submitFeedback() {
    const helpful = null; // Will be set by button click
    uiManager.handleFeedback(helpful);
}

// Initialize UI when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.uiManager = new UIManager();
});

// Add slide in animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);