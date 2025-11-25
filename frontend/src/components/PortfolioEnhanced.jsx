import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Wallet, TrendingUp, TrendingDown, DollarSign, Percent, Target, CheckCircle2, Clock, XCircle, MinusCircle, Calendar, BarChart3 } from 'lucide-react';
import { useSport } from '../contexts/SportContext';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const PortfolioEnhanced = () => {
  const { selectedSport } = useSport();
  const [bets, setBets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [resolvingBetId, setResolvingBetId] = useState(null);
  const [resolutionOutcomes, setResolutionOutcomes] = useState({});
  const [filterStatus, setFilterStatus] = useState('all'); // all, pending, resolved

  useEffect(() => {
    fetchBets();
  }, [selectedSport]);

  const fetchBets = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/portfolio`);
      setBets(response.data || []);
    } catch (error) {
      console.error("Failed to fetch bets:", error);
      setBets([]);
    } finally {
      setLoading(false);
    }
  };

  const handleResolveBet = async (betId) => {
    const outcome = resolutionOutcomes[betId];
    if (!outcome) {
      alert('Please select an outcome');
      return;
    }

    setResolvingBetId(betId);
    try {
      await axios.post(`${API_BASE}/portfolio/resolve`, {
        bet_id: betId,
        outcome: outcome
      });
      await fetchBets();
      setResolutionOutcomes(prev => {
        const newState = { ...prev };
        delete newState[betId];
        return newState;
      });
    } catch (error) {
      console.error('Failed to resolve bet:', error);
      alert('Failed to resolve bet. Please try again.');
    } finally {
      setResolvingBetId(null);
    }
  };

  const handleOutcomeChange = (betId, outcome) => {
    setResolutionOutcomes(prev => ({
      ...prev,
      [betId]: outcome
    }));
  };

  // Filter bets
  const pendingBets = bets.filter(bet => bet.status === 'pending');
  const resolvedBets = bets.filter(bet => bet.status !== 'pending');

  const filteredBets = filterStatus === 'all' ? bets :
    filterStatus === 'pending' ? pendingBets : resolvedBets;

  // Calculate metrics
  const totalWagered = bets.reduce((sum, bet) => sum + (bet.wager_amount || 0), 0);
  const wins = resolvedBets.filter(bet => bet.status === 'win').length;
  const losses = resolvedBets.filter(bet => bet.status === 'loss').length;
  const pushes = resolvedBets.filter(bet => bet.status === 'push').length;

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

  const profit = calculateProfit();
  const roi = totalWagered > 0 ? ((profit / totalWagered) * 100) : 0;
  const winRate = resolvedBets.length > 0 ? ((wins / resolvedBets.length) * 100) : 0;

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
          My Bets Portfolio
        </h2>
        <p style={{ fontSize: '14px', color: 'var(--text-secondary)', margin: 0 }}>
          {bets.length} total bets • {pendingBets.length} pending • {resolvedBets.length} resolved
        </p>
      </motion.div>

      {/* Metrics Dashboard */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '16px',
          marginBottom: '32px'
        }}
      >
        <MetricCard
          icon={<DollarSign size={20} />}
          label="Total Wagered"
          value={`$${totalWagered.toFixed(2)}`}
          color="var(--primary)"
        />
        <MetricCard
          icon={profit >= 0 ? <TrendingUp size={20} /> : <TrendingDown size={20} />}
          label="Net Profit/Loss"
          value={`${profit >= 0 ? '+' : ''}$${profit.toFixed(2)}`}
          color={profit >= 0 ? 'var(--success)' : 'var(--danger)'}
        />
        <MetricCard
          icon={<Percent size={20} />}
          label="ROI"
          value={`${roi >= 0 ? '+' : ''}${roi.toFixed(1)}%`}
          color={roi >= 0 ? 'var(--success)' : 'var(--danger)'}
        />
        <MetricCard
          icon={<Target size={20} />}
          label="Win Rate"
          value={`${winRate.toFixed(1)}%`}
          color="var(--primary)"
        />
      </motion.div>

      {/* Record Stats */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.15 }}
        className="section"
        style={{ marginBottom: '24px', padding: '20px 24px' }}
      >
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '24px',
          flexWrap: 'wrap'
        }}>
          <RecordStat icon={<CheckCircle2 size={18} />} label="Wins" value={wins} color="var(--success)" />
          <RecordStat icon={<XCircle size={18} />} label="Losses" value={losses} color="var(--danger)" />
          <RecordStat icon={<MinusCircle size={18} />} label="Pushes" value={pushes} color="var(--warning)" />
          <RecordStat icon={<Clock size={18} />} label="Pending" value={pendingBets.length} color="var(--info)" />
        </div>
      </motion.div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        style={{
          display: 'flex',
          gap: '8px',
          marginBottom: '20px',
          flexWrap: 'wrap'
        }}
      >
        <FilterButton active={filterStatus === 'all'} onClick={() => setFilterStatus('all')}>
          All Bets ({bets.length})
        </FilterButton>
        <FilterButton active={filterStatus === 'pending'} onClick={() => setFilterStatus('pending')}>
          Pending ({pendingBets.length})
        </FilterButton>
        <FilterButton active={filterStatus === 'resolved'} onClick={() => setFilterStatus('resolved')}>
          Resolved ({resolvedBets.length})
        </FilterButton>
      </motion.div>

      {/* Bets List */}
      {loading ? (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '400px'
        }}>
          <div className="loading-spinner"></div>
        </div>
      ) : filteredBets.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="section"
          style={{
            textAlign: 'center',
            padding: '80px 20px'
          }}
        >
          <Wallet size={48} style={{ color: 'var(--text-tertiary)', marginBottom: '16px' }} />
          <p style={{ color: 'var(--text-secondary)', margin: 0, fontSize: '16px', fontWeight: '500' }}>
            No bets found
          </p>
          <p style={{ color: 'var(--text-tertiary)', margin: '8px 0 0 0', fontSize: '14px' }}>
            Place your first bet from the Dashboard
          </p>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.25 }}
          style={{ display: 'grid', gap: '16px' }}
        >
          {filteredBets.map((bet, index) => (
            <BetCard
              key={bet.bet_id || index}
              bet={bet}
              index={index}
              resolvingBetId={resolvingBetId}
              resolutionOutcomes={resolutionOutcomes}
              onOutcomeChange={handleOutcomeChange}
              onResolve={handleResolveBet}
            />
          ))}
        </motion.div>
      )}
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

const RecordStat = ({ icon, label, value, color }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
    <div style={{ color, display: 'flex' }}>{icon}</div>
    <div>
      <div style={{ fontSize: '20px', fontWeight: '700', color, lineHeight: 1 }}>{value}</div>
      <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>{label}</div>
    </div>
  </div>
);

const FilterButton = ({ children, active, onClick }) => (
  <motion.button
    whileHover={{ scale: 1.02 }}
    whileTap={{ scale: 0.98 }}
    onClick={onClick}
    style={{
      padding: '10px 18px',
      background: active ? 'var(--primary)' : 'var(--bg-card)',
      border: `1px solid ${active ? 'var(--primary)' : 'var(--border-subtle)'}`,
      borderRadius: '8px',
      color: active ? 'white' : 'var(--text-secondary)',
      fontSize: '13px',
      fontWeight: '500',
      cursor: 'pointer',
      transition: 'all 0.15s ease',
      fontFamily: 'inherit'
    }}
  >
    {children}
  </motion.button>
);

const BetCard = ({ bet, index, resolvingBetId, resolutionOutcomes, onOutcomeChange, onResolve }) => {
  const isPending = bet.status === 'pending';
  const statusConfig = {
    win: { color: 'var(--success)', icon: <CheckCircle2 size={16} />, label: 'WON' },
    loss: { color: 'var(--danger)', icon: <XCircle size={16} />, label: 'LOST' },
    push: { color: 'var(--warning)', icon: <MinusCircle size={16} />, label: 'PUSH' },
    pending: { color: 'var(--info)', icon: <Clock size={16} />, label: 'PENDING' }
  };

  const config = statusConfig[bet.status] || statusConfig.pending;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.03 }}
      className="section"
      style={{
        padding: '20px',
        borderLeft: `4px solid ${config.color}`
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '20px', flexWrap: 'wrap' }}>
        {/* Bet Details */}
        <div style={{ flex: 1, minWidth: '200px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <div className="badge" style={{ background: `${config.color}15`, color: config.color, border: 'none' }}>
              {config.icon}
              <span style={{ marginLeft: '6px' }}>{config.label}</span>
            </div>
            {bet.placed_at && (
              <span style={{ fontSize: '12px', color: 'var(--text-tertiary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Calendar size={12} />
                {new Date(bet.placed_at).toLocaleDateString()}
              </span>
            )}
          </div>

          <h3 style={{
            fontSize: '16px',
            fontWeight: '600',
            color: 'var(--text-primary)',
            margin: '0 0 8px 0',
            letterSpacing: '-0.02em'
          }}>
            {bet.game_description || 'Game Bet'}
          </h3>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', marginTop: '12px' }}>
            <BetDetail label="Wager" value={`$${(bet.wager_amount || 0).toFixed(2)}`} />
            <BetDetail label="Odds" value={bet.odds || '-110'} />
            {bet.predicted_margin && <BetDetail label="Margin" value={`${bet.predicted_margin > 0 ? '+' : ''}${bet.predicted_margin.toFixed(1)}`} />}
          </div>
        </div>

        {/* Resolution Controls (for pending) or Result (for resolved) */}
        {isPending ? (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '10px',
            minWidth: '200px'
          }}>
            <select
              value={resolutionOutcomes[bet.bet_id] || ''}
              onChange={(e) => onOutcomeChange(bet.bet_id, e.target.value)}
              className="input-field"
              style={{ fontSize: '13px' }}
            >
              <option value="">Select outcome...</option>
              <option value="win">Win</option>
              <option value="loss">Loss</option>
              <option value="push">Push</option>
            </select>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => onResolve(bet.bet_id)}
              disabled={resolvingBetId === bet.bet_id || !resolutionOutcomes[bet.bet_id]}
              style={{
                padding: '10px 16px',
                background: resolutionOutcomes[bet.bet_id] ? 'var(--primary)' : 'var(--bg-elevated)',
                border: 'none',
                borderRadius: '8px',
                color: resolutionOutcomes[bet.bet_id] ? 'white' : 'var(--text-tertiary)',
                fontSize: '13px',
                fontWeight: '600',
                cursor: resolutionOutcomes[bet.bet_id] ? 'pointer' : 'not-allowed',
                transition: 'all 0.15s ease',
                fontFamily: 'inherit',
                opacity: resolutionOutcomes[bet.bet_id] ? 1 : 0.5
              }}
            >
              {resolvingBetId === bet.bet_id ? 'Resolving...' : 'Resolve Bet'}
            </motion.button>
          </div>
        ) : bet.payout && (
          <div style={{ textAlign: 'right', minWidth: '120px' }}>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
              Payout
            </div>
            <div style={{
              fontSize: '24px',
              fontWeight: '700',
              color: config.color,
              letterSpacing: '-0.02em'
            }}>
              ${bet.payout.toFixed(2)}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
};

const BetDetail = ({ label, value }) => (
  <div>
    <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', marginBottom: '4px', textTransform: 'uppercase', fontWeight: '600', letterSpacing: '0.5px' }}>
      {label}
    </div>
    <div style={{ fontSize: '14px', color: 'var(--text-primary)', fontWeight: '600' }}>
      {value}
    </div>
  </div>
);

export default PortfolioEnhanced;
