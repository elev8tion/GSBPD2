import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Target, BarChart3, PieChart, Activity, Calendar, DollarSign, Percent, Award } from 'lucide-react';
import { useSport } from '../contexts/SportContext';
import { ResponsiveContainer, LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend, PieChart as RPieChart, Pie, Cell } from 'recharts';

const AnalyticsEnhanced = () => {
  const { selectedSport } = useSport();
  const [timeframe, setTimeframe] = useState('30d'); // 7d, 30d, 90d, all

  // Mock data - would come from API
  const performanceData = [
    { date: 'Week 1', profit: 120, roi: 15, wins: 3, losses: 1 },
    { date: 'Week 2', profit: -50, roi: -8, wins: 1, losses: 3 },
    { date: 'Week 3', profit: 200, roi: 25, wins: 4, losses: 1 },
    { date: 'Week 4', profit: 150, roi: 18, wins: 3, losses: 2 },
  ];

  const categoryData = [
    { name: 'Spread', value: 45, color: '#00d9ff' },
    { name: 'Moneyline', value: 30, color: '#6366f1' },
    { name: 'Over/Under', value: 25, color: '#00ff88' }
  ];

  const metrics = {
    totalProfit: 420,
    totalBets: 24,
    winRate: 62.5,
    avgOdds: -110,
    roi: 18.5,
    longestStreak: 5,
    bestCategory: 'Spread',
    avgWager: 100
  };

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
          Performance Analytics
        </h2>
        <p style={{ fontSize: '14px', color: 'var(--text-secondary)', margin: 0 }}>
          Track your betting performance • {selectedSport} insights
        </p>
      </motion.div>

      {/* Timeframe Selector */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        style={{
          display: 'flex',
          gap: '8px',
          marginBottom: '24px',
          flexWrap: 'wrap'
        }}
      >
        {['7d', '30d', '90d', 'all'].map(period => (
          <motion.button
            key={period}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setTimeframe(period)}
            style={{
              padding: '8px 16px',
              background: timeframe === period ? 'var(--primary)' : 'var(--bg-card)',
              border: `1px solid ${timeframe === period ? 'var(--primary)' : 'var(--border-subtle)'}`,
              borderRadius: '8px',
              color: timeframe === period ? 'white' : 'var(--text-secondary)',
              fontSize: '13px',
              fontWeight: '500',
              cursor: 'pointer',
              transition: 'all 0.15s ease',
              fontFamily: 'inherit'
            }}
          >
            {period === 'all' ? 'All Time' : period.toUpperCase()}
          </motion.button>
        ))}
      </motion.div>

      {/* Key Metrics */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.15 }}
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
          gap: '16px',
          marginBottom: '32px'
        }}
      >
        <MetricCard
          icon={<DollarSign size={18} />}
          label="Total Profit"
          value={`$${metrics.totalProfit.toFixed(2)}`}
          color="var(--success)"
        />
        <MetricCard
          icon={<Target size={18} />}
          label="Win Rate"
          value={`${metrics.winRate}%`}
          color="var(--primary)"
        />
        <MetricCard
          icon={<Percent size={18} />}
          label="ROI"
          value={`${metrics.roi}%`}
          color="var(--success)"
        />
        <MetricCard
          icon={<Award size={18} />}
          label="Best Streak"
          value={metrics.longestStreak}
          color="var(--warning)"
        />
      </motion.div>

      {/* Charts Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
          gap: '24px',
          marginBottom: '32px'
        }}
      >
        {/* Profit Trend */}
        <div className="section" style={{ padding: '24px' }}>
          <h3 style={{
            fontSize: '16px',
            fontWeight: '600',
            color: 'var(--text-primary)',
            margin: '0 0 20px 0',
            letterSpacing: '-0.02em'
          }}>
            Profit Trend
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={performanceData}>
              <defs>
                <linearGradient id="colorProfit" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="var(--primary)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
              <XAxis dataKey="date" tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
              <YAxis tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
              <Tooltip
                contentStyle={{
                  background: 'var(--bg-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '8px',
                  fontSize: '12px'
                }}
              />
              <Area
                type="monotone"
                dataKey="profit"
                stroke="var(--primary)"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorProfit)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Bet Category Distribution */}
        <div className="section" style={{ padding: '24px' }}>
          <h3 style={{
            fontSize: '16px',
            fontWeight: '600',
            color: 'var(--text-primary)',
            margin: '0 0 20px 0',
            letterSpacing: '-0.02em'
          }}>
            Bet Categories
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <RPieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={5}
                dataKey="value"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </RPieChart>
          </ResponsiveContainer>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', marginTop: '16px', flexWrap: 'wrap' }}>
            {categoryData.map((cat, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: cat.color }} />
                <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>{cat.name}</span>
              </div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Win/Loss Analysis */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.25 }}
        className="section"
        style={{ padding: '24px' }}
      >
        <h3 style={{
          fontSize: '16px',
          fontWeight: '600',
          color: 'var(--text-primary)',
          margin: '0 0 20px 0',
          letterSpacing: '-0.02em'
        }}>
          Weekly Win/Loss Record
        </h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={performanceData}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
            <XAxis dataKey="date" tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
            <YAxis tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
            <Tooltip
              contentStyle={{
                background: 'var(--bg-elevated)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '8px',
                fontSize: '12px'
              }}
            />
            <Legend />
            <Bar dataKey="wins" fill="var(--success)" radius={[8, 8, 0, 0]} />
            <Bar dataKey="losses" fill="var(--danger)" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>
    </div>
  );
};

const MetricCard = ({ icon, label, value, color }) => (
  <div className="metric-card">
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
      <div style={{
        color,
        background: `${color}15`,
        padding: '8px',
        borderRadius: '8px',
        display: 'flex'
      }}>
        {icon}
      </div>
      <span className="metric-label" style={{ margin: 0 }}>{label}</span>
    </div>
    <div className="metric-value" style={{ color }}>{value}</div>
  </div>
);

export default AnalyticsEnhanced;
