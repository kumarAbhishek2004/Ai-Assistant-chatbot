import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  // Get all threads
  getThreads: async () => {
    const response = await api.get('/threads');
    return response.data;
  },

  // Create new thread
  createThread: async () => {
    const response = await api.post('/thread/new');
    return response.data;
  },

  // Send message with streaming
  sendMessageStream: async (message, threadId, onChunk, onComplete, onError) => {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          thread_id: threadId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.substring(6));
            
            if (data.type === 'content') {
              onChunk(data.content);
            } else if (data.type === 'done') {
              onComplete(data.thread_id);
            } else if (data.type === 'error') {
              onError(data.error);
            }
          }
        }
      }
    } catch (error) {
      onError(error.message);
    }
  },

  // Send message (non-streaming fallback)
  sendMessage: async (message, threadId) => {
    const response = await api.post('/chat', {
      message,
      thread_id: threadId,
    });
    return response.data;
  },

  // Get conversation
  getConversation: async (threadId) => {
    const response = await api.get(`/conversation/${threadId}`);
    return response.data;
  },

  // Delete thread
  deleteThread: async (threadId) => {
    const response = await api.delete(`/thread/${threadId}`);
    return response.data;
  },
};

export default api;
