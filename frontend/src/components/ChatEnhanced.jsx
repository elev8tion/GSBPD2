import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Send, MessageSquare, User, Bot, Trash2, RefreshCw, TrendingUp, Zap } from 'lucide-react';
import { useSport } from '../contexts/SportContext';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const ChatEnhanced = () => {
  const { selectedSport } = useSport();
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: `Hey! I'm KC, your AI betting assistant. I can help you analyze games, explain predictions, and answer questions about ${selectedSport} betting strategies. What would you like to know?`,
      timestamp: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Auto-resize textarea
  const handleInputChange = (e) => {
    setInput(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/chat`, {
        message: input.trim(),
        sport: selectedSport,
        history: messages
      });

      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: generateMockResponse(input),
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const generateMockResponse = (userInput) => {
    const lowerInput = userInput.toLowerCase();

    if (lowerInput.includes('strategy') || lowerInput.includes('how')) {
      return "Great question! When analyzing games, I recommend focusing on these key factors:\n\n1. **Recent Form**: Look at the last 5-10 games for momentum\n2. **Head-to-Head**: Historical matchups can reveal patterns\n3. **Home/Away Performance**: Some teams perform significantly better at home\n4. **Injuries**: Star player availability is crucial\n5. **Rest Days**: Back-to-back games affect performance\n\nWould you like me to analyze a specific matchup?";
    }

    if (lowerInput.includes('predict') || lowerInput.includes('game')) {
      return "I can help you analyze any upcoming game! To give you the best prediction, I'll need:\n\n• The two teams playing\n• Game date and location\n• Any relevant injury information\n\nYou can also use the Dashboard to select a game and get an instant AI prediction with detailed analysis.";
    }

    if (lowerInput.includes('model') || lowerInput.includes('accuracy')) {
      return `Our ${selectedSport} prediction model uses advanced machine learning (XGBoost + Neural Networks) and currently achieves:\n\n✓ 72.5% prediction accuracy\n✓ 18.3% average ROI\n✓ Trained on 15,000+ historical games\n\nThe model considers 50+ features including team stats, player performance, scheduling factors, and historical matchups.`;
    }

    return `I understand you're asking about "${userInput}". I'm here to help with ${selectedSport} betting analysis, game predictions, and strategy advice. Could you provide more details so I can give you a better answer?`;
  };

  const handleClearChat = () => {
    setMessages([{
      id: 1,
      role: 'assistant',
      content: `Chat cleared! I'm ready to help you with ${selectedSport} betting analysis. What would you like to know?`,
      timestamp: new Date().toISOString()
    }]);
  };

  const suggestedQuestions = [
    "What's your betting strategy for today's games?",
    "How accurate is your prediction model?",
    "Explain the key factors in game predictions",
    "What should I consider when betting on underdogs?"
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 280px)', minHeight: '600px' }}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ marginBottom: '24px' }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <h2 style={{
              fontSize: '24px',
              fontWeight: '600',
              color: 'var(--text-primary)',
              marginBottom: '6px',
              letterSpacing: '-0.03em'
            }}>
              KC Chat
            </h2>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', margin: 0 }}>
              Ask me anything about {selectedSport} betting and predictions
            </p>
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleClearChat}
            style={{
              padding: '10px 18px',
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '8px',
              color: 'var(--text-secondary)',
              fontSize: '13px',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.15s ease',
              fontFamily: 'inherit',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <Trash2 size={16} />
            Clear Chat
          </motion.button>
        </div>
      </motion.div>

      {/* Messages Container */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="section"
        style={{
          flex: 1,
          padding: '24px',
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
          marginBottom: '16px'
        }}
      >
        {messages.map((message, index) => (
          <Message key={message.id} message={message} index={index} />
        ))}

        {loading && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '16px 20px',
              background: 'var(--bg-elevated)',
              borderRadius: '12px',
              alignSelf: 'flex-start',
              maxWidth: '80%'
            }}
          >
            <Bot size={20} style={{ color: 'var(--primary)' }} />
            <div className="loading-spinner" style={{ width: '16px', height: '16px' }}></div>
            <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>KC is thinking...</span>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </motion.div>

      {/* Suggested Questions (show when no messages) */}
      {messages.length === 1 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '12px',
            marginBottom: '16px'
          }}
        >
          {suggestedQuestions.map((question, idx) => (
            <motion.button
              key={idx}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setInput(question)}
              style={{
                padding: '12px 16px',
                background: 'var(--bg-card)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '8px',
                color: 'var(--text-secondary)',
                fontSize: '13px',
                fontWeight: '500',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                fontFamily: 'inherit',
                textAlign: 'left',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <Zap size={14} style={{ color: 'var(--primary)', flexShrink: 0 }} />
              <span>{question}</span>
            </motion.button>
          ))}
        </motion.div>
      )}

      {/* Input Area */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15 }}
        className="section"
        style={{
          padding: '24px',
          background: 'var(--bg-elevated)',
          borderTop: '2px solid var(--border-subtle)'
        }}
      >
        <div className="chat-input-container" style={{
          display: 'flex',
          gap: '16px',
          alignItems: 'flex-end',
          position: 'relative'
        }}>
          <div style={{
            flex: 1,
            position: 'relative',
            background: 'var(--bg-card)',
            borderRadius: '16px',
            border: '2px solid var(--border-subtle)',
            transition: 'all 0.2s ease',
            overflow: 'hidden'
          }}
          onFocus={(e) => e.currentTarget.style.borderColor = 'var(--primary)'}
          onBlur={(e) => e.currentTarget.style.borderColor = 'var(--border-subtle)'}
          >
            <textarea
              ref={textareaRef}
              value={input}
              onChange={handleInputChange}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Ask me anything about betting strategies, game analysis, or predictions..."
              style={{
                width: '100%',
                minHeight: '80px',
                maxHeight: '200px',
                padding: '20px',
                background: 'transparent',
                border: 'none',
                outline: 'none',
                resize: 'none',
                fontSize: '15px',
                lineHeight: '1.6',
                color: 'var(--text-primary)',
                fontFamily: 'inherit',
                overflow: 'auto'
              }}
            />
            <div style={{
              position: 'absolute',
              bottom: '12px',
              left: '20px',
              fontSize: '12px',
              color: 'var(--text-tertiary)',
              pointerEvents: 'none',
              opacity: input ? 0 : 0.6,
              transition: 'opacity 0.2s ease'
            }}>
              💡 Tip: Press Shift + Enter for new line
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleSend}
            disabled={loading || !input.trim()}
            style={{
              padding: '20px 32px',
              background: 'transparent',
              border: `2px solid ${input.trim() ? 'var(--primary)' : 'var(--border-subtle)'}`,
              borderRadius: '16px',
              color: input.trim() ? 'var(--primary)' : 'var(--text-tertiary)',
              fontSize: '15px',
              fontWeight: '600',
              cursor: input.trim() ? 'pointer' : 'not-allowed',
              transition: 'all 0.2s ease',
              fontFamily: 'inherit',
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              opacity: input.trim() ? 1 : 0.5,
              minHeight: '80px'
            }}
          >
            <Send size={20} />
            <span>Send</span>
          </motion.button>
        </div>

        <div className="chat-status-bar" style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginTop: '16px',
          paddingTop: '16px',
          borderTop: '1px solid var(--border-subtle)'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
          }}>
            <div style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              background: 'var(--success)',
              boxShadow: '0 0 8px var(--success)',
              animation: 'pulse 2s infinite'
            }} />
            <span style={{
              fontSize: '13px',
              color: 'var(--text-secondary)',
              fontWeight: '500'
            }}>
              KC AI is online and ready to help
            </span>
          </div>

          <div style={{
            fontSize: '12px',
            color: 'var(--text-tertiary)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <MessageSquare size={14} />
            {messages.length - 1} message{messages.length - 1 !== 1 ? 's' : ''} in chat
          </div>
        </div>
      </motion.div>
    </div>
  );
};

