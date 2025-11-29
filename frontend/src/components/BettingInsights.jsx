import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { TrendingUp, RefreshCw, DollarSign, Target, Clock, Star, BarChart3 } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const BettingInsights = () => {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBettingInsights();
  }, []);

  const fetchBettingInsights = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE}/nba/betting-insights`);
      setInsights(response.data.insights || []);
    } catch (err) {
      console.error('Error fetching betting insights:', err);
      setError('Failed to load betting insights');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  };

  const getOddsColor = (odds) => {
    if (!odds) return 'var(--text-tertiary)';
    if (odds < 1.5) return 'var(--success)';  // Heavy favorite
    if (odds < 2.0) return 'var(--info)';     // Moderate favorite
    return 'var(--warning)';                  // Underdog
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <div className="skeleton" style={{ height: '120px' }} />
        <div className="grid-2">
          <div className="skeleton" style={{ height: '600px' }} />
          <div className="skeleton" style={{ height: '600px' }} />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
        style={{ padding: '60px', textAlign: 'center' }}
      >
        <div style={{
          width: '64px',
          height: '64px',
          margin: '0 auto 24px',
          borderRadius: '50%',
          background: 'rgba(255, 62, 157, 0.1)',
          border: '2px solid var(--danger)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <TrendingUp size={32} style={{ color: 'var(--danger)' }} />
        </div>
        <p style={{ color: 'var(--danger)', fontSize: '16px', marginBottom: '8px', fontWeight: '600' }}>
          {error}
        </p>
        <p style={{ color: 'var(--text-tertiary)', fontSize: '14px', marginBottom: '24px' }}>
          Please try refreshing or check back later
        </p>
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={fetchBettingInsights}
          className="btn btn-primary"
        >
          <RefreshCw size={16} />
          Try Again
        </motion.button>
      </motion.div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      {/* Header Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card-elevated"
        style={{ padding: '32px', position: 'relative' }}
      >
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '3px',
          background: 'linear-gradient(90deg, var(--primary), var(--secondary))'
        }} />
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{
              padding: '14px',
              background: 'var(--bg-elevated)',
              borderRadius: '50%',
              border: '2px solid var(--primary)',
              boxShadow: 'var(--glow-primary)'
            }}>
              <DollarSign size={28} style={{ color: 'var(--primary)' }} />
            </div>
            <div>
              <h1 style={{
                fontSize: '28px',
                fontWeight: '700',
                margin: '0 0 4px 0',
                color: 'var(--text-primary)',
                letterSpacing: '-0.02em'
              }}>
                Betting Insights
              </h1>
              <p style={{ color: 'var(--text-secondary)', fontSize: '14px', margin: '0' }}>
                AI-powered analysis from DraftKings live odds
              </p>
            </div>
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={fetchBettingInsights}
            className="btn btn-primary"
            style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
          >
            <RefreshCw size={16} />
            Refresh Data
          </motion.button>
        </div>
      </motion.div>

      {/* Quick Stats */}
      {insights.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid-3"
        >
          <motion.div
            whileHover={{ y: -4 }}
            className="metric-card"
            style={{ textAlign: 'center' }}
          >
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '16px' }}>
              <div style={{
                padding: '12px',
                background: 'var(--bg-elevated)',
                borderRadius: '50%',
                border: '2px solid var(--info)',
                boxShadow: '0 0 20px rgba(99, 102, 241, 0.15)'
              }}>
                <BarChart3 size={24} style={{ color: 'var(--info)' }} />
              </div>
            </div>
            <div className="metric-label">Games Available</div>
            <div className="metric-value" style={{ color: 'var(--info)' }}>
              {insights.length}
            </div>
          </motion.div>

          <motion.div
            whileHover={{ y: -4 }}
            className="metric-card"
            style={{ textAlign: 'center' }}
          >
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '16px' }}>
              <div style={{
                padding: '12px',
                background: 'var(--bg-elevated)',
                borderRadius: '50%',
                border: '2px solid var(--primary)',
                boxShadow: 'var(--glow-primary)'
              }}>
                <Target size={24} style={{ color: 'var(--primary)' }} />
              </div>
            </div>
            <div className="metric-label">Live Markets</div>
            <div className="metric-value" style={{ color: 'var(--primary)' }}>
              {insights.length * 2}
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
              Spread & Total
            </div>
          </motion.div>

          <motion.div
            whileHover={{ y: -4 }}
            className="metric-card"
            style={{ textAlign: 'center' }}
          >
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '16px' }}>
              <div style={{
                padding: '12px',
                background: 'var(--bg-elevated)',
                borderRadius: '50%',
                border: '2px solid var(--success)',
                boxShadow: 'var(--glow-primary)'
              }}>
                <Star size={24} style={{ color: 'var(--success)' }} />
              </div>
            </div>
            <div className="metric-label">AI Analyzed</div>
            <div className="metric-value" style={{ color: 'var(--success)' }}>
              {insights.length}
            </div>
            <div style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
              Full insights
            </div>
          </motion.div>
        </motion.div>
      )}

      {/* Insights Grid */}
      <div className="insights-grid">
        {insights.map((insight, index) => (
          <motion.div
            key={insight.game_id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="section"
          >
            {/* Game Header */}
            <div className="section-header">
              <Clock className="section-icon" size={20} style={{ color: 'var(--warning)' }} />
              <h2 className="section-title">{insight.matchup}</h2>
            </div>
            <div style={{
              fontSize: '13px',
              color: 'var(--text-secondary)',
              marginBottom: '20px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <Clock size={14} />
              {formatTime(insight.commence_time)}
            </div>

            {/* Team Stats Comparison */}
            {insight.team_stats?.home && insight.team_stats?.away && (
              <div style={{
                background: 'var(--bg-elevated)',
                borderRadius: 'var(--radius-md)',
                padding: '20px',
                marginBottom: '20px',
                border: '1px solid var(--border-subtle)'
              }}>
                <div style={{
                  fontSize: '11px',
                  color: 'var(--text-secondary)',
                  textTransform: 'uppercase',
                  marginBottom: '16px',
                  fontWeight: '600',
                  letterSpacing: '0.05em'
                }}>
                  Season Averages
                </div>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(3, 1fr)',
                  gap: '16px'
                }}>
                  {/* Points Per Game */}
                  <div>
                    <div style={{
                      fontSize: '11px',
                      color: 'var(--text-tertiary)',
                      textAlign: 'center',
                      marginBottom: '8px',
                      fontWeight: '500'
                    }}>
                      PPG
                    </div>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      gap: '8px'
                    }}>
                      <span style={{
                        fontSize: '14px',
                        fontWeight: '600',
                        color: parseFloat(insight.team_stats.home.pts) > parseFloat(insight.team_stats.away.pts)
                          ? 'var(--success)' : 'var(--text-secondary)'
                      }}>
                        {insight.team_stats.home.pts}
                      </span>
                      <span style={{ fontSize: '11px', color: 'var(--text-tertiary)' }}>vs</span>
                      <span style={{
                        fontSize: '14px',
                        fontWeight: '600',
                        color: parseFloat(insight.team_stats.away.pts) > parseFloat(insight.team_stats.home.pts)
                          ? 'var(--success)' : 'var(--text-secondary)'
                      }}>
                        {insight.team_stats.away.pts}
                      </span>
                    </div>
                  </div>

                  {/* Rebounds Per Game */}
                  <div>
                    <div style={{
                      fontSize: '11px',
                      color: 'var(--text-tertiary)',
                      textAlign: 'center',
                      marginBottom: '8px',
                      fontWeight: '500'
                    }}>
                      RPG
                    </div>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      gap: '8px'
                    }}>
                      <span style={{
                        fontSize: '14px',
                        fontWeight: '600',
                        color: parseFloat(insight.team_stats.home.reb) > parseFloat(insight.team_stats.away.reb)
                          ? 'var(--success)' : 'var(--text-secondary)'
                      }}>
                        {insight.team_stats.home.reb}
                      </span>
                      <span style={{ fontSize: '11px', color: 'var(--text-tertiary)' }}>vs</span>
                      <span style={{
                        fontSize: '14px',
                        fontWeight: '600',
                        color: parseFloat(insight.team_stats.away.reb) > parseFloat(insight.team_stats.home.reb)
                          ? 'var(--success)' : 'var(--text-secondary)'
                      }}>
                        {insight.team_stats.away.reb}
                      </span>
                    </div>
                  </div>

                  {/* Assists Per Game */}
                  <div>
                    <div style={{
                      fontSize: '11px',
                      color: 'var(--text-tertiary)',
                      textAlign: 'center',
                      marginBottom: '8px',
                      fontWeight: '500'
                    }}>
                      APG
                    </div>
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      gap: '8px'
                    }}>
                      <span style={{
                        fontSize: '14px',
                        fontWeight: '600',
                        color: parseFloat(insight.team_stats.home.ast) > parseFloat(insight.team_stats.away.ast)
                          ? 'var(--success)' : 'var(--text-secondary)'
                      }}>
                        {insight.team_stats.home.ast}
                      </span>
                      <span style={{ fontSize: '11px', color: 'var(--text-tertiary)' }}>vs</span>
                      <span style={{
                        fontSize: '14px',
                        fontWeight: '600',
                        color: parseFloat(insight.team_stats.away.ast) > parseFloat(insight.team_stats.home.ast)
                          ? 'var(--success)' : 'var(--text-secondary)'
                      }}>
                        {insight.team_stats.away.ast}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Betting Lines */}
            <div className="stats-grid-2" style={{ marginBottom: '20px' }}>
              {/* Spread */}
              <div className="metric-card">
                <div className="metric-label">Spread</div>
                <div className="metric-value" style={{ color: 'var(--primary)' }}>
                  {insight.spread > 0 ? '+' : ''}{insight.spread}
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '6px' }}>
                  Favorite: {insight.favorite}
                </div>
              </div>

              {/* Total */}
              <div className="metric-card">
                <div className="metric-label">Total (O/U)</div>
                <div className="metric-value" style={{ color: 'var(--secondary)' }}>
                  {insight.total}
                </div>
                <div style={{
                  fontSize: '12px',
                  color: 'var(--text-tertiary)',
                  marginTop: '6px',
                  display: 'flex',
                  justifyContent: 'space-between'
                }}>
                  <span>Over: {insight.betting_analysis.over_odds}</span>
                  <span>Under: {insight.betting_analysis.under_odds}</span>
                </div>
              </div>
            </div>

            {/* Implied Probabilities */}
            {insight.implied_probabilities.home && (
              <div style={{
                background: 'var(--bg-elevated)',
                borderRadius: 'var(--radius-md)',
                padding: '20px',
                marginBottom: '20px',
                border: '1px solid var(--border-subtle)'
              }}>
                <div style={{
                  fontSize: '11px',
                  color: 'var(--text-secondary)',
                  textTransform: 'uppercase',
                  marginBottom: '12px',
                  fontWeight: '600',
                  letterSpacing: '0.05em'
                }}>
                  Implied Probabilities
                </div>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '12px'
                }}>
                  <div>
                    <div style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                      Home
                    </div>
                    <div style={{
                      fontSize: '20px',
                      fontWeight: '700',
                      color: getOddsColor(insight.implied_probabilities.home / 100)
                    }}>
                      {insight.implied_probabilities.home}%
                    </div>
                  </div>
                  <div style={{
                    fontSize: '12px',
                    color: 'var(--text-tertiary)',
                    fontWeight: '500'
                  }}>
                    vs
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                      Away
                    </div>
                    <div style={{
                      fontSize: '20px',
                      fontWeight: '700',
                      color: getOddsColor(insight.implied_probabilities.away / 100)
                    }}>
                      {insight.implied_probabilities.away}%
                    </div>
                  </div>
                </div>
                {insight.betting_analysis.market_efficiency && (
                  <div style={{
                    paddingTop: '12px',
                    borderTop: '1px solid var(--border-subtle)',
                    fontSize: '12px',
                    color: 'var(--text-secondary)'
                  }}>
                    Market Efficiency: <span style={{ color: 'var(--text-primary)', fontWeight: '600' }}>
                      {insight.betting_analysis.market_efficiency}%
                    </span>
                    <span style={{ color: 'var(--text-tertiary)', marginLeft: '8px' }}>(includes vig)</span>
                  </div>
                )}
              </div>
            )}

            {/* Key Players */}
            {insight.top_players?.home && insight.top_players?.away && (
              <div style={{
                background: 'var(--bg-elevated)',
                borderRadius: 'var(--radius-md)',
                padding: '20px',
                marginBottom: '20px',
                border: '1px solid var(--border-subtle)'
              }}>
                <div style={{
                  fontSize: '11px',
                  color: 'var(--text-secondary)',
                  textTransform: 'uppercase',
                  marginBottom: '16px',
                  fontWeight: '600',
                  letterSpacing: '0.05em'
                }}>
                  Top Scorers
                </div>
                <div className="stats-grid-2" style={{ gap: '20px' }}>
                  {/* Home Team Players */}
                  <div>
                    <div style={{
                      fontSize: '11px',
                      color: 'var(--text-tertiary)',
                      marginBottom: '12px',
                      fontWeight: '600'
                    }}>
                      Home
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                      {insight.top_players.home.slice(0, 3).map((player, idx) => (
                        <div
                          key={idx}
                          style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center'
                          }}
                        >
                          <span style={{
                            fontSize: '13px',
                            color: 'var(--text-primary)',
                            flex: 1,
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                            marginRight: '8px'
                          }}>
                            {player.name}
                          </span>
                          <span className="badge info">
                            {player.ppg} PPG
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Away Team Players */}
                  <div>
                    <div style={{
                      fontSize: '11px',
                      color: 'var(--text-tertiary)',
                      marginBottom: '12px',
                      fontWeight: '600'
                    }}>
                      Away
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                      {insight.top_players.away.slice(0, 3).map((player, idx) => (
                        <div
                          key={idx}
                          style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center'
                          }}
                        >
                          <span style={{
                            fontSize: '13px',
                            color: 'var(--text-primary)',
                            flex: 1,
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                            marginRight: '8px'
                          }}>
                            {player.name}
                          </span>
                          <span className="badge warning">
                            {player.ppg} PPG
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* AI Recommendation */}
            <div style={{
              background: 'rgba(0, 217, 255, 0.08)',
              border: '1px solid rgba(0, 217, 255, 0.2)',
              borderRadius: 'var(--radius-md)',
              padding: '20px'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                marginBottom: '12px'
              }}>
                <TrendingUp size={16} style={{ color: 'var(--primary)' }} />
                <div style={{
                  fontSize: '11px',
                  color: 'var(--primary)',
                  textTransform: 'uppercase',
                  fontWeight: '600',
                  letterSpacing: '0.05em'
                }}>
                  AI Analysis
                </div>
              </div>
              <div style={{
                fontSize: '14px',
                color: 'var(--text-primary)',
                lineHeight: '1.6',
                letterSpacing: '-0.01em'
              }}>
                {insight.recommendation}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Empty State */}
      {insights.length === 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
          style={{ padding: '60px', textAlign: 'center' }}
        >
          <div style={{
            width: '64px',
            height: '64px',
            margin: '0 auto 24px',
            borderRadius: '50%',
            background: 'var(--bg-elevated)',
            border: '2px solid var(--border-strong)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <DollarSign size={32} style={{ color: 'var(--text-tertiary)' }} />
          </div>
          <p style={{ color: 'var(--text-primary)', fontSize: '16px', marginBottom: '8px', fontWeight: '600' }}>
            No betting insights available
          </p>
          <p style={{ color: 'var(--text-tertiary)', fontSize: '14px' }}>
            Check back later for AI-powered betting insights
          </p>
        </motion.div>
      )}

      {/* Disclaimer */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        style={{
          background: 'rgba(255, 184, 0, 0.08)',
          border: '1px solid rgba(255, 184, 0, 0.2)',
          borderRadius: 'var(--radius-md)',
          padding: '16px 20px',
          textAlign: 'center'
        }}
      >
        <p style={{
          fontSize: '13px',
          color: 'var(--warning)',
          margin: 0,
          fontWeight: '500'
        }}>
          ⚠️ For entertainment purposes only. Bet responsibly. Never wager more than you can afford to lose.
        </p>
      </motion.div>
    </div>
  );
};

export default BettingInsights;
