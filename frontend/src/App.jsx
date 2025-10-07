import { useState, useEffect, useRef } from 'react';
import { chatAPI } from './api';
import { MessageSquarePlus, Trash2, Send, Loader2 } from 'lucide-react';
import './App.css';

function App() {
  const [threads, setThreads] = useState([]);
  const [currentThreadId, setCurrentThreadId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState('');
  const messagesEndRef = useRef(null);

  // Scroll to bottom when messages change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingMessage]);

  // Load threads on mount
  useEffect(() => {
    loadThreads();
  }, []);

  const loadThreads = async () => {
    try {
      const data = await chatAPI.getThreads();
      setThreads(data.threads);
      
      // If no current thread, create one
      if (!currentThreadId && data.threads.length === 0) {
        await createNewThread();
      } else if (!currentThreadId && data.threads.length > 0) {
        // Load the first thread
        const firstThread = data.threads[0];
        setCurrentThreadId(firstThread.thread_id);
        await loadConversation(firstThread.thread_id);
      }
    } catch (error) {
      console.error('Error loading threads:', error);
    }
  };

  const createNewThread = async () => {
    try {
      const data = await chatAPI.createThread();
      setCurrentThreadId(data.thread_id);
      setMessages([]);
      await loadThreads();
    } catch (error) {
      console.error('Error creating thread:', error);
    }
  };

  const loadConversation = async (threadId) => {
    try {
      const data = await chatAPI.getConversation(threadId);
      setMessages(data.messages);
      setCurrentThreadId(threadId);
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  const deleteThread = async (threadId) => {
    try {
      await chatAPI.deleteThread(threadId);
      
      // If we deleted the current thread, create a new one
      if (threadId === currentThreadId) {
        await createNewThread();
      } else {
        await loadThreads();
      }
    } catch (error) {
      console.error('Error deleting thread:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Add user message to UI
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);
    setStreamingMessage('');

    try {
      let accumulatedResponse = '';
      
      await chatAPI.sendMessageStream(
        userMessage,
        currentThreadId,
        // onChunk callback
        (chunk) => {
          accumulatedResponse += chunk;
          setStreamingMessage(accumulatedResponse);
        },
        // onComplete callback
        async (threadId) => {
          // Add final assistant message to messages array
          setMessages(prev => [...prev, { role: 'assistant', content: accumulatedResponse }]);
          setStreamingMessage('');
          setIsLoading(false);
          
          // Reload threads to update names
          await loadThreads();
        },
        // onError callback
        (error) => {
          console.error('Streaming error:', error);
          setMessages(prev => [
            ...prev,
            { role: 'assistant', content: 'Sorry, there was an error processing your message.' }
          ]);
          setStreamingMessage('');
          setIsLoading(false);
        }
      );
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Sorry, there was an error processing your message.' }
      ]);
      setStreamingMessage('');
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h1>Personal Assistant</h1>
          <button className="new-chat-btn" onClick={createNewThread} title="New Chat">
            <MessageSquarePlus size={20} />
          </button>
        </div>

        <div className="threads-list">
          <h2>Conversations</h2>
          {threads.map((thread) => (
            <div
              key={thread.thread_id}
              className={`thread-item ${currentThreadId === thread.thread_id ? 'active' : ''}`}
            >
              <button
                className="thread-btn"
                onClick={() => loadConversation(thread.thread_id)}
              >
                {thread.name}
              </button>
              <button
                className="delete-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  deleteThread(thread.thread_id);
                }}
                title="Delete"
              >
                <Trash2 size={16} />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 && !streamingMessage ? (
            <div className="empty-state">
              <h2>Welcome to Personal Assistant</h2>
              <p>Ask me anything! I can help you with:</p>
              <ul>
                <li>🔍 Web searches</li>
                <li>📊 Stock prices</li>
                <li>🧮 Calculations</li>
                <li>💬 General questions</li>
              </ul>
            </div>
          ) : (
            <>
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.role}`}>
                  <div className="message-content">
                    <strong>{msg.role === 'user' ? 'You' : 'Assistant'}:</strong>
                    <p>{msg.content}</p>
                  </div>
                </div>
              ))}
              {streamingMessage && (
                <div className="message assistant">
                  <div className="message-content">
                    <strong>Assistant:</strong>
                    <p>{streamingMessage}<span className="cursor">▊</span></p>
                  </div>
                </div>
              )}
            </>
          )}
          {isLoading && !streamingMessage && (
            <div className="message assistant">
              <div className="message-content">
                <strong>Assistant:</strong>
                <div className="loading">
                  <Loader2 className="spinner" size={20} />
                  <span>Thinking...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="input-form" onSubmit={sendMessage}>
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading || !inputMessage.trim()}>
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
