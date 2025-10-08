import { useState, useEffect, useRef } from 'react';
import { chatAPI } from './api';
import { MessageSquarePlus, Trash2, Send, Loader2, Sparkles, Bot, User } from 'lucide-react';
import './App.css';

function App() {
  const [threads, setThreads] = useState([]);
  const [currentThreadId, setCurrentThreadId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingMessage]);

  useEffect(() => {
    loadThreads();
  }, []);

  const loadThreads = async () => {
    try {
      const data = await chatAPI.getThreads();
      setThreads(data.threads);
      
      if (!currentThreadId && data.threads.length === 0) {
        await createNewThread();
      } else if (!currentThreadId && data.threads.length > 0) {
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
    
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);
    setStreamingMessage('');

    try {
      let accumulatedResponse = '';
      
      await chatAPI.sendMessageStream(
        userMessage,
        currentThreadId,
        (chunk) => {
          accumulatedResponse += chunk;
          setStreamingMessage(accumulatedResponse);
        },
        async (threadId) => {
          setMessages(prev => [...prev, { role: 'assistant', content: accumulatedResponse }]);
          setStreamingMessage('');
          setIsLoading(false);
          await loadThreads();
        },
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

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(e);
    }
  };

  return (
    <div className="app-container">
      {/* Animated Background with Stars */}
      <div className="animated-background">
        {/* Animated Blobs */}
        <div className="blob blob-1" />
        <div className="blob blob-2" />
        <div className="blob blob-3" />
        
        {/* Twinkling Stars */}
        {[...Array(100)].map((_, i) => (
          <div
            key={`star-${i}`}
            className="star"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              width: `${1 + Math.random() * 2}px`,
              height: `${1 + Math.random() * 2}px`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${2 + Math.random() * 3}s`
            }}
          />
        ))}
        
        {/* Shooting Stars */}
        {[...Array(5)].map((_, i) => (
          <div
            key={`shooting-${i}`}
            className="shooting-star"
            style={{
              left: `${20 + Math.random() * 60}%`,
              top: `${Math.random() * 50}%`,
              width: `${50 + Math.random() * 100}px`,
              animationDelay: `${i * 8}s`,
              animationDuration: `${2 + Math.random()}s`
            }}
          />
        ))}
        
        {/* Grid Pattern */}
        <div className="grid-pattern" />
      </div>

      {/* Content */}
      <div className="app">
        {/* Sidebar */}
        <div className="sidebar">
          <div className="sidebar-header">
            <div className="header-content">
              <div className="logo-container">
                <Sparkles size={20} />
              </div>
              <h1 className="gradient-text">AI Assistant</h1>
            </div>
            <button className="new-chat-btn" onClick={createNewThread} title="New Chat">
              <MessageSquarePlus size={20} />
              <span>New Conversation</span>
            </button>
          </div>

          <div className="threads-list">
            <h2>Recent Chats</h2>
            {threads.map((thread, index) => (
              <div
                key={thread.thread_id}
                className={`thread-item ${currentThreadId === thread.thread_id ? 'active' : ''}`}
                style={{ animationDelay: `${index * 0.05}s` }}
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
                <div className="empty-state-icon">
                  <Bot size={48} />
                </div>
                <h2 className="gradient-text">Welcome to AI Assistant</h2>
                <p>I'm powered by Gemini and equipped with advanced tools!</p>
                <div className="feature-grid">
                  <div className="feature-card">
                    <div className="feature-icon blue">🔍</div>
                    <p>Search the web</p>
                  </div>
                  <div className="feature-card">
                    <div className="feature-icon green">📊</div>
                    <p>Stock prices</p>
                  </div>
                  <div className="feature-card">
                    <div className="feature-icon yellow">🧮</div>
                    <p>Calculate</p>
                  </div>
                  <div className="feature-card">
                    <div className="feature-icon pink">💡</div>
                    <p>Ask anything</p>
                  </div>
                </div>
              </div>
            ) : (
              <>
                {messages.map((msg, index) => (
                  <div key={index} className={`message ${msg.role}`}>
                    <div className="message-avatar">
                      {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                    </div>
                    <div className="message-content">
                      <p>{msg.content}</p>
                    </div>
                  </div>
                ))}
                {streamingMessage && (
                  <div className="message assistant streaming">
                    <div className="message-avatar">
                      <Bot size={20} />
                    </div>
                    <div className="message-content">
                      <p>{streamingMessage}<span className="typing-cursor"></span></p>
                    </div>
                  </div>
                )}
              </>
            )}
            {isLoading && !streamingMessage && (
              <div className="message assistant">
                <div className="message-avatar">
                  <Bot size={20} />
                </div>
                <div className="message-content">
                  <div className="loading">
                    <Loader2 className="spinner" size={20} />
                    <div className="loading-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
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
              onKeyPress={handleKeyPress}
              placeholder="Type your message here..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading || !inputMessage.trim()}>
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
