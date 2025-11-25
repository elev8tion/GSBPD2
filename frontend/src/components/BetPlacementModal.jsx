import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, DollarSign, TrendingUp, AlertCircle } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

const BetPlacementModal = ({ isOpen, onClose, prediction, gameData }) => {
  const [betType, setBetType] = useState('spread');
  const [wagerAmount, setWagerAmount] = useState('');
  const [odds, setOdds] = useState(-110);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const betTypes = [
    { value: 'spread', label: 'Spread', icon: TrendingUp },
    { value: 'moneyline', label: 'Moneyline', icon: DollarSign },
    { value: 'over_under', label: 'Over/Under', icon: TrendingUp },
    { value: 'sgp', label: 'Same Game Parlay', icon: TrendingUp }
  ];

  const calculatePayout = () => {
    const wager = parseFloat(wagerAmount) || 0;
    if (odds > 0) {
      return wager + (wager * (odds / 100));
    } else {
      return wager + (wager * (100 / Math.abs(odds)));
    }
  };

  const calculateProfit = () => {
    return calculatePayout() - (parseFloat(wagerAmount) || 0);
  };

  const getConfidenceLevel = () => {
    if (!prediction) return 0;
    const absPrediction = Math.abs(prediction);
    if (absPrediction >= 10) return 90;
    if (absPrediction >= 7) return 75;
    if (absPrediction >= 5) return 60;
    if (absPrediction >= 3) return 50;
    return 40;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!wagerAmount || parseFloat(wagerAmount) <= 0) {
      setError('Please enter a valid wager amount');
      return;
    }

    if (parseFloat(wagerAmount) > 10000) {
      setError('Maximum wager is $10,000');
      return;
    }

    setIsSubmitting(true);

    try {
      await axios.post(`${API_URL}/portfolio/bet`, {
        bet_type: betType,
        wager_amount: parseFloat(wagerAmount),
        odds: odds,
        game_data: gameData || {},
        prediction_used: prediction,
        status: 'pending'
      });

      onClose(true); // true indicates success
    } catch (err) {
      console.error('Failed to place bet:', err);
      setError(err.response?.data?.detail || 'Failed to place bet. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const confidence = getConfidenceLevel();

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            backdropFilter: 'blur(8px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            padding: '20px'
          }}
        >
          <motion.div
            initial={{ scale: 0.9, y: 20 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.9, y: 20 }}
            onClick={(e) => e.stopPropagation()}
            className="card-elevated"
            style={{
              maxWidth: '600px',
              width: '100%',
              maxHeight: '90vh',
              overflow: 'auto',
              position: 'relative'
            }}
          >
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              height: '4px',
              background: 'linear-gradient(90deg, var(--primary), var(--secondary), var(--accent))'
            }} />

            <div style={{
              padding: '32px',
              display: 'flex',
              flexDirection: 'column',
              gap: '24px'
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <h2 style={{
                  fontSize: '24px',
                  fontWeight: '700',
                  color: 'var(--text-primary)',
                  margin: 0
                }}>Place Bet</h2>
                <motion.button
                  whileHover={{ scale: 1.1, rotate: 90 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={onClose}
                  style={{
                    background: 'var(--bg-hover)',
                    border: 'none',
                    borderRadius: 'var(--radius-md)',
                    padding: '8px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}
                >
                  <X size={20} style={{ color: 'var(--text-secondary)' }} />
                </motion.button>
              </div>

              {prediction !== null && (
                <div className="card" style={{
                  background: 'linear-gradient(135deg, rgba(0, 217, 255, 0.1), rgba(168, 85, 247, 0.1))',
                  border: '1px solid rgba(0, 217, 255, 0.3)',
                  padding: '20px'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <p style={{
                        color: 'var(--text-secondary)',
                        fontSize: '12px',
                        textTransform: 'uppercase',
                        letterSpacing: '1px',
                        marginBottom: '8px'
                      }}>Predicted Margin</p>
                      <p style={{
                        fontSize: '32px',
                        fontWeight: '900',
                        color: 'var(--primary)',
                        margin: 0
                      }}>
                        {prediction > 0 ? '+' : ''}{prediction.toFixed(1)}
                      </p>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <p style={{
                        color: 'var(--text-secondary)',
                        fontSize: '12px',
                        textTransform: 'uppercase',
                        letterSpacing: '1px',
                        marginBottom: '8px'
                      }}>Confidence</p>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px'
                      }}>
                        <div style={{
                          width: '80px',
                          height: '8px',
                          background: 'var(--bg-dark)',
                          borderRadius: '4px',
                          overflow: 'hidden'
                        }}>
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${confidence}%` }}
                            transition={{ duration: 0.5 }}
                            style={{
                              height: '100%',
                              background: confidence >= 70 ? 'var(--success)' : confidence >= 50 ? 'var(--warning)' : 'var(--danger)'
                            }}
                          />
                        </div>
                        <span style={{
                          fontSize: '16px',
                          fontWeight: '700',
                          color: confidence >= 70 ? 'var(--success)' : confidence >= 50 ? 'var(--warning)' : 'var(--danger)'
                        }}>{confidence}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <div className="input-group">
                  <label className="input-label">Bet Type</label>
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(2, 1fr)',
                    gap: '12px'
                  }}>
                    {betTypes.map((type) => {
                      const Icon = type.icon;
                      return (
                        <motion.button
                          key={type.value}
                          type="button"
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          onClick={() => setBetType(type.value)}
                          className="card"
                          style={{
                            padding: '16px',
                            cursor: 'pointer',
                            border: betType === type.value
                              ? '2px solid var(--primary)'
                              : '2px solid transparent',
                            background: betType === type.value
                              ? 'rgba(0, 217, 255, 0.1)'
                              : 'var(--bg-card)',
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            gap: '8px',
                            transition: 'all 0.2s'
                          }}
                        >
                          <Icon size={24} style={{ color: betType === type.value ? 'var(--primary)' : 'var(--text-secondary)' }} />
                          <span style={{
                            fontSize: '14px',
                            fontWeight: '600',
                            color: betType === type.value ? 'var(--primary)' : 'var(--text-secondary)'
                          }}>{type.label}</span>
                        </motion.button>
                      );
                    })}
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                  <div className="input-group">
                    <label className="input-label">Wager Amount</label>
                    <div style={{ position: 'relative' }}>
                      <DollarSign
                        size={20}
                        style={{
                          position: 'absolute',
                          left: '12px',
                          top: '50%',
                          transform: 'translateY(-50%)',
                          color: 'var(--text-secondary)'
                        }}
                      />
                      <input
                        type="number"
                        className="input-field"
                        value={wagerAmount}
                        onChange={(e) => setWagerAmount(e.target.value)}
                        placeholder="0.00"
                        step="0.01"
                        min="0"
                        max="10000"
                        style={{ paddingLeft: '40px' }}
                      />
                    </div>
                  </div>

                  <div className="input-group">
                    <label className="input-label">Odds (American)</label>
                    <input
                      type="number"
                      className="input-field"
                      value={odds}
                      onChange={(e) => setOdds(parseInt(e.target.value))}
                      placeholder="-110"
                    />
                  </div>
                </div>

                {wagerAmount && parseFloat(wagerAmount) > 0 && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="card"
                    style={{
                      background: 'var(--bg-elevated)',
                      padding: '20px'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                      <span style={{ color: 'var(--text-secondary)' }}>To Win:</span>
                      <span style={{ color: 'var(--success)', fontWeight: '700', fontSize: '18px' }}>
                        ${calculateProfit().toFixed(2)}
                      </span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-secondary)' }}>Total Payout:</span>
                      <span style={{ color: 'var(--text-primary)', fontWeight: '700', fontSize: '18px' }}>
                        ${calculatePayout().toFixed(2)}
                      </span>
                    </div>
                  </motion.div>
                )}

                {error && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                      padding: '12px 16px',
                      background: 'rgba(255, 62, 157, 0.1)',
                      border: '1px solid var(--danger)',
                      borderRadius: 'var(--radius-md)',
                      color: 'var(--danger)'
                    }}
                  >
                    <AlertCircle size={20} />
                    <span style={{ fontSize: '14px' }}>{error}</span>
                  </motion.div>
                )}

                <div style={{ display: 'flex', gap: '12px', marginTop: '8px' }}>
                  <motion.button
                    type="button"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={onClose}
                    className="btn-secondary"
                    style={{
                      flex: 1,
                      padding: '16px',
                      fontSize: '16px',
                      fontWeight: '600',
                      borderRadius: 'var(--radius-md)',
                      border: '2px solid var(--border-subtle)',
                      background: 'transparent',
                      color: 'var(--text-secondary)',
                      cursor: 'pointer'
                    }}
                  >
                    Cancel
                  </motion.button>
                  <motion.button
                    type="submit"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    disabled={isSubmitting || !wagerAmount || parseFloat(wagerAmount) <= 0}
                    style={{
                      flex: 1,
                      padding: '16px',
                      fontSize: '16px',
                      fontWeight: '600',
                      borderRadius: 'var(--radius-md)',
                      border: 'none',
                      background: isSubmitting || !wagerAmount || parseFloat(wagerAmount) <= 0
                        ? 'var(--bg-hover)'
                        : 'linear-gradient(135deg, var(--primary), var(--secondary))',
                      color: 'var(--text-primary)',
                      cursor: isSubmitting || !wagerAmount || parseFloat(wagerAmount) <= 0 ? 'not-allowed' : 'pointer',
                      opacity: isSubmitting || !wagerAmount || parseFloat(wagerAmount) <= 0 ? 0.5 : 1
                    }}
                  >
                    {isSubmitting ? 'Placing Bet...' : 'Place Bet'}
                  </motion.button>
                </div>
              </form>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default BetPlacementModal;
