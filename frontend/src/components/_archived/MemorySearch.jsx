import { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Database, BookOpen, Trophy, Plus, Trash2, X, AlertCircle, CheckCircle2, Folder, Calendar } from 'lucide-react';

const API_URL = 'http://localhost:8000';

// Mock data for demonstration
const MOCK_MEMORIES = [
  {
    project_name: 'nfl-game-analysis',
    file_count: 127,
    size_mb: 45.2,
    created_at: '2025-01-15T10:30:00Z'
  },
  {
    project_name: 'nba-player-stats',
    file_count: 89,
    size_mb: 32.8,
    created_at: '2025-01-18T14:20:00Z'
  },
  {
    project_name: 'nfl-betting-strategies',
    file_count: 56,
    size_mb: 18.5,
    created_at: '2025-01-20T09:15:00Z'
  },
  {
    project_name: 'nba-team-matchups',
    file_count: 23,
    size_mb: 8.3,
    created_at: '2025-01-22T16:45:00Z'
  }
];

const MOCK_SEARCH_RESULTS = {
  status: 'success',
  results: [
    {
      text: 'Chiefs offense has been dominant in the playoffs, averaging 31.5 points per game over the last 3 seasons. Patrick Mahomes has thrown for 12 TDs with only 2 INTs in playoff games at home.',
      memory: 'nfl-game-analysis'
    },
    {
      text: 'When facing the Bills, the Chiefs have won 4 of the last 5 matchups. The key factor has been Chiefs\' ability to control time of possession, averaging 32:15 compared to Bills\' 27:45.',
      memory: 'nfl-game-analysis'
    },
    {
      text: 'Historical data shows that playoff games between top-5 offenses tend to go OVER the total 67% of the time. Both Chiefs and Bills rank in top 3 for offensive efficiency this season.',
      memory: 'nfl-betting-strategies'
    },
    {
      text: 'Mahomes has covered the passing yards prop (Over 275.5) in 8 of his last 10 playoff games. His average playoff performance: 287 yards, 2.4 TDs, 68% completion rate.',
      memory: 'nfl-betting-strategies'
    },
    {
      text: 'Bills defense struggles against mobile QBs who can extend plays. Mahomes averages 4.2 yards per rush attempt in playoff games, often scrambling for crucial first downs on 3rd down.',
      memory: 'nfl-game-analysis'
    }
  ]
};

