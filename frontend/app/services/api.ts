import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const chatService = {
    sendMessage: async (message: string, history: any[]) => {
        try {
            const response = await api.post('/chat/send', {
                message,
                user_id: "demo-user", // Todo: Replace with real auth
                history,
            });
            return response.data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
};

export default api;
