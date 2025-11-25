import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Wallet, TrendingUp, TrendingDown, DollarSign, Percent, PiggyBank } from 'lucide-react';

const Portfolio = () => {
    const [bets, setBets] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
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

        fetchBets();
    }, []);

    const totalWagered = bets.reduce((sum, bet) => sum + bet.wager_amount, 0);
    // Mocking outcome for demo since we don't have real result tracking yet
    const wins = bets.filter((_, i) => i % 2 === 0).length;
    const losses = bets.length - wins;

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
                        {bets.length > 0 ? ((wins / bets.length) * 100).toFixed(0) : 0}%
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
                            border: '2px solid var(--secondary)',
                            boxShadow: 'var(--glow-secondary)'
                        }}>
                            <PiggyBank size={24} style={{ color: 'var(--secondary)' }} />
                        </div>
                    </div>
                    <div className="metric-label">Net Profit</div>
                    <div className="metric-value" style={{ color: 'var(--secondary)' }}>
                        ${(wins * 50 - losses * 50).toFixed(2)}
                    </div>
                    <div style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>(Estimated)</div>
                </motion.div>
            </motion.div>

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
                    {bets.length === 0 ? (
                        <p style={{
                            color: 'var(--text-tertiary)',
                            textAlign: 'center',
                            padding: '40px 0',
                            fontSize: '14px'
                        }}>No bets recorded yet.</p>
                    ) : (
                        bets.map((bet, index) => {
                            const isWin = index % 2 === 0;
                            return (
                                <motion.div
                                    key={index}
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
                                        borderLeft: `3px solid ${isWin ? 'var(--success)' : 'var(--danger)'}`
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
                                            alignItems: 'center'
                                        }}>
                                            <span>{bet.bet_type}</span>
                                            <span style={{ color: 'var(--text-tertiary)' }}>•</span>
                                            <span>Odds: {bet.odds}</span>
                                            <span style={{ color: 'var(--text-tertiary)' }}>•</span>
                                            <span>Pred: {bet.prediction_used.toFixed(1)}</span>
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
                                        <div className={`badge ${isWin ? 'success' : 'danger'}`} style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                            {isWin ? (
                                                <><TrendingUp size={12} /> Win</>
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