export default function MemorySearch() {
  const [query, setQuery] = useState('');
  const [sport, setSport] = useState('all');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [memories, setMemories] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [memoryToDelete, setMemoryToDelete] = useState(null);
  const [createForm, setCreateForm] = useState({
    memory_name: '',
    sport: 'nfl',
    category: 'games',
    docs_dir: ''
  });
  const [creating, setCreating] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [createError, setCreateError] = useState('');
  const [createSuccess, setCreateSuccess] = useState(false);
  const [useMockData, setUseMockData] = useState(false);

  useEffect(() => {
    loadMemories();
  }, []);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setUseMockData(false);
    try {
      const response = await axios.post(`${API_URL}/memories/search`, {
        query: query,
        memories: sport === 'all' ? [] : [`${sport}-*`],
        top_k: 5
      });
      if (response.data && response.data.results && response.data.results.length > 0) {
        setResults(response.data);
      } else {
        // Use mock data if API returns no results
        setResults(MOCK_SEARCH_RESULTS);
        setUseMockData(true);
      }
    } catch (error) {
      console.error('Search failed:', error);
      // Use mock data on error
      setResults(MOCK_SEARCH_RESULTS);
      setUseMockData(true);
    } finally {
      setLoading(false);
    }
  };

  const loadMemories = async () => {
    try {
      const response = await axios.get(`${API_URL}/memories/list`);
      if (response.data.status === 'success' && response.data.memories && response.data.memories.length > 0) {
        setMemories(response.data.memories);
        setUseMockData(false);
      } else {
        // Use mock data if API returns no memories
        setMemories(MOCK_MEMORIES);
        setUseMockData(true);
      }
    } catch (error) {
      console.error('Failed to load memories:', error);
      // Use mock data on error
      setMemories(MOCK_MEMORIES);
      setUseMockData(true);
    }
  };

  const loadDemoData = () => {
    setMemories(MOCK_MEMORIES);
    setResults(MOCK_SEARCH_RESULTS);
    setUseMockData(true);
    setQuery('Chiefs vs Bills playoff analysis');
  };

  const handleCreateMemory = async (e) => {
    e.preventDefault();
    setCreateError('');

    if (!createForm.memory_name || !createForm.docs_dir) {
      setCreateError('Please fill in all required fields');
      return;
    }

    setCreating(true);
    try {
      await axios.post(`${API_URL}/memories/create`, {
        memory_name: createForm.memory_name,
        docs_dir: createForm.docs_dir,
        sport: createForm.sport
      });

      setCreateSuccess(true);
      setTimeout(() => setCreateSuccess(false), 3000);
      setShowCreateModal(false);
      setCreateForm({
        memory_name: '',
        sport: 'nfl',
        category: 'games',
        docs_dir: ''
      });
      await loadMemories();
    } catch (error) {
      console.error('Failed to create memory:', error);
      setCreateError(error.response?.data?.message || 'Failed to create memory');
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteMemory = async () => {
    if (!memoryToDelete) return;

    setDeleting(true);
    try {
      await axios.delete(`${API_URL}/memories/${memoryToDelete.project_name}`);
      setShowDeleteModal(false);
      setMemoryToDelete(null);
      await loadMemories();
    } catch (error) {
      console.error('Failed to delete memory:', error);
      alert('Failed to delete memory. Check console for details.');
    } finally {
      setDeleting(false);
    }
  };

  const getMemoryHealth = (memory) => {
    if (!memory.file_count) return 'poor';
    if (memory.file_count >= 100) return 'excellent';
    if (memory.file_count >= 50) return 'good';
    if (memory.file_count >= 10) return 'fair';
    return 'poor';
  };

  const getHealthColor = (health) => {
    switch (health) {
      case 'excellent': return 'var(--success)';
      case 'good': return 'var(--primary)';
      case 'fair': return 'var(--warning)';
      default: return 'var(--danger)';
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card-elevated"
        style={{ padding: '40px', textAlign: 'center' }}
      >
        <Database size={48} style={{ color: 'var(--primary)', marginBottom: '16px' }} />
        <h2 style={{
          fontSize: '32px',
          fontWeight: '700',
          marginBottom: '8px',
          color: 'var(--text-primary)'
        }}>
          Knowledge Base Search
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
          Search across NFL and NBA game memories, strategies, and player stats
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card"
        style={{ padding: '32px' }}
      >
        <div style={{ display: 'flex', gap: '12px', marginBottom: '24px', flexWrap: 'wrap' }}>
          {['all', 'nfl', 'nba'].map((s) => (
            <motion.button
              key={s}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setSport(s)}
              className="card"
              style={{
                flex: '1 1 150px',
                padding: '16px',
                cursor: 'pointer',
                border: sport === s ? '2px solid var(--primary)' : '2px solid transparent',
                background: sport === s ? 'rgba(0, 217, 255, 0.1)' : 'var(--bg-card)',
                color: sport === s ? 'var(--primary)' : 'var(--text-secondary)',
                fontWeight: '600',
                textAlign: 'center',
                textTransform: 'capitalize',
                transition: 'all 0.2s'
              }}
            >
              {s === 'nfl' && '🏈 '}
              {s === 'nba' && '🏀 '}
              {s === 'all' ? 'All Sports' : s.toUpperCase()}
            </motion.button>
          ))}
        </div>

        <div style={{ position: 'relative', marginBottom: '16px' }}>
          <Search size={20} style={{
            position: 'absolute',
            left: '16px',
            top: '50%',
            transform: 'translateY(-50%)',
            color: 'var(--primary)'
          }} />
          <input
            type="text"
            className="input-field"
            placeholder="Ask anything about games, players, strategies..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            style={{ paddingLeft: '48px', width: '100%' }}
          />
        </div>

        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            style={{
              flex: '1 1 150px',
              padding: '16px',
              background: loading || !query.trim() ? 'var(--bg-hover)' : 'rgba(0, 217, 255, 0.1)',
              color: loading || !query.trim() ? 'var(--text-tertiary)' : 'var(--primary)',
              border: loading || !query.trim() ? '2px solid var(--border-subtle)' : '2px solid var(--primary)',
              borderRadius: 'var(--radius-md)',
              fontWeight: '700',
              fontSize: '16px',
              cursor: loading || !query.trim() ? 'not-allowed' : 'pointer',
              opacity: loading || !query.trim() ? 0.5 : 1
            }}
          >
            {loading ? 'Searching...' : 'Search'}
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            onClick={loadMemories}
            style={{
              padding: '16px 24px',
              background: 'rgba(168, 85, 247, 0.1)',
              color: 'var(--secondary)',
              border: '2px solid var(--secondary)',
              borderRadius: 'var(--radius-md)',
              fontWeight: '600',
              fontSize: '14px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              whiteSpace: 'nowrap'
            }}
          >
            <BookOpen size={16} />
            Refresh
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            onClick={loadDemoData}
            style={{
              padding: '16px 24px',
              background: 'rgba(255, 184, 0, 0.1)',
              color: 'var(--accent)',
              border: '2px solid var(--accent)',
              borderRadius: 'var(--radius-md)',
              fontWeight: '600',
              fontSize: '14px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              whiteSpace: 'nowrap'
            }}
          >
            <Database size={16} />
            Load Demo
          </motion.button>
        </div>
      </motion.div>

      {createSuccess && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          style={{
            padding: '16px 20px',
            background: 'rgba(0, 255, 136, 0.1)',
            border: '1px solid var(--success)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--success)',
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
          }}
        >
          <CheckCircle2 size={20} />
          <span>Memory created successfully!</span>
        </motion.div>
      )}

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="section"
      >
        <div className="section-header">
          <Database className="section-icon" size={24} style={{ color: 'var(--accent)' }} />
          <h2 className="section-title">Memory Management</h2>
          {useMockData && memories.length > 0 && (
            <div style={{
              padding: '6px 12px',
              background: 'var(--accent)',
              borderRadius: 'var(--radius-md)',
              fontSize: '12px',
              fontWeight: '600',
              color: 'var(--text-primary)',
              marginLeft: '12px'
            }}>
              Demo Data
            </div>
          )}
          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            onClick={() => setShowCreateModal(true)}
            style={{
              marginLeft: 'auto',
              padding: '12px 20px',
              background: 'rgba(0, 255, 136, 0.1)',
              color: 'var(--success)',
              border: '2px solid var(--success)',
              borderRadius: 'var(--radius-md)',
              fontWeight: '700',
              fontSize: '14px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <Plus size={18} />
            Create Memory
          </motion.button>
        </div>

        {memories.length > 0 ? (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
            {memories.map((mem, idx) => {
              const health = getMemoryHealth(mem);
              return (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: idx * 0.05 }}
                  whileHover={{ y: -2 }}
                  className="card"
                  style={{ padding: '20px', position: 'relative' }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Trophy size={20} style={{ color: 'var(--primary)' }} />
                      <div
                        style={{
                          width: '8px',
                          height: '8px',
                          borderRadius: '50%',
                          background: getHealthColor(health),
                          boxShadow: `0 0 8px ${getHealthColor(health)}`
                        }}
                        title={`Health: ${health}`}
                      />
                    </div>
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={() => {
                        setMemoryToDelete(mem);
                        setShowDeleteModal(true);
                      }}
                      style={{
                        background: 'rgba(255, 62, 157, 0.1)',
                        border: '1px solid var(--danger)',
                        borderRadius: 'var(--radius-md)',
                        padding: '6px',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center'
                      }}
                    >
                      <Trash2 size={14} style={{ color: 'var(--danger)' }} />
                    </motion.button>
                  </div>

                  <h3 style={{
                    fontSize: '16px',
                    fontWeight: '700',
                    color: 'var(--text-primary)',
                    marginBottom: '12px'
                  }}>
                    {mem.project_name}
                  </h3>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                      <Folder size={14} />
                      <span>{mem.file_count || 0} files</span>
                      <span style={{ color: 'var(--text-tertiary)' }}>•</span>
                      <span>{mem.size_mb || 0} MB</span>
                    </div>
                    {mem.created_at && (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                        <Calendar size={14} />
                        <span>{new Date(mem.created_at).toLocaleDateString()}</span>
                      </div>
                    )}
                  </div>

                  <div className={`badge ${health === 'excellent' ? 'success' : health === 'good' ? 'info' : health === 'fair' ? 'warning' : 'danger'}`}
                    style={{ marginTop: '12px', textTransform: 'capitalize' }}
                  >
                    {health}
                  </div>
                </motion.div>
              );
            })}
          </div>
        ) : (
          <p style={{ color: 'var(--text-tertiary)', textAlign: 'center', padding: '40px 0' }}>
            No memories found. Create your first memory to get started.
          </p>
        )}
      </motion.div>

      {results && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="section"
        >
          <div className="section-header">
            <Search className="section-icon" size={24} />
            <h2 className="section-title">Search Results for "{query}"</h2>
            {useMockData && results.status === 'success' && (
              <div style={{
                padding: '6px 12px',
                background: 'var(--accent)',
                borderRadius: 'var(--radius-md)',
                fontSize: '12px',
                fontWeight: '600',
                color: 'var(--text-primary)',
                marginLeft: '12px'
              }}>
                Demo Data
              </div>
            )}
          </div>

          {results.status === 'success' ? (
            results.results && results.results.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {results.results.map((result, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    whileHover={{ x: 2 }}
                    className="card"
                    style={{ padding: '20px' }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                      <span className="badge info">#{idx + 1}</span>
                      {result.memory && (
                        <span className="badge" style={{
                          background: 'rgba(168, 85, 247, 0.1)',
                          color: 'var(--secondary)'
                        }}>
                          {result.memory}
                        </span>
                      )}
                    </div>
                    <p style={{ lineHeight: '1.6', color: 'var(--text-primary)' }}>
                      {typeof result === 'string' ? result : result.text}
                    </p>
                  </motion.div>
                ))}
              </div>
            ) : (
              <p style={{ color: 'var(--text-tertiary)', textAlign: 'center', padding: '40px 0' }}>
                No results found. Try a different query.
              </p>
            )
          ) : (
            <div style={{
              padding: '20px',
              background: 'rgba(255, 62, 157, 0.1)',
              border: '1px solid var(--danger)',
              borderRadius: 'var(--radius-md)',
              color: 'var(--danger)',
              display: 'flex',
              alignItems: 'center',
              gap: '12px'
            }}>
              <AlertCircle size={20} />
              <span>Error: {results.message}</span>
            </div>
          )}
        </motion.div>
      )}

      {/* Create Memory Modal */}
      <AnimatePresence>
        {showCreateModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowCreateModal(false)}
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              backdropFilter: 'blur(8px)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 1000,
              padding: '20px'
            }}
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              onClick={(e) => e.stopPropagation()}
              className="card-elevated"
              style={{ maxWidth: '500px', width: '100%', maxHeight: '90vh', overflow: 'auto' }}
            >
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '4px',
                background: 'var(--success)'
              }} />

              <div style={{ padding: '32px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                  <h2 style={{ fontSize: '24px', fontWeight: '700', margin: 0 }}>Create New Memory</h2>
                  <motion.button
                    whileHover={{ scale: 1.1, rotate: 90 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => setShowCreateModal(false)}
                    style={{
                      background: 'var(--bg-hover)',
                      border: 'none',
                      borderRadius: 'var(--radius-md)',
                      padding: '8px',
                      cursor: 'pointer',
                      display: 'flex'
                    }}
                  >
                    <X size={20} style={{ color: 'var(--text-secondary)' }} />
                  </motion.button>
                </div>

                <form onSubmit={handleCreateMemory} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                  <div className="input-group">
                    <label className="input-label">Memory Name *</label>
                    <input
                      type="text"
                      className="input-field"
                      value={createForm.memory_name}
                      onChange={(e) => setCreateForm({ ...createForm, memory_name: e.target.value })}
                      placeholder="e.g., nfl-week-1, player-injuries"
                      required
                    />
                  </div>

                  <div className="input-group">
                    <label className="input-label">Sport</label>
                    <select
                      className="input-field"
                      value={createForm.sport}
                      onChange={(e) => setCreateForm({ ...createForm, sport: e.target.value })}
                    >
                      <option value="nfl">NFL</option>
                      <option value="nba">NBA</option>
                      <option value="mlb">MLB</option>
                      <option value="nhl">NHL</option>
                    </select>
                  </div>

                  <div className="input-group">
                    <label className="input-label">Category</label>
                    <select
                      className="input-field"
                      value={createForm.category}
                      onChange={(e) => setCreateForm({ ...createForm, category: e.target.value })}
                    >
                      <option value="games">Games</option>
                      <option value="highlights">Highlights</option>
                      <option value="strategies">Strategies</option>
                      <option value="stats">Player Stats</option>
                    </select>
                  </div>

                  <div className="input-group">
                    <label className="input-label">Documents Directory *</label>
                    <input
                      type="text"
                      className="input-field"
                      value={createForm.docs_dir}
                      onChange={(e) => setCreateForm({ ...createForm, docs_dir: e.target.value })}
                      placeholder="/path/to/documents"
                      required
                    />
                    <p style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
                      Absolute path to directory containing markdown, txt, or PDF files
                    </p>
                  </div>

                  {createError && (
                    <div style={{
                      padding: '12px',
                      background: 'rgba(255, 62, 157, 0.1)',
                      border: '1px solid var(--danger)',
                      borderRadius: 'var(--radius-md)',
                      color: 'var(--danger)',
                      fontSize: '14px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px'
                    }}>
                      <AlertCircle size={16} />
                      {createError}
                    </div>
                  )}

                  <motion.button
                    type="submit"
                    whileHover={{ scale: 1.01 }}
                    whileTap={{ scale: 0.99 }}
                    disabled={creating}
                    style={{
                      padding: '16px',
                      background: creating ? 'var(--bg-hover)' : 'rgba(0, 255, 136, 0.1)',
                      color: creating ? 'var(--text-tertiary)' : 'var(--success)',
                      border: creating ? '2px solid var(--border-subtle)' : '2px solid var(--success)',
                      borderRadius: 'var(--radius-md)',
                      fontWeight: '700',
                      fontSize: '16px',
                      cursor: creating ? 'not-allowed' : 'pointer',
                      opacity: creating ? 0.5 : 1
                    }}
                  >
                    {creating ? 'Creating Memory...' : 'Create Memory'}
                  </motion.button>
                </form>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Delete Confirmation Modal */}
      <AnimatePresence>
        {showDeleteModal && memoryToDelete && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowDeleteModal(false)}
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              backdropFilter: 'blur(8px)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 1000,
              padding: '20px'
            }}
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              onClick={(e) => e.stopPropagation()}
              className="card-elevated"
              style={{ maxWidth: '450px', width: '100%' }}
            >
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '4px',
                background: 'var(--danger)'
              }} />

              <div style={{ padding: '32px', textAlign: 'center' }}>
                <div style={{
                  width: '64px',
                  height: '64px',
                  background: 'rgba(255, 62, 157, 0.1)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 20px'
                }}>
                  <Trash2 size={32} style={{ color: 'var(--danger)' }} />
                </div>

                <h2 style={{ fontSize: '24px', fontWeight: '700', marginBottom: '12px' }}>
                  Delete Memory?
                </h2>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
                  Are you sure you want to delete <strong style={{ color: 'var(--text-primary)' }}>{memoryToDelete.project_name}</strong>? This action cannot be undone.
                </p>

                <div style={{ display: 'flex', gap: '12px' }}>
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => setShowDeleteModal(false)}
                    style={{
                      flex: 1,
                      padding: '16px',
                      background: 'transparent',
                      color: 'var(--text-secondary)',
                      border: '2px solid var(--border-subtle)',
                      borderRadius: 'var(--radius-md)',
                      fontWeight: '600',
                      cursor: 'pointer'
                    }}
                  >
                    Cancel
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.01 }}
                    whileTap={{ scale: 0.99 }}
                    onClick={handleDeleteMemory}
                    disabled={deleting}
                    style={{
                      flex: 1,
                      padding: '16px',
                      background: deleting ? 'var(--bg-hover)' : 'rgba(255, 62, 157, 0.1)',
                      color: deleting ? 'var(--text-tertiary)' : 'var(--danger)',
                      border: deleting ? '2px solid var(--border-subtle)' : '2px solid var(--danger)',
                      borderRadius: 'var(--radius-md)',
                      fontWeight: '700',
                      cursor: deleting ? 'not-allowed' : 'pointer',
                      opacity: deleting ? 0.5 : 1
                    }}
                  >
                    {deleting ? 'Deleting...' : 'Delete'}
                  </motion.button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
