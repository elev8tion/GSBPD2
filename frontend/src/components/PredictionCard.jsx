import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Brain, Trophy, Home } from 'lucide-react';

const PredictionCard = ({ onPredict, isLoading }) => {
    const [teamStrength, setTeamStrength] = useState(85);
    const [opponentStrength, setOpponentStrength] = useState(80);
    const [homeAdvantage, setHomeAdvantage] = useState(true);

    const handleSubmit = () => {
        onPredict({
            team_strength: teamStrength,
            opponent_strength: opponentStrength,
            home_advantage: homeAdvantage ? 1 : 0
        });
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="card"
            style={{ width: '100%', padding: '32px' }}
        >
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '32px',
                paddingBottom: '16px',
                borderBottom: '1px solid var(--border-subtle)'
            }}>
                <Brain style={{ color: 'var(--secondary)' }} size={24} />
                <h2 style={{
                    fontSize: '20px',
                    fontWeight: '600',
                    margin: 0,
                    color: 'var(--text-primary)'
                }}>Game Parameters</h2>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
                <div>
                    <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        marginBottom: '12px',
                        alignItems: 'center'
                    }}>
                        <label style={{
                            fontSize: '14px',
                            color: 'var(--text-secondary)',
                            fontWeight: '500'
                        }}>Team Strength</label>
                        <span style={{
                            color: 'var(--secondary)',
                            fontFamily: 'monospace',
                            fontSize: '16px',
                            fontWeight: '700',
                            background: 'var(--bg-elevated)',
                            padding: '4px 12px',
                            borderRadius: 'var(--radius-sm)',
                            border: '1px solid var(--border-subtle)'
                        }}>{teamStrength}</span>
                    </div>
                    <input
                        type="range"
                        min="0"
                        max="100"
                        value={teamStrength}
                        onChange={(e) => setTeamStrength(Number(e.target.value))}
                        style={{ width: '100%' }}
                    />
                </div>

                <div>
                    <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        marginBottom: '12px',
                        alignItems: 'center'
                    }}>
                        <label style={{
                            fontSize: '14px',
                            color: 'var(--text-secondary)',
                            fontWeight: '500'
                        }}>Opponent Strength</label>
                        <span style={{
                            color: 'var(--primary)',
                            fontFamily: 'monospace',
                            fontSize: '16px',
                            fontWeight: '700',
                            background: 'var(--bg-elevated)',
                            padding: '4px 12px',
                            borderRadius: 'var(--radius-sm)',
                            border: '1px solid var(--border-subtle)'
                        }}>{opponentStrength}</span>
                    </div>
                    <input
                        type="range"
                        min="0"
                        max="100"
                        value={opponentStrength}
                        onChange={(e) => setOpponentStrength(Number(e.target.value))}
                        style={{ width: '100%' }}
                    />
                </div>

                <motion.div
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        padding: '16px',
                        background: 'var(--bg-elevated)',
                        borderRadius: 'var(--radius-md)',
                        border: '1px solid var(--border-subtle)',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease'
                    }}
                    onClick={() => setHomeAdvantage(!homeAdvantage)}
                >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <Home
                            style={{ color: homeAdvantage ? 'var(--success)' : 'var(--text-tertiary)' }}
                            size={20}
                        />
                        <span style={{
                            fontSize: '14px',
                            fontWeight: '500',
                            color: 'var(--text-primary)'
                        }}>Home Advantage</span>
                    </div>
                    <div className={`toggle-switch ${homeAdvantage ? 'active' : ''}`}>
                        <div className="toggle-knob" />
                    </div>
                </motion.div>

                <motion.button
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={handleSubmit}
                    disabled={isLoading}
                    className="btn btn-primary"
                    style={{
                        width: '100%',
                        padding: '16px',
                        fontSize: '16px',
                        opacity: isLoading ? 0.5 : 1,
                        cursor: isLoading ? 'not-allowed' : 'pointer'
                    }}
                >
                    {isLoading ? 'Crunching Numbers...' : 'Predict Outcome'}
                </motion.button>
            </div>
        </motion.div>
    );
};

export default PredictionCard;
