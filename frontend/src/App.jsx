import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, Zap, Wallet, LayoutDashboard, GitMerge, Database, Settings as SettingsIcon, TrendingUp } from 'lucide-react';
import PredictionCard from './components/PredictionCard';
import GrokInsight from './components/GrokInsight';
import StatsChart from './components/StatsChart';
import GameSelector from './components/GameSelector';
import ExplainabilityChart from './components/ExplainabilityChart';
import Portfolio from './components/Portfolio';
import Pipeline from './components/Pipeline';
import MemorySearch from './components/MemorySearch';
import BetPlacementModal from './components/BetPlacementModal';
import Settings from './components/Settings';
import Analytics from './components/Analytics';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard'); // 'dashboard', 'portfolio', 'pipeline'
  const [prediction, setPrediction] = useState(null);
  const [insight, setInsight] = useState(null);
  const [shapValues, setShapValues] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [lastInput, setLastInput] = useState(null);
  const [isBetModalOpen, setIsBetModalOpen] = useState(false);
  const [betSuccess, setBetSuccess] = useState(false);

  const handlePredict = async (data) => {
    setIsLoading(true);
    setLastInput(data);
    try {
      const response = await axios.post(`${API_URL}/predict`, data);
      setPrediction(response.data.predicted_spread_margin);
      setInsight(response.data.grok_insight);
      setShapValues(response.data.shap_values);
    } catch (error) {
      console.error("Prediction failed:", error);
      setInsight("My circuits are fried. The backend seems to be taking a nap.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectGame = (gameData) => {
    // Pre-fill the prediction card (logic handled by passing props or context,
    // but for now we'll just trigger a prediction or update state if we refactor PredictionCard)
    // For this demo, we'll auto-predict
    handlePredict(gameData);
  };

  const handleBetModalClose = (success) => {
    setIsBetModalOpen(false);
    if (success) {
      setBetSuccess(true);
      setTimeout(() => setBetSuccess(false), 3000);
    }
  };

  return (
    <div className="app-container">
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        style={{ marginBottom: '32px' }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <motion.div
              whileHover={{ scale: 1.05, rotate: 5 }}
              whileTap={{ scale: 0.95 }}
              style={{
                padding: '16px',
                background: 'var(--primary)',
                borderRadius: 'var(--radius-lg)',
                boxShadow: 'var(--glow-primary), var(--shadow-md)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <Activity size={32} style={{ color: 'var(--bg-dark)' }} />
            </motion.div>
            <div>
              <h1 style={{
                fontSize: '32px',
                fontWeight: '700',
                margin: '0',
                color: 'var(--text-primary)',
                letterSpacing: '-0.5px'
              }}>
                <span style={{ color: 'var(--primary)' }}>KC DaCRE8TOR</span> Prediction Dashboard
              </h1>
              <p style={{
                color: 'var(--text-secondary)',
                fontSize: '14px',
                margin: '4px 0 0 0'
              }}>AI-Powered Sports Betting Intelligence</p>
            </div>
          </div>

          <nav className="tab-navigation">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setActiveTab('dashboard')}
              className={`tab-button ${activeTab === 'dashboard' ? 'active' : ''}`}
            >
              <LayoutDashboard size={20} />
              <span>Dashboard</span>
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setActiveTab('pipeline')}
              className={`tab-button ${activeTab === 'pipeline' ? 'active' : ''}`}
            >
              <GitMerge size={20} />
              <span>Pipeline</span>
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setActiveTab('knowledge')}
              className={`tab-button ${activeTab === 'knowledge' ? 'active' : ''}`}
            >
              <Database size={20} />
              <span>Knowledge Base</span>
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setActiveTab('portfolio')}
              className={`tab-button ${activeTab === 'portfolio' ? 'active' : ''}`}
            >
              <Wallet size={20} />
              <span>My Bets</span>
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setActiveTab('analytics')}
              className={`tab-button ${activeTab === 'analytics' ? 'active' : ''}`}
            >
              <TrendingUp size={20} />
              <span>Analytics</span>
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setActiveTab('settings')}
              className={`tab-button ${activeTab === 'settings' ? 'active' : ''}`}
            >
              <SettingsIcon size={20} />
              <span>Settings</span>
            </motion.button>
          </nav>
        </div>
      </motion.header>

        <AnimatePresence mode="wait">
          {activeTab === 'dashboard' && (
            <motion.main
              key="dashboard"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="grid-2"
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <section>
                  <GameSelector onSelectGame={handleSelectGame} />

                  <div className="section-header" style={{ marginTop: '32px' }}>
                    <Zap className="section-icon" style={{ color: 'var(--warning)' }} size={24} />
                    <h2 className="section-title">Custom Parameters</h2>
                  </div>
                  <PredictionCard onPredict={handlePredict} isLoading={isLoading} />
                </section>

                {lastInput && (
                  <motion.section
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.3 }}
                  >
                    <StatsChart data={lastInput} />
                  </motion.section>
                )}
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <section>
                  <div className="section-header">
                    <Activity className="section-icon" size={24} />
                    <h2 className="section-title">Live Analysis</h2>
                  </div>

                  {prediction !== null ? (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ duration: 0.3 }}
                      style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}
                    >
                      <div className="card-elevated" style={{
                        padding: '40px',
                        textAlign: 'center',
                        position: 'relative',
                        overflow: 'hidden'
                      }}>
                        <div style={{
                          position: 'absolute',
                          top: 0,
                          left: 0,
                          right: 0,
                          height: '3px',
                          background: 'var(--primary)'
                        }} />
                        <h3 style={{
                          color: 'var(--text-secondary)',
                          textTransform: 'uppercase',
                          letterSpacing: '2px',
                          fontSize: '12px',
                          fontWeight: '600',
                          marginBottom: '16px'
                        }}>Predicted Spread Margin</h3>
                        <div style={{
                          fontSize: '64px',
                          fontWeight: '900',
                          color: 'var(--text-primary)',
                          marginBottom: '16px',
                          letterSpacing: '-2px'
                        }}>
                          {prediction > 0 ? '+' : ''}{prediction.toFixed(1)}
                        </div>
                        <div className={`badge ${prediction > 0 ? 'success' : 'danger'}`}>
                          {prediction > 0 ? 'FAVORABLE' : 'UNFAVORABLE'}
                        </div>
                      </div>

                      <GrokInsight insight={insight} prediction={prediction} />

                      <ExplainabilityChart shapValues={shapValues} />

                      <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => setIsBetModalOpen(true)}
                        style={{
                          width: '100%',
                          padding: '16px 24px',
                          fontSize: '16px',
                          fontWeight: '700',
                          borderRadius: 'var(--radius-md)',
                          border: 'none',
                          background: 'linear-gradient(135deg, var(--success), var(--primary))',
                          color: 'var(--bg-dark)',
                          cursor: 'pointer',
                          boxShadow: 'var(--shadow-md)',
                          textTransform: 'uppercase',
                          letterSpacing: '1px'
                        }}
                      >
                        Place Bet on This Prediction
                      </motion.button>

                      {betSuccess && (
                        <motion.div
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0 }}
                          style={{
                            padding: '12px 16px',
                            background: 'rgba(0, 255, 136, 0.1)',
                            border: '1px solid var(--success)',
                            borderRadius: 'var(--radius-md)',
                            color: 'var(--success)',
                            textAlign: 'center',
                            fontSize: '14px',
                            fontWeight: '600'
                          }}
                        >
                          ✓ Bet placed successfully! Check the My Bets tab.
                        </motion.div>
                      )}
                    </motion.div>
                  ) : (
                    <div className="card" style={{
                      padding: '60px',
                      textAlign: 'center',
                      border: '2px dashed var(--border-subtle)'
                    }}>
                      <p style={{ color: 'var(--text-tertiary)', margin: 0 }}>
                        Waiting for input data...
                        <br />
                        <span style={{ fontSize: '12px', opacity: '0.7' }}>Select a game or configure parameters</span>
                      </p>
                    </div>
                  )}
                </section>
              </div>
            </motion.main>
          )}

          {activeTab === 'pipeline' && (
            <motion.div
              key="pipeline"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Pipeline />
            </motion.div>
          )}

          {activeTab === 'knowledge' && (
            <motion.div
              key="knowledge"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <MemorySearch />
            </motion.div>
          )}

          {activeTab === 'portfolio' && (
            <motion.div
              key="portfolio"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Portfolio />
            </motion.div>
          )}

          {activeTab === 'analytics' && (
            <motion.div
              key="analytics"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Analytics />
            </motion.div>
          )}

          {activeTab === 'settings' && (
            <motion.div
              key="settings"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <Settings />
            </motion.div>
          )}
        </AnimatePresence>

        <BetPlacementModal
          isOpen={isBetModalOpen}
          onClose={handleBetModalClose}
          prediction={prediction}
          gameData={lastInput}
        />
    </div>
  );
}

export default App;
