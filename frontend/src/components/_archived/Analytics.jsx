import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { BarChart, Bar, LineChart, Line, AreaChart, Area, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, DollarSign, Percent, Target, Calendar, Award } from 'lucide-react';

const API_URL = 'http://localhost:8000';

// Mock data for demonstration
const MOCK_BETS = [
  { id: 1, bet_type: 'moneyline', sport: 'NFL', team: 'Chiefs', odds: -150, wager_amount: 150, status: 'win', date: '2025-01-20' },
  { id: 2, bet_type: 'spread', sport: 'NBA', team: 'Lakers -5.5', odds: -110, wager_amount: 110, status: 'win', date: '2025-01-20' },
  { id: 3, bet_type: 'totals', sport: 'NFL', team: 'Over 47.5', odds: -105, wager_amount: 105, status: 'loss', date: '2025-01-19' },
  { id: 4, bet_type: 'prop_bet', sport: 'NBA', team: 'LeBron Over 25.5 Pts', odds: 120, wager_amount: 100, status: 'win', date: '2025-01-19' },
  { id: 5, bet_type: 'parlay', sport: 'NFL', team: '3-Team Parlay', odds: 600, wager_amount: 50, status: 'loss', date: '2025-01-18' },
  { id: 6, bet_type: 'moneyline', sport: 'NBA', team: 'Warriors', odds: 180, wager_amount: 100, status: 'win', date: '2025-01-18' },
  { id: 7, bet_type: 'spread', sport: 'NFL', team: '49ers -3', odds: -110, wager_amount: 110, status: 'push', date: '2025-01-17' },
  { id: 8, bet_type: 'totals', sport: 'NBA', team: 'Under 225.5', odds: -115, wager_amount: 115, status: 'win', date: '2025-01-17' },
  { id: 9, bet_type: 'moneyline', sport: 'NFL', team: 'Ravens', odds: -200, wager_amount: 200, status: 'win', date: '2025-01-16' },
  { id: 10, bet_type: 'prop_bet', sport: 'NBA', team: 'Curry Over 4.5 3PM', odds: -120, wager_amount: 120, status: 'loss', date: '2025-01-16' },
  { id: 11, bet_type: 'spread', sport: 'NFL', team: 'Bills -7', odds: -110, wager_amount: 110, status: 'win', date: '2025-01-15' },
  { id: 12, bet_type: 'totals', sport: 'NBA', team: 'Over 218.5', odds: -110, wager_amount: 110, status: 'loss', date: '2025-01-15' },
  { id: 13, bet_type: 'parlay', sport: 'NFL', team: '2-Team Parlay', odds: 260, wager_amount: 75, status: 'win', date: '2025-01-14' },
  { id: 14, bet_type: 'moneyline', sport: 'NBA', team: 'Celtics', odds: -180, wager_amount: 180, status: 'win', date: '2025-01-14' },
  { id: 15, bet_type: 'spread', sport: 'NFL', team: 'Cowboys +3.5', odds: -105, wager_amount: 105, status: 'loss', date: '2025-01-13' },
  { id: 16, bet_type: 'prop_bet', sport: 'NBA', team: 'Giannis Over 30.5 Pts', odds: 110, wager_amount: 100, status: 'win', date: '2025-01-13' },
  { id: 17, bet_type: 'totals', sport: 'NFL', team: 'Under 51.5', odds: -110, wager_amount: 110, status: 'win', date: '2025-01-12' },
  { id: 18, bet_type: 'moneyline', sport: 'NBA', team: 'Nuggets', odds: -140, wager_amount: 140, status: 'loss', date: '2025-01-12' },
  { id: 19, bet_type: 'spread', sport: 'NFL', team: 'Eagles -6', odds: -110, wager_amount: 110, status: 'win', date: '2025-01-11' },
  { id: 20, bet_type: 'parlay', sport: 'NBA', team: '4-Team Parlay', odds: 1200, wager_amount: 50, status: 'loss', date: '2025-01-11' },
];

