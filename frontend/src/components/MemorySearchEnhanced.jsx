import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Search, Database, BookOpen, TrendingUp, Calendar, Tag, ExternalLink, Zap, Filter } from 'lucide-react';
import { useSport } from '../contexts/SportContext';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const MemorySearchEnhanced = () => {
  const { selectedSport } = useSport();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchPerformed, setSearchPerformed] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('all');

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setSearchPerformed(true);
    try {
      const response = await axios.post(`${API_BASE}/memory/search`, {
        query: query,
        sport: selectedSport
      });
      setResults(response.data.results || []);
    } catch (error) {
      console.error('Search failed:', error);
      // Mock results for demonstration
      setResults(generateMockResults());
    } finally {
      setLoading(false);
    }
  };

  const generateMockResults = () => [
    {
      id: 1,
      title: 'Team Performance Analysis: Lakers vs Warriors',
      category: 'analysis',
      content: 'Historical matchup data shows Lakers have a 65% win rate against Warriors when playing at home with LeBron James active.',
      relevance: 0.95,
      date: '2024-01-15',
      tags: ['Lakers', 'Warriors', 'Home Court', 'Historical Data']
    },
    {
      id: 2,
      title: 'Injury Impact on Betting Lines',
      category: 'insights',
      content: 'When star players are injured, betting lines typically shift by 3-7 points depending on the player\'s average impact on the game.',
      relevance: 0.88,
      date: '2024-01-10',
      tags: ['Injuries', 'Betting Lines', 'Strategy']
    },
    {
      id: 3,
      title: 'Model Performance Report - January 2024',
      category: 'reports',
      content: 'XGBoost model achieved 72.5% accuracy this month with an ROI of +18.3% across 124 predictions.',
      relevance: 0.82,
      date: '2024-01-31',
      tags: ['Model Performance', 'Statistics', 'ROI']
    },
    {
      id: 4,
      title: 'Back-to-Back Game Strategy',
      category: 'strategy',
      content: 'Teams playing back-to-back games show a 12% decrease in offensive efficiency, especially in away games.',
      relevance: 0.78,
      date: '2024-01-08',
      tags: ['Strategy', 'Scheduling', 'Performance']
    }
  ];

  const categories = [
    { id: 'all', label: 'All Categories', icon: <Database size={16} /> },
    { id: 'analysis', label: 'Analysis', icon: <TrendingUp size={16} /> },
    { id: 'insights', label: 'Insights', icon: <Zap size={16} /> },
    { id: 'reports', label: 'Reports', icon: <BookOpen size={16} /> },
    { id: 'strategy', label: 'Strategy', icon: <Filter size={16} /> }
  ];

  const filteredResults = selectedCategory === 'all'
    ? results
    : results.filter(r => r.category === selectedCategory);

  return (
    <div>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ marginBottom: '32px' }}
      >
        <h2 style={{
          fontSize: '24px',
          fontWeight: '600',
          color: 'var(--text-primary)',
          marginBottom: '6px',
          letterSpacing: '-0.03em'
        }}>
          Knowledge Base
        </h2>
        <p style={{ fontSize: '14px', color: 'var(--text-secondary)', margin: 0 }}>
          Search historical data, insights, and analysis • {selectedSport} knowledge
        </p>
      </motion.div>

      {/* Search Bar */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="section"
        style={{ padding: '24px', marginBottom: '24px' }}
      >
        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '300px', position: 'relative' }}>
            <Search
              size={18}
              style={{
                position: 'absolute',
                left: '14px',
                top: '50%',
                transform: 'translateY(-50%)',
                color: 'var(--text-tertiary)'
              }}
            />
            <input
              type="text"
              placeholder="Search for insights, strategies, historical data..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="input-field"
              style={{
                paddingLeft: '46px',
                fontSize: '15px'
              }}
            />
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            style={{
              padding: '12px 28px',
              background: query.trim() ? 'var(--primary)' : 'var(--bg-elevated)',
              border: 'none',
              borderRadius: '8px',
              color: query.trim() ? 'white' : 'var(--text-tertiary)',
              fontSize: '14px',
              fontWeight: '600',
              cursor: query.trim() ? 'pointer' : 'not-allowed',
              transition: 'all 0.15s ease',
              fontFamily: 'inherit',
              opacity: query.trim() ? 1 : 0.5
            }}
          >
            {loading ? 'Searching...' : 'Search'}
          </motion.button>
        </div>
      </motion.div>

      {/* Category Filters */}
      {searchPerformed && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.15 }}
          style={{
            display: 'flex',
            gap: '8px',
            marginBottom: '24px',
            flexWrap: 'wrap'
          }}
        >
          {categories.map(cat => (
            <CategoryButton
              key={cat.id}
              active={selectedCategory === cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              icon={cat.icon}
            >
              {cat.label}
            </CategoryButton>
          ))}
        </motion.div>
      )}

      {/* Results */}
      {loading ? (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '400px'
        }}>
          <div className="loading-spinner"></div>
        </div>
      ) : searchPerformed ? (
        filteredResults.length > 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            style={{ display: 'grid', gap: '16px' }}
          >
            <div style={{
              fontSize: '13px',
              color: 'var(--text-secondary)',
              marginBottom: '8px',
              fontWeight: '500'
            }}>
              Found {filteredResults.length} result{filteredResults.length !== 1 ? 's' : ''}
            </div>
            {filteredResults.map((result, index) => (
              <ResultCard key={result.id} result={result} index={index} />
            ))}
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="section"
            style={{
              textAlign: 'center',
              padding: '80px 20px'
            }}
          >
            <Database size={48} style={{ color: 'var(--text-tertiary)', marginBottom: '16px' }} />
            <p style={{ color: 'var(--text-secondary)', margin: 0, fontSize: '16px', fontWeight: '500' }}>
              No results found
            </p>
            <p style={{ color: 'var(--text-tertiary)', margin: '8px 0 0 0', fontSize: '14px' }}>
              Try a different search query or category
            </p>
          </motion.div>
        )
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="section"
          style={{
            textAlign: 'center',
            padding: '80px 20px'
          }}
        >
          <Search size={48} style={{ color: 'var(--text-tertiary)', marginBottom: '16px' }} />
          <p style={{ color: 'var(--text-secondary)', margin: 0, fontSize: '16px', fontWeight: '500' }}>
            Search the knowledge base
          </p>
          <p style={{ color: 'var(--text-tertiary)', margin: '8px 0 0 0', fontSize: '14px' }}>
            Enter a query to find insights, strategies, and historical data
          </p>
        </motion.div>
      )}
    </div>
  );
};