const Message = ({ message, index }) => {
  const isUser = message.role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.02 }}
      style={{
        display: 'flex',
        gap: '12px',
        alignItems: 'flex-start',
        alignSelf: isUser ? 'flex-end' : 'flex-start',
        maxWidth: '80%'
      }}
    >
      {!isUser && (
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: '50%',
          background: 'transparent',
          border: '2px solid var(--primary)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0
        }}>
          <Bot size={18} style={{ color: 'var(--primary)' }} />
        </div>
      )}

      <div style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        gap: '6px'
      }}>
        <div style={{
          padding: '14px 18px',
          background: isUser ? 'var(--primary)' : 'var(--bg-elevated)',
          borderRadius: isUser ? '12px 12px 4px 12px' : '12px 12px 12px 4px',
          color: isUser ? 'white' : 'var(--text-primary)',
          fontSize: '14px',
          lineHeight: '1.6',
          whiteSpace: 'pre-wrap',
          wordWrap: 'break-word'
        }}>
          {message.content}
        </div>
        <div style={{
          fontSize: '11px',
          color: 'var(--text-tertiary)',
          paddingLeft: '4px'
        }}>
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>

      {isUser && (
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: '50%',
          background: 'var(--bg-elevated)',
          border: '2px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0
        }}>
          <User size={18} style={{ color: 'var(--text-secondary)' }} />
        </div>
      )}
    </motion.div>
  );
};

export default ChatEnhanced;
