import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Wallet, TrendingUp, TrendingDown, DollarSign, Percent, PiggyBank, CheckCircle2, Clock } from 'lucide-react';

const Portfolio = () => {
    const [bets, setBets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [resolvingBetId, setResolvingBetId] = useState(null);
    const [resolutionOutcomes, setResolutionOutcomes] = useState({});

    useEffect(() => {
        fetchBets();
    }, []);

    const fetchBets = async () => {
        try {
            const response = await axios.get('http://localhost:8000/portfolio');
            setBets(response.data);
        } catch (error) {
            console.error("Failed to fetch bets:", error);
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
            await axios.post(`http://localhost:8000/portfolio/resolve`, {
                bet_id: betId,
                outcome: outcome
            });

            // Refresh bets after resolution
            await fetchBets();

            // Clear the resolution state for this bet
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

    // Separate pending and resolved bets
    const pendingBets = bets.filter(bet => bet.status === 'pending');
    const resolvedBets = bets.filter(bet => bet.status !== 'pending');

    // Calculate metrics based on actual bet results
    const totalWagered = bets.reduce((sum, bet) => sum + bet.wager_amount, 0);
    const wins = resolvedBets.filter(bet => bet.status === 'win').length;
    const losses = resolvedBets.filter(bet => bet.status === 'loss').length;
    const pushes = resolvedBets.filter(bet => bet.status === 'push').length;

    const calculateProfit = () => {
        return resolvedBets.reduce((total, bet) => {
            if (bet.status === 'win') {
                // Calculate profit based on odds
                const odds = bet.odds || -110;
                if (odds > 0) {
                    return total + (bet.wager_amount * (odds / 100));
                } else {
                    return total + (bet.wager_amount * (100 / Math.abs(odds)));
                }
            } else if (bet.status === 'loss') {
                return total - bet.wager_amount;
            }
            return total; // push returns wager
        }, 0);
    };

    const netProfit = calculateProfit();
    const winRate = resolvedBets.length > 0 ? ((wins / resolvedBets.length) * 100) : 0;

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
                className="grid-3"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, staggerChildren: 0.1 }}
            >
                <motion.div
                    className="metric-card"
                    whileHover={{ y: -8 }}
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
                            <DollarSign size={24} style={{ color: 'var(--info)' }} />
                        </div>
                    </div>
                    <div className="metric-label">Total Wagered</div>
                    <div className="metric-value" style={{ color: 'var(--info)' }}>
                        ${totalWagered.toFixed(2)}
                    </div>
                </motion.div>

                <motion.div
                    className="metric-card"
                    whileHover={{ y: -8 }}
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
                            <Percent size={24} style={{ color: 'var(--success)' }} />
                        </div>
                    </div>
                    <div className="metric-label">Win Rate</div>
                    <div className="metric-value" style={{ color: 'var(--success)' }}>
                        {winRate.toFixed(0)}%
                    </div>
                    <div style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
                        {wins}W - {losses}L - {pushes}P
                    </div>
                </motion.div>

                <motion.div
                    className="metric-card"
                    whileHover={{ y: -8 }}
                    style={{ textAlign: 'center' }}
                >
                    <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '16px' }}>
                        <div style={{
                            padding: '12px',
                            background: 'var(--bg-elevated)',
                            borderRadius: '50%',
                            border: `2px solid ${netProfit >= 0 ? 'var(--success)' : 'var(--danger)'}`,
                            boxShadow: netProfit >= 0 ? 'var(--glow-primary)' : '0 0 20px rgba(255, 62, 157, 0.15)'
                        }}>
                            <PiggyBank size={24} style={{ color: netProfit >= 0 ? 'var(--success)' : 'var(--danger)' }} />
                        </div>
                    </div>
                    <div className="metric-label">Net Profit</div>
                    <div className="metric-value" style={{ color: netProfit >= 0 ? 'var(--success)' : 'var(--danger)' }}>
                        {netProfit >= 0 ? '+' : ''}${netProfit.toFixed(2)}
                    </div>
                    <div style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
                        ROI: {totalWagered > 0 ? ((netProfit / totalWagered) * 100).toFixed(1) : 0}%
                    </div>
                </motion.div>
            </motion.div>

            {/* Pending Bets Section */}
            {pendingBets.length > 0 && (
                <motion.div
                    className="section"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.1 }}
                >
                    <div className="section-header">
                        <Clock className="section-icon" style={{ color: 'var(--warning)' }} size={24} />
                        <h2 className="section-title">Pending Bets</h2>
                        <div className="badge warning" style={{ marginLeft: 'auto' }}>
                            {pendingBets.length} Unresolved
                        </div>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        {pendingBets.map((bet, index) => (
                            <motion.div
                                key={bet.id || index}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.05 }}
                                className="card"
                                style={{
                                    padding: '20px',
                                    borderLeft: '3px solid var(--warning)'
                                }}
                            >
                                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                                    <div style={{ flex: 1 }}>
                                        <div style={{
                                            fontWeight: '700',
                                            color: 'var(--text-primary)',
                                            fontSize: '15px',
                                            marginBottom: '8px'
                                        }}>
                                            {bet.home_team} <span style={{ color: 'var(--text-tertiary)' }}>vs</span> {bet.away_team}
                                        </div>
                                        <div style={{
                                            fontSize: '12px',
                                            color: 'var(--text-secondary)',
                                            display: 'flex',
                                            gap: '12px',
                                            alignItems: 'center',
                                            flexWrap: 'wrap'
                                        }}>
                                            <span className="badge" style={{ padding: '4px 8px' }}>{bet.bet_type}</span>
                                            <span>Odds: {bet.odds}</span>
                                            <span style={{ color: 'var(--text-tertiary)' }}>•</span>
                                            <span>Wager: ${bet.wager_amount}</span>
                                            {bet.prediction_used && (
                                                <>
                                                    <span style={{ color: 'var(--text-tertiary)' }}>•</span>
                                                    <span>Prediction: {bet.prediction_used.toFixed(1)}</span>
                                                </>
                                            )}
                                        </div>
                                    </div>
                                </div>

                                <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                                    <select
                                        className="input-field"
                                        value={resolutionOutcomes[bet.id] || ''}
                                        onChange={(e) => handleOutcomeChange(bet.id, e.target.value)}
                                        style={{
                                            flex: 1,
                                            padding: '12px',
                                            background: 'var(--bg-elevated)',
                                            border: '1px solid var(--border-subtle)',
                                            color: 'var(--text-primary)',
                                            borderRadius: 'var(--radius-md)',
                                            fontSize: '14px'
                                        }}
                                    >
                                        <option value="">Select Outcome</option>
                                        <option value="win">Win</option>
                                        <option value="loss">Loss</option>
                                        <option value="push">Push</option>
                                    </select>

                                    <motion.button
                                        whileHover={{ scale: 1.02 }}
                                        whileTap={{ scale: 0.98 }}
                                        onClick={() => handleResolveBet(bet.id)}
                                        disabled={!resolutionOutcomes[bet.id] || resolvingBetId === bet.id}
                                        style={{
                                            padding: '12px 24px',
                                            background: resolutionOutcomes[bet.id]
                                                ? 'linear-gradient(135deg, var(--success), var(--primary))'
                                                : 'var(--bg-hover)',
                                            color: resolutionOutcomes[bet.id] ? 'var(--bg-dark)' : 'var(--text-tertiary)',
                                            border: 'none',
                                            borderRadius: 'var(--radius-md)',
                                            fontWeight: '600',
                                            fontSize: '14px',
                                            cursor: resolutionOutcomes[bet.id] ? 'pointer' : 'not-allowed',
                                            opacity: resolutionOutcomes[bet.id] ? 1 : 0.5,
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '8px',
                                            whiteSpace: 'nowrap'
                                        }}
                                    >
                                        {resolvingBetId === bet.id ? (
                                            <>
                                                <div className="loading-spinner" style={{ width: '16px', height: '16px' }} />
                                                Resolving...
                                            </>
                                        ) : (
                                            <>
                                                <CheckCircle2 size={16} />
                                                Resolve Bet
                                            </>
                                        )}
                                    </motion.button>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>
            )}

            {/* Bet History Section */}
            <motion.div
                className="section"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.2 }}
            >
                <div className="section-header">
                    <Wallet className="section-icon" style={{ color: 'var(--secondary)' }} size={24} />
                    <h2 className="section-title">Bet History</h2>
                    <div className="badge info" style={{ marginLeft: 'auto' }}>
                        Memvid Storage
                    </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    {resolvedBets.length === 0 ? (
                        <p style={{
                            color: 'var(--text-tertiary)',
                            textAlign: 'center',
                            padding: '40px 0',
                            fontSize: '14px'
                        }}>No resolved bets yet. Resolve pending bets above to see them here.</p>
                    ) : (
                        resolvedBets.map((bet, index) => {
                            const isWin = bet.status === 'win';
                            const isPush = bet.status === 'push';
                            const borderColor = isWin ? 'var(--success)' : isPush ? 'var(--warning)' : 'var(--danger)';

                            return (
                                <motion.div
                                    key={bet.id || index}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.05 }}
                                    whileHover={{ x: 4, scale: 1.01 }}
                                    className="card"
                                    style={{
                                        padding: '20px',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'space-between',
                                        borderLeft: `3px solid ${borderColor}`
                                    }}
                                >
                                    <div style={{ flex: 1 }}>
                                        <div style={{
                                            fontWeight: '700',
                                            color: 'var(--text-primary)',
                                            fontSize: '15px',
                                            marginBottom: '8px'
                                        }}>
                                            {bet.home_team} <span style={{ color: 'var(--text-tertiary)' }}>vs</span> {bet.away_team}
                                        </div>
                                        <div style={{
                                            fontSize: '12px',
                                            color: 'var(--text-secondary)',
                                            display: 'flex',
                                            gap: '12px',
                                            alignItems: 'center',
                                            flexWrap: 'wrap'
                                        }}>
                                            <span>{bet.bet_type}</span>
                                            <span style={{ color: 'var(--text-tertiary)' }}>•</span>
                                            <span>Odds: {bet.odds}</span>
                                            {bet.prediction_used && (
                                                <>
                                                    <span style={{ color: 'var(--text-tertiary)' }}>•</span>
                                                    <span>Pred: {bet.prediction_used.toFixed(1)}</span>
                                                </>
                                            )}
                                        </div>
                                    </div>
                                    <div style={{ textAlign: 'right', display: 'flex', flexDirection: 'column', gap: '8px', alignItems: 'flex-end' }}>
                                        <div style={{
                                            fontFamily: 'monospace',
                                            color: 'var(--primary)',
                                            fontSize: '18px',
                                            fontWeight: '700'
                                        }}>
                                            ${bet.wager_amount}
                                        </div>
                                        <div className={`badge ${isWin ? 'success' : isPush ? 'warning' : 'danger'}`} style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                            {isWin ? (
                                                <><TrendingUp size={12} /> Win</>
                                            ) : isPush ? (
                                                <>Push</>
                                            ) : (
                                                <><TrendingDown size={12} /> Loss</>
                                            )}
                                        </div>
                                    </div>
                                </motion.div>
                            );
                        })
                    )}
                </div>
            </motion.div>
        </div>
    );
};

export default Portfolio;