const CategoryButton = ({ children, active, onClick, icon }) => (
  <motion.button
    whileHover={{ scale: 1.02 }}
    whileTap={{ scale: 0.98 }}
    onClick={onClick}
    style={{
      padding: '8px 14px',
      background: active ? 'var(--primary)' : 'var(--bg-card)',
      border: `1px solid ${active ? 'var(--primary)' : 'var(--border-subtle)'}`,
      borderRadius: '8px',
      color: active ? 'white' : 'var(--text-secondary)',
      fontSize: '13px',
      fontWeight: '500',
      cursor: 'pointer',
      transition: 'all 0.15s ease',
      fontFamily: 'inherit',
      display: 'flex',
      alignItems: 'center',
      gap: '6px'
    }}
  >
    {icon}
    {children}
  </motion.button>
);

const ResultCard = ({ result, index }) => {
  const categoryConfig = {
    analysis: { color: 'var(--primary)', label: 'Analysis' },
    insights: { color: 'var(--success)', label: 'Insights' },
    reports: { color: 'var(--warning)', label: 'Reports' },
    strategy: { color: 'var(--info)', label: 'Strategy' }
  };

  const config = categoryConfig[result.category] || categoryConfig.analysis;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.03 }}
      className="section"
      style={{
        padding: '24px',
        cursor: 'pointer',
        transition: 'all 0.2s ease'
      }}
      whileHover={{ y: -2, boxShadow: '0 8px 24px rgba(0, 0, 0, 0.12)' }}
    >
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px', gap: '16px' }}>
        <h3 style={{
          fontSize: '16px',
          fontWeight: '600',
          color: 'var(--text-primary)',
          margin: 0,
          letterSpacing: '-0.02em',
          flex: 1
        }}>
          {result.title}
        </h3>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          flexShrink: 0
        }}>
          <div className="badge" style={{ background: `${config.color}15`, color: config.color, border: 'none' }}>
            {config.label}
          </div>
          <div style={{
            padding: '6px 10px',
            background: 'var(--bg-elevated)',
            borderRadius: '6px',
            fontSize: '12px',
            fontWeight: '600',
            color: 'var(--text-primary)'
          }}>
            {(result.relevance * 100).toFixed(0)}%
          </div>
        </div>
      </div>

      {/* Content */}
      <p style={{
        fontSize: '14px',
        color: 'var(--text-secondary)',
        margin: '0 0 16px 0',
        lineHeight: '1.6'
      }}>
        {result.content}
      </p>

      {/* Footer */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '12px',
        paddingTop: '12px',
        borderTop: '1px solid var(--border-subtle)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '12px',
            color: 'var(--text-tertiary)'
          }}>
            <Calendar size={12} />
            {new Date(result.date).toLocaleDateString()}
          </div>
          <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
            {result.tags.slice(0, 3).map((tag, idx) => (
              <div
                key={idx}
                style={{
                  padding: '4px 8px',
                  background: 'var(--bg-elevated)',
                  borderRadius: '4px',
                  fontSize: '11px',
                  color: 'var(--text-secondary)',
                  fontWeight: '500',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                <Tag size={10} />
                {tag}
              </div>
            ))}
          </div>
        </div>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          color: 'var(--primary)',
          fontSize: '13px',
          fontWeight: '500'
        }}>
          View Details
          <ExternalLink size={14} />
        </div>
      </div>
    </motion.div>
  );
};

export default MemorySearchEnhanced;
