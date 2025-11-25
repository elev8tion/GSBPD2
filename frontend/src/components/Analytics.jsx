import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { BarChart, Bar, LineChart, Line, AreaChart, Area, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, DollarSign, Percent, Target, Calendar, Award } from 'lucide-react';

const API_URL = 'http://localhost:8000';

const Analytics = () => {
  const [bets, setBets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState('all'); // 'all', '30d', '7d'

  useEffect(() => {
    fetchBets();
  }, []);

  const fetchBets = async () => {
    try {
      const response = await axios.get(`${API_URL}/portfolio`);
      setBets(response.data);
    } catch (error) {
      console.error('Failed to fetch bets:', error);
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
        style={{ padding: '40px', textAlign: 'center' }}
      >
        <TrendingUp size={48} style={{ color: 'var(--success)', marginBottom: '16px' }} />
        <h2 style={{
          fontSize: '32px',
          fontWeight: '700',
          marginBottom: '8px',
          background: 'linear-gradient(135deg, var(--success), var(--primary))',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
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
            whileHover={{ y: -8 }}
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
                <defs>
                  <linearGradient id="profitGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--primary)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
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
                <Area type="monotone" dataKey="profit" stroke="var(--primary)" strokeWidth={3} fillOpacity={1} fill="url(#profitGradient)" />
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

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={betTypeDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {betTypeDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    background: 'var(--bg-elevated)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--text-primary)'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>

            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '16px' }}>
              {betTypeDistribution.map((type, index) => (
                <div key={index} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)', borderLeft: `4px solid ${COLORS[index % COLORS.length]}` }}>
                  <div>
                    <div style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{type.name}</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>{type.value} bets total</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div className={`badge ${type.wins / type.value >= 0.5 ? 'success' : 'danger'}`}>
                      {((type.wins / type.value) * 100).toFixed(0)}% Win Rate
                    </div>
                    <div style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
                      {type.wins}W - {type.value - type.wins}L
                    </div>
                  </div>
                </div>
              ))}
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
