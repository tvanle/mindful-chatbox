// Chat functionality
class ChatService {
    constructor() {
        this.currentConversationId = null;
    }

    async sendMessage(message) {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to send message');
            }

            const data = await response.json();
            this.currentConversationId = data.data.conversation_id;
            return data.data;
        } catch (error) {
            console.error('Chat error:', error);
            throw error;
        }
    }

    async getHistory(limit = 20) {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/chat/history?limit=${limit}`, {
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Failed to fetch history');
            }

            const data = await response.json();
            return data.data;
        } catch (error) {
            console.error('History error:', error);
            return [];
        }
    }

    async sendFeedback(conversationId, helpful, comment = '') {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/feedback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    conversation_id: conversationId,
                    helpful: helpful,
                    comment: comment
                })
            });

            if (!response.ok) {
                throw new Error('Failed to send feedback');
            }

            return await response.json();
        } catch (error) {
            console.error('Feedback error:', error);
            throw error;
        }
    }
}

// Initialize chat service
const chatService = new ChatService();