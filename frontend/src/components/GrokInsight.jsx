import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, Sparkles } from 'lucide-react';

const GrokInsight = ({ insight, prediction }) => {
    if (!insight) return null;

    const isPositive = prediction > 0;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.3 }}
                className="card"
                style={{
                    padding: '28px',
                    borderLeft: '4px solid var(--secondary)',
                    position: 'relative'
                }}
            >
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '20px' }}>
                    <motion.div
                        whileHover={{ rotate: 10 }}
                        transition={{ type: 'spring', stiffness: 300 }}
                        style={{
                            padding: '16px',
                            background: 'var(--bg-elevated)',
                            borderRadius: '50%',
                            border: '2px solid var(--secondary)',
                            boxShadow: 'var(--glow-secondary)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}
                    >
                        <Bot style={{ color: 'var(--secondary)' }} size={32} />
                    </motion.div>

                    <div style={{ flex: 1 }}>
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            marginBottom: '16px'
                        }}>
                            <h3 style={{
                                fontSize: '18px',
                                fontWeight: '700',
                                margin: 0,
                                color: 'var(--secondary)'
                            }}>KC DaCRE8TOR's Take</h3>
                            <Sparkles size={18} style={{ color: 'var(--warning)' }} />
                        </div>

                        <p style={{
                            color: 'var(--text-primary)',
                            fontSize: '16px',
                            lineHeight: '1.7',
                            fontStyle: 'italic',
                            margin: '0 0 20px 0'
                        }}>
                            "{insight}"
                        </p>

                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '12px',
                            marginTop: '20px'
                        }}>
                            <span style={{
                                fontSize: '11px',
                                textTransform: 'uppercase',
                                letterSpacing: '1.5px',
                                color: 'var(--text-secondary)',
                                fontWeight: '600',
                                whiteSpace: 'nowrap'
                            }}>Confidence Level:</span>
                            <div style={{
                                height: '8px',
                                flex: 1,
                                background: 'var(--bg-elevated)',
                                borderRadius: 'var(--radius-sm)',
                                overflow: 'hidden',
                                border: '1px solid var(--border-subtle)'
                            }}>
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: `${Math.min(Math.abs(prediction) * 10 + 50, 95)}%` }}
                                    transition={{ duration: 0.8, ease: 'easeOut' }}
                                    style={{
                                        height: '100%',
                                        background: isPositive ? 'var(--success)' : 'var(--danger)',
                                        borderRadius: 'var(--radius-sm)'
                                    }}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </motion.div>
        </AnimatePresence>
    );
};

export default GrokInsight;
