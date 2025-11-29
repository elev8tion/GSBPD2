import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Sparkles, Trash2, MessageSquare } from 'lucide-react';

const API_URL = 'http://localhost:8000';

export default function Chat() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hey! I\'m KC the Creator, your AI sports betting analyst. Ask me anything about NFL/NBA predictions, player stats, betting strategies, or SGP insights!',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // TODO: Replace with actual API endpoint
      const response = await axios.post(`${API_URL}/chat`, {
        message: input.trim(),
        history: messages.slice(-10) // Send last 10 messages for context
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.message || 'I understand. Let me analyze that for you...',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat failed:', error);

      // Mock response for demo
      const mockResponse = {
        role: 'assistant',
        content: `Based on recent analysis, here's my insight on "${input.trim()}": This feature is currently in development. I'll be able to provide deep sports betting insights, player comparisons, and SGP recommendations soon!`,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, mockResponse]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: 'Chat cleared! What would you like to know?',
        timestamp: new Date()
      }
    ]);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', height: '100%' }}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card-elevated"
        style={{ padding: '32px', textAlign: 'center' }}
      >
        <Sparkles size={48} style={{ color: 'var(--accent)', marginBottom: '16px' }} />
        <h2 style={{
          fontSize: '32px',
          fontWeight: '700',
          marginBottom: '8px',
          color: 'var(--text-primary)'
        }}>
          KC the Creator
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
          AI-powered sports betting insights and analysis
        </p>
      </motion.div>

      {/* Chat Container */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="section"
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          minHeight: '500px',
          maxHeight: 'calc(100vh - 400px)'
        }}
      >
        <div className="section-header">
          <MessageSquare className="section-icon" size={24} style={{ color: 'var(--primary)' }} />
          <h2 className="section-title">Conversation</h2>
          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            onClick={clearChat}
            style={{
              marginLeft: 'auto',
              padding: '8px 16px',
              background: 'rgba(255, 62, 157, 0.1)',
              color: 'var(--danger)',
              border: '2px solid var(--danger)',
              borderRadius: 'var(--radius-md)',
              fontWeight: '600',
              fontSize: '13px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <Trash2 size={14} />
            Clear
          </motion.button>
        </div>

        {/* Messages */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px'
        }}>
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                style={{
                  display: 'flex',
                  gap: '12px',
                  alignItems: 'flex-start',
                  alignSelf: message.role === 'user' ? 'flex-end' : 'flex-start',
                  maxWidth: '85%'
                }}
              >
                {message.role === 'assistant' && (
                  <div style={{
                    padding: '10px',
                    background: 'var(--bg-elevated)',
                    borderRadius: '50%',
                    border: '2px solid var(--accent)',
                    boxShadow: 'var(--glow-accent)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0
                  }}>
                    <Bot size={20} style={{ color: 'var(--accent)' }} />
                  </div>
                )}

                <div style={{
                  padding: '16px 20px',
                  background: message.role === 'user'
                    ? 'rgba(0, 217, 255, 0.1)'
                    : 'var(--bg-elevated)',
                  border: message.role === 'user'
                    ? '2px solid var(--primary)'
                    : '2px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  color: 'var(--text-primary)',
                  fontSize: '14px',
                  lineHeight: '1.6',
                  flex: 1
                }}>
                  <p style={{ margin: 0 }}>{message.content}</p>
                  <div style={{
                    fontSize: '11px',
                    color: 'var(--text-tertiary)',
                    marginTop: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}>
                    {message.role === 'user' ? <User size={10} /> : <Bot size={10} />}
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>

                {message.role === 'user' && (
                  <div style={{
                    padding: '10px',
                    background: 'var(--bg-elevated)',
                    borderRadius: '50%',
                    border: '2px solid var(--primary)',
                    boxShadow: 'var(--glow-primary)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0
                  }}>
                    <User size={20} style={{ color: 'var(--primary)' }} />
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              style={{
                display: 'flex',
                gap: '12px',
                alignItems: 'flex-start',
                alignSelf: 'flex-start',
                maxWidth: '85%'
              }}
            >
              <div style={{
                padding: '10px',
                background: 'var(--bg-elevated)',
                borderRadius: '50%',
                border: '2px solid var(--accent)',
                boxShadow: 'var(--glow-accent)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <Bot size={20} style={{ color: 'var(--accent)' }} />
              </div>
              <div style={{
                padding: '16px 20px',
                background: 'var(--bg-elevated)',
                border: '2px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                color: 'var(--text-secondary)',
                fontSize: '14px'
              }}>
                <div style={{ display: 'flex', gap: '4px' }}>
                  <span className="animate-pulse">●</span>
                  <span className="animate-pulse" style={{ animationDelay: '0.2s' }}>●</span>
                  <span className="animate-pulse" style={{ animationDelay: '0.4s' }}>●</span>
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form onSubmit={handleSubmit} style={{
          padding: '20px 24px',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          gap: '12px'
        }}>
          <input
            type="text"
            className="input-field"
            placeholder="Ask about players, teams, betting strategies..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            style={{ flex: 1 }}
          />
          <motion.button
            type="submit"
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            disabled={loading || !input.trim()}
            style={{
              padding: '14px 24px',
              background: (loading || !input.trim()) ? 'var(--bg-hover)' : 'rgba(255, 184, 0, 0.1)',
              color: (loading || !input.trim()) ? 'var(--text-tertiary)' : 'var(--accent)',
              border: (loading || !input.trim()) ? '2px solid var(--border-subtle)' : '2px solid var(--accent)',
              borderRadius: 'var(--radius-md)',
              fontWeight: '700',
              fontSize: '14px',
              cursor: (loading || !input.trim()) ? 'not-allowed' : 'pointer',
              opacity: (loading || !input.trim()) ? 0.5 : 1,
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              whiteSpace: 'nowrap'
            }}
          >
            <Send size={16} />
            Send
          </motion.button>
        </form>
      </motion.div>
    </div>
  );
}
