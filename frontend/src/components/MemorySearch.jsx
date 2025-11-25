import { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Search, Database, BookOpen, Trophy } from 'lucide-react';

const API_URL = 'http://localhost:8000';

export default function MemorySearch() {
  const [query, setQuery] = useState('');
  const [sport, setSport] = useState('all');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [memories, setMemories] = useState([]);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/memories/search`, {
        query: query,
        memories: sport === 'all' ? [] : [`${sport}-*`],
        top_k: 5
      });
      setResults(response.data);
    } catch (error) {
      console.error('Search failed:', error);
      setResults({ status: 'error', message: error.message });
    } finally {
      setLoading(false);
    }
  };

  const loadMemories = async () => {
    try {
      const response = await axios.get(`${API_URL}/memories/list`);
      if (response.data.status === 'success') {
        setMemories(response.data.memories);
      }
    } catch (error) {
      console.error('Failed to load memories:', error);
    }
  };

  return (
    <div className="memory-search-container">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="search-header"
      >
        <Database className="icon" size={32} />
        <h2>Knowledge Base Search</h2>
        <p>Search across NFL and NBA game memories, strategies, and player stats</p>
      </motion.div>

      <div className="search-controls">
        <div className="sport-selector">
          <button
            className={sport === 'all' ? 'active' : ''}
            onClick={() => setSport('all')}
          >
            All Sports
          </button>
          <button
            className={sport === 'nfl' ? 'active' : ''}
            onClick={() => setSport('nfl')}
          >
            🏈 NFL
          </button>
          <button
            className={sport === 'nba' ? 'active' : ''}
            onClick={() => setSport('nba')}
          >
            🏀 NBA
          </button>
        </div>

        <div className="search-input-group">
          <Search className="search-icon" size={20} />
          <input
            type="text"
            placeholder="Ask anything about games, players, strategies..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            className="search-input"
          />
          <button
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            className="search-button"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        <button onClick={loadMemories} className="list-memories-btn">
          <BookOpen size={16} /> View All Memories
        </button>
      </div>

      {memories.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="memories-list"
        >
          <h3>Available Memories ({memories.length})</h3>
          <div className="memory-cards">
            {memories.map((mem, idx) => (
              <div key={idx} className="memory-card">
                <Trophy size={16} />
                <div>
                  <strong>{mem.project_name}</strong>
                  <span>{mem.file_count} files • {mem.size_mb} MB</span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {results && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="search-results"
        >
          {results.status === 'success' ? (
            <>
              <h3>Search Results for "{query}"</h3>
              {results.results && results.results.length > 0 ? (
                <div className="results-grid">
                  {results.results.map((result, idx) => (
                    <div key={idx} className="result-card">
                      <div className="result-header">
                        <span className="result-number">#{idx + 1}</span>
                        {result.memory && (
                          <span className="memory-badge">{result.memory}</span>
                        )}
                      </div>
                      <p className="result-text">
                        {typeof result === 'string' ? result : result.text}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="no-results">No results found. Try a different query.</p>
              )}
            </>
          ) : (
            <div className="error-message">
              <p>Error: {results.message}</p>
            </div>
          )}
        </motion.div>
      )}

      <style jsx>{`
        .memory-search-container {
          padding: 2rem;
          max-width: 1200px;
          margin: 0 auto;
        }

        .search-header {
          text-align: center;
          margin-bottom: 2rem;
        }

        .search-header .icon {
          color: #00d4ff;
          margin-bottom: 1rem;
        }

        .search-header h2 {
          font-size: 2rem;
          margin-bottom: 0.5rem;
          background: linear-gradient(135deg, #00d4ff, #ff00ea);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .search-controls {
          background: rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(0, 212, 255, 0.3);
          border-radius: 12px;
          padding: 1.5rem;
          margin-bottom: 2rem;
        }

        .sport-selector {
          display: flex;
          gap: 0.5rem;
          margin-bottom: 1rem;
        }

        .sport-selector button {
          flex: 1;
          padding: 0.75rem;
          border: 1px solid rgba(0, 212, 255, 0.3);
          background: rgba(0, 0, 0, 0.3);
          color: #fff;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.3s;
        }

        .sport-selector button.active {
          background: linear-gradient(135deg, #00d4ff, #0099cc);
          border-color: #00d4ff;
        }

        .search-input-group {
          position: relative;
          display: flex;
          gap: 0.5rem;
          margin-bottom: 1rem;
        }

        .search-icon {
          position: absolute;
          left: 1rem;
          top: 50%;
          transform: translateY(-50%);
          color: #00d4ff;
        }

        .search-input {
          flex: 1;
          padding: 1rem 1rem 1rem 3rem;
          background: rgba(0, 0, 0, 0.5);
          border: 1px solid rgba(0, 212, 255, 0.3);
          border-radius: 8px;
          color: #fff;
          font-size: 1rem;
        }

        .search-button {
          padding: 1rem 2rem;
          background: linear-gradient(135deg, #00d4ff, #0099cc);
          border: none;
          border-radius: 8px;
          color: #fff;
          font-weight: bold;
          cursor: pointer;
          transition: all 0.3s;
        }

        .search-button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 212, 255, 0.4);
        }

        .search-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .list-memories-btn {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1.5rem;
          background: rgba(255, 0, 234, 0.1);
          border: 1px solid rgba(255, 0, 234, 0.3);
          border-radius: 8px;
          color: #ff00ea;
          cursor: pointer;
          transition: all 0.3s;
        }

        .list-memories-btn:hover {
          background: rgba(255, 0, 234, 0.2);
        }

        .memories-list {
          margin-bottom: 2rem;
        }

        .memories-list h3 {
          color: #00d4ff;
          margin-bottom: 1rem;
        }

        .memory-cards {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
          gap: 1rem;
        }

        .memory-card {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 1rem;
          background: rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(0, 212, 255, 0.3);
          border-radius: 8px;
        }

        .memory-card div {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .memory-card strong {
          color: #00d4ff;
        }

        .memory-card span {
          color: #999;
          font-size: 0.875rem;
        }

        .search-results {
          background: rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(0, 212, 255, 0.3);
          border-radius: 12px;
          padding: 2rem;
        }

        .search-results h3 {
          color: #00d4ff;
          margin-bottom: 1.5rem;
        }

        .results-grid {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .result-card {
          background: rgba(0, 0, 0, 0.5);
          border: 1px solid rgba(0, 212, 255, 0.2);
          border-radius: 8px;
          padding: 1.5rem;
          transition: all 0.3s;
        }

        .result-card:hover {
          border-color: #00d4ff;
          transform: translateX(4px);
        }

        .result-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }

        .result-number {
          color: #00d4ff;
          font-weight: bold;
        }

        .memory-badge {
          padding: 0.25rem 0.75rem;
          background: rgba(255, 0, 234, 0.2);
          border: 1px solid rgba(255, 0, 234, 0.3);
          border-radius: 4px;
          color: #ff00ea;
          font-size: 0.75rem;
        }

        .result-text {
          line-height: 1.6;
          color: #e0e0e0;
        }

        .no-results {
          text-align: center;
          color: #999;
          padding: 2rem;
        }

        .error-message {
          padding: 1rem;
          background: rgba(255, 0, 0, 0.1);
          border: 1px solid rgba(255, 0, 0, 0.3);
          border-radius: 8px;
          color: #ff6b6b;
        }
      `}</style>
    </div>
  );
}