const Analytics = () => {
  const [bets, setBets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState('all'); // 'all', '30d', '7d'
  const [useMockData, setUseMockData] = useState(false);

  useEffect(() => {
    fetchBets();
  }, []);

  const fetchBets = async () => {
    try {
      const response = await axios.get(`${API_URL}/portfolio`);
      if (response.data && response.data.length > 0) {
        setBets(response.data);
        setUseMockData(false);
      } else {
        // Use mock data when no real data is available
        setBets(MOCK_BETS);
        setUseMockData(true);
      }
    } catch (error) {
      console.error('Failed to fetch bets:', error);
      // Use mock data on error
      setBets(MOCK_BETS);
      setUseMockData(true);
    } finally {
      setLoading(false);
    }
  };

  const resolvedBets = bets.filter(bet => bet.status !== 'pending');
  const wins = resolvedBets.filter(bet => bet.status === 'win').length;
  const losses = resolvedBets.filter(bet => bet.status === 'loss').length;
  const pushes = resolvedBets.filter(bet => bet.status === 'push').length;
  const winRate = resolvedBets.length > 0 ? ((wins / resolvedBets.length) * 100) : 0;
  const totalWagered = bets.reduce((sum, bet) => sum + bet.wager_amount, 0);

  const calculateProfit = () => {
    return resolvedBets.reduce((total, bet) => {
      if (bet.status === 'win') {
        const odds = bet.odds || -110;
        if (odds > 0) {
          return total + (bet.wager_amount * (odds / 100));
        } else {
          return total + (bet.wager_amount * (100 / Math.abs(odds)));
        }
      } else if (bet.status === 'loss') {
        return total - bet.wager_amount;
      }
      return total;
    }, 0);
  };

  const netProfit = calculateProfit();
  const roi = totalWagered > 0 ? ((netProfit / totalWagered) * 100) : 0;

  // Win rate over time data
  const winRateOverTime = (() => {
    const data = [];
    let cumulativeWins = 0;
    let cumulativeBets = 0;

    resolvedBets.forEach((bet, index) => {
      cumulativeBets++;
      if (bet.status === 'win') cumulativeWins++;

      if (index % 5 === 0 || index === resolvedBets.length - 1) {
        data.push({
          bet: cumulativeBets,
          winRate: (cumulativeWins / cumulativeBets) * 100
        });
      }
    });

    return data;
  })();

  // Profit/Loss over time
  const profitOverTime = (() => {
    const data = [];
    let cumulativeProfit = 0;

    resolvedBets.forEach((bet, index) => {
      if (bet.status === 'win') {
        const odds = bet.odds || -110;
        cumulativeProfit += odds > 0 ? (bet.wager_amount * (odds / 100)) : (bet.wager_amount * (100 / Math.abs(odds)));
      } else if (bet.status === 'loss') {
        cumulativeProfit -= bet.wager_amount;
      }

      data.push({
        bet: index + 1,
        profit: cumulativeProfit
      });
    });

    return data;
  })();

  // Bet type distribution
  const betTypeDistribution = (() => {
    const types = {};
    resolvedBets.forEach(bet => {
      types[bet.bet_type] = (types[bet.bet_type] || 0) + 1;
    });

    return Object.entries(types).map(([name, value]) => ({
      name: name.replace('_', ' ').toUpperCase(),
      value,
      wins: resolvedBets.filter(b => b.bet_type === name && b.status === 'win').length
    }));
  })();

  const COLORS = ['#00D9FF', '#A855F7', '#FF3E9D', '#00FF88', '#FFB800'];

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <div className="grid-3">
          <div className="skeleton" style={{ height: '120px' }} />
          <div className="skeleton" style={{ height: '120px' }} />
          <div className="skeleton" style={{ height: '120px' }} />
        </div>
        <div className="skeleton" style={{ height: '400px' }} />
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card-elevated"
        style={{ padding: '40px', textAlign: 'center', position: 'relative' }}
      >
        {useMockData && (
          <div style={{
            position: 'absolute',
            top: '16px',
            right: '16px',
            padding: '6px 12px',
            background: 'var(--accent)',
            borderRadius: 'var(--radius-md)',
            fontSize: '12px',
            fontWeight: '600',
            color: 'var(--text-primary)'
          }}>
            Demo Data
          </div>
        )}
        <TrendingUp size={48} style={{ color: 'var(--success)', marginBottom: '16px' }} />
        <h2 style={{
          fontSize: '32px',
          fontWeight: '700',
          marginBottom: '8px',
          color: 'var(--text-primary)'
        }}>
          Performance Analytics
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
          Track your betting performance and improve your strategy
        </p>
      </motion.div>

      {/* Overview Metrics */}
      <motion.div
        className="grid-3"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, staggerChildren: 0.1 }}
      >
        {[
          { icon: DollarSign, label: 'Total Wagered', value: `$${totalWagered.toFixed(2)}`, color: 'var(--info)' },
          { icon: Percent, label: 'Win Rate', value: `${winRate.toFixed(1)}%`, color: 'var(--success)', subtitle: `${wins}W - ${losses}L - ${pushes}P` },
          { icon: Target, label: 'ROI', value: `${roi >= 0 ? '+' : ''}${roi.toFixed(1)}%`, color: roi >= 0 ? 'var(--success)' : 'var(--danger)' },
        ].map((metric, index) => (
          <motion.div
            key={index}
            className="metric-card"
            whileHover={{ y: -2 }}
            style={{ textAlign: 'center' }}
          >
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '16px' }}>
              <div style={{
                padding: '12px',
                background: 'var(--bg-elevated)',
                borderRadius: '50%',
                border: `2px solid ${metric.color}`,
                boxShadow: `0 0 20px ${metric.color}33`
              }}>
                <metric.icon size={24} style={{ color: metric.color }} />
              </div>
            </div>
            <div className="metric-label">{metric.label}</div>
            <div className="metric-value" style={{ color: metric.color }}>
              {metric.value}
            </div>
            {metric.subtitle && (
              <div style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
                {metric.subtitle}
              </div>
            )}
          </motion.div>
        ))}
      </motion.div>

      {/* Charts Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '24px' }}>
        {/* Win Rate Over Time */}
        {winRateOverTime.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="section"
          >
            <div className="section-header">
              <TrendingUp className="section-icon" size={24} style={{ color: 'var(--success)' }} />
              <h2 className="section-title">Win Rate Trend</h2>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={winRateOverTime}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
                <XAxis dataKey="bet" stroke="var(--text-secondary)" />
                <YAxis stroke="var(--text-secondary)" domain={[0, 100]} />
                <Tooltip
                  contentStyle={{
                    background: 'var(--bg-elevated)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-primary)'
                  }}
                />
                <Line type="monotone" dataKey="winRate" stroke="var(--success)" strokeWidth={3} dot={{ fill: 'var(--success)' }} />
              </LineChart>
            </ResponsiveContainer>
          </motion.div>
        )}

        {/* Cumulative Profit */}
        {profitOverTime.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="section"
          >
            <div className="section-header">
              <DollarSign className="section-icon" size={24} style={{ color: 'var(--primary)' }} />
              <h2 className="section-title">Cumulative Profit</h2>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={profitOverTime}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
                <XAxis dataKey="bet" stroke="var(--text-secondary)" />
                <YAxis stroke="var(--text-secondary)" />
                <Tooltip
                  contentStyle={{
                    background: 'var(--bg-elevated)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-primary)'
                  }}
                />
                <Area type="monotone" dataKey="profit" stroke="var(--primary)" strokeWidth={3} fillOpacity={0.1} fill="var(--primary)" />
              </AreaChart>
            </ResponsiveContainer>
          </motion.div>
        )}
      </div>

      {/* Bet Type Distribution */}
      {betTypeDistribution.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="section"
        >
          <div className="section-header">
            <Award className="section-icon" size={24} style={{ color: 'var(--accent)' }} />
            <h2 className="section-title">Bet Type Performance</h2>
          </div>

          <div className="chart-grid">
            {/* Modern Donut Chart */}
            <div style={{ position: 'relative' }}>
              <ResponsiveContainer width="100%" height={320}>
                <PieChart>
                  <Pie
                    data={betTypeDistribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={85}
                    outerRadius={120}
                    paddingAngle={2}
                    dataKey="value"
                    stroke="none"
                  >
                    {betTypeDistribution.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background: 'var(--bg-elevated)',
                      border: '1px solid var(--border-strong)',
                      borderRadius: '8px',
                      color: 'var(--text-primary)',
                      fontSize: '13px',
                      padding: '8px 12px',
                      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              {/* Center Label */}
              <div style={{
                position: 'absolute',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                textAlign: 'center',
                pointerEvents: 'none'
              }}>
                <div style={{ fontSize: '32px', fontWeight: '700', color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
                  {resolvedBets.length}
                </div>
                <div style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px', fontWeight: '500' }}>
                  Total Bets
                </div>
              </div>
            </div>

            {/* Clean Legend with Stats */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {betTypeDistribution.map((type, index) => {
                const percentage = ((type.value / resolvedBets.length) * 100).toFixed(1);
                const winRate = ((type.wins / type.value) * 100).toFixed(0);

                return (
                  <div
                    key={index}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '16px 20px',
                      background: 'var(--bg-elevated)',
                      borderRadius: '10px',
                      border: '1px solid var(--border-subtle)',
                      transition: 'all 0.15s cubic-bezier(0.4, 0, 0.2, 1)',
                      cursor: 'pointer'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.borderColor = COLORS[index % COLORS.length];
                      e.currentTarget.style.transform = 'translateX(4px)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.borderColor = 'var(--border-subtle)';
                      e.currentTarget.style.transform = 'translateX(0)';
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '14px', flex: 1 }}>
                      <div style={{
                        width: '12px',
                        height: '12px',
                        borderRadius: '3px',
                        background: COLORS[index % COLORS.length],
                        flexShrink: 0
                      }} />
                      <div style={{ flex: 1 }}>
                        <div style={{
                          fontWeight: '600',
                          color: 'var(--text-primary)',
                          fontSize: '14px',
                          letterSpacing: '-0.01em',
                          marginBottom: '4px'
                        }}>
                          {type.name}
                        </div>
                        <div style={{
                          fontSize: '12px',
                          color: 'var(--text-secondary)',
                          fontWeight: '500'
                        }}>
                          {type.value} bets ({percentage}%)
                        </div>
                      </div>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '6px' }}>
                      <div className={`badge ${Number(winRate) >= 50 ? 'success' : 'danger'}`}>
                        {winRate}% Win
                      </div>
                      <div style={{
                        fontSize: '11px',
                        color: 'var(--text-tertiary)',
                        fontWeight: '600',
                        letterSpacing: '0.02em'
                      }}>
                        {type.wins}W - {type.value - type.wins}L
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </motion.div>
      )}

      {resolvedBets.length === 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
          style={{ padding: '60px', textAlign: 'center' }}
        >
          <Calendar size={48} style={{ color: 'var(--text-tertiary)', marginBottom: '16px', opacity: 0.5 }} />
          <p style={{ color: 'var(--text-tertiary)', fontSize: '16px', marginBottom: '8px' }}>
            No betting history yet
          </p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
            Place and resolve some bets to see your analytics
          </p>
        </motion.div>
      )}
    </div>
  );
};

export default Analytics;
