import React, { useState } from 'react';
import { Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Activity, Zap, Wallet, LayoutDashboard, GitMerge, Database, Settings as SettingsIcon, TrendingUp, MessageSquare, Users, UserCircle, Calendar } from 'lucide-react';
import { useSport } from './contexts/SportContext';
import PredictionCard from './components/PredictionCard';
import GrokInsight from './components/GrokInsight';
import StatsChart from './components/StatsChart';
import GameSelector from './components/GameSelector';
import ExplainabilityChart from './components/ExplainabilityChart';
import PortfolioEnhanced from './components/PortfolioEnhanced';
import PipelineEnhanced from './components/PipelineEnhanced';
import MemorySearchEnhanced from './components/MemorySearchEnhanced';
import ChatEnhanced from './components/ChatEnhanced';
import BetPlacementModal from './components/BetPlacementModal';
import SettingsEnhanced from './components/SettingsEnhanced';
import AnalyticsEnhanced from './components/AnalyticsEnhanced';
import TeamsEnhanced from './components/TeamsEnhanced';
import TeamDetail from './components/TeamDetail';
import PlayersEnhanced from './components/PlayersEnhanced';
import Schedule from './components/Schedule';
import Matchup from './components/Matchup';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
  const location = useLocation();
  const navigate = useNavigate();
  const { selectedSport, setSelectedSport } = useSport();
  const [prediction, setPrediction] = useState(null);
  const [insight, setInsight] = useState(null);
  const [shapValues, setShapValues] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [lastInput, setLastInput] = useState(null);
  const [isBetModalOpen, setIsBetModalOpen] = useState(false);
  const [betSuccess, setBetSuccess] = useState(false);

  // Determine active tab from location
  const getActiveTab = () => {
    const path = location.pathname;
    if (path === '/' || path === '/dashboard') return 'dashboard';
    if (path.startsWith('/teams')) return 'teams';
    if (path.startsWith('/players')) return 'players';
    if (path.startsWith('/schedule') || path.startsWith('/matchup')) return 'schedule';
    if (path.startsWith('/portfolio')) return 'portfolio';
    if (path.startsWith('/pipeline')) return 'pipeline';
    if (path.startsWith('/knowledge')) return 'knowledge';
    if (path.startsWith('/analytics')) return 'analytics';
    if (path.startsWith('/chat')) return 'chat';
    if (path.startsWith('/settings')) return 'settings';
    return 'dashboard';
  };

  const activeTab = getActiveTab();

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
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', flexWrap: 'wrap', gap: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div>
              <h1 style={{
                fontSize: '32px',
                fontWeight: '700',
                margin: '0 0 4px 0',
                color: 'var(--text-primary)',
                letterSpacing: '-0.5px'
              }}>
                <span style={{ color: 'var(--primary)' }}>KC DaCRE8TOR</span> Prediction Dashboard
              </h1>
              <p style={{
                color: 'var(--text-secondary)',
                fontSize: '14px',
                margin: '0'
              }}>AI-Powered Sports Betting Intelligence</p>
            </div>
          </div>

          <nav className="tab-navigation">
            <TabButton
              icon={<LayoutDashboard size={20} />}
              label="Dashboard"
              active={activeTab === 'dashboard'}
              onClick={() => navigate('/dashboard')}
            />
            <TabButton
              icon={<Users size={20} />}
              label="Teams"
              active={activeTab === 'teams'}
              onClick={() => navigate('/teams')}
            />
            <TabButton
              icon={<UserCircle size={20} />}
              label="Players"
              active={activeTab === 'players'}
              onClick={() => navigate('/players')}
            />
            <TabButton
              icon={<Calendar size={20} />}
              label="Schedule"
              active={activeTab === 'schedule'}
              onClick={() => navigate('/schedule')}
            />
            <TabButton
              icon={<Wallet size={20} />}
              label="My Bets"
              active={activeTab === 'portfolio'}
              onClick={() => navigate('/portfolio')}
            />
            <TabButton
              icon={<TrendingUp size={20} />}
              label="Analytics"
              active={activeTab === 'analytics'}
              onClick={() => navigate('/analytics')}
            />
            <TabButton
              icon={<GitMerge size={20} />}
              label="Pipeline"
              active={activeTab === 'pipeline'}
              onClick={() => navigate('/pipeline')}
            />
            <TabButton
              icon={<Database size={20} />}
              label="Knowledge"
              active={activeTab === 'knowledge'}
              onClick={() => navigate('/knowledge')}
            />
            <TabButton
              icon={<MessageSquare size={20} />}
              label="KC Chat"
              active={activeTab === 'chat'}
              onClick={() => navigate('/chat')}
            />
            <TabButton
              icon={<SettingsIcon size={20} />}
              label="Settings"
              active={activeTab === 'settings'}
              onClick={() => navigate('/settings')}
            />
          </nav>
        </div>

        {/* Prominent Sport Switcher */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '16px 24px',
            background: 'var(--bg-card)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '12px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)'
          }}
        >
          <span style={{
            fontSize: '14px',
            fontWeight: '600',
            color: 'var(--text-secondary)',
            letterSpacing: '-0.01em'
          }}>
            Sport:
          </span>
          <div style={{
            display: 'flex',
            gap: '6px',
            padding: '4px',
            background: 'var(--bg-elevated)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '8px'
          }}>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setSelectedSport('NBA')}
              style={{
                padding: '10px 20px',
                background: selectedSport === 'NBA' ? 'var(--primary)' : 'transparent',
                border: 'none',
                borderRadius: '6px',
                color: selectedSport === 'NBA' ? 'white' : 'var(--text-secondary)',
                fontSize: '15px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                fontFamily: 'inherit',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                boxShadow: selectedSport === 'NBA' ? '0 2px 8px rgba(0, 217, 255, 0.3)' : 'none'
              }}
            >
              <span style={{ fontSize: '20px' }}>🏀</span>
              NBA
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setSelectedSport('NFL')}
              style={{
                padding: '10px 20px',
                background: selectedSport === 'NFL' ? 'var(--primary)' : 'transparent',
                border: 'none',
                borderRadius: '6px',
                color: selectedSport === 'NFL' ? 'white' : 'var(--text-secondary)',
                fontSize: '15px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                fontFamily: 'inherit',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                boxShadow: selectedSport === 'NFL' ? '0 2px 8px rgba(0, 217, 255, 0.3)' : 'none'
              }}
            >
              <span style={{ fontSize: '20px' }}>🏈</span>
              NFL
            </motion.button>
          </div>
          <span style={{
            fontSize: '13px',
            color: 'var(--text-tertiary)',
            marginLeft: 'auto',
            fontStyle: 'italic'
          }}>
            All data and predictions will update to match your selection
          </span>
        </motion.div>
      </motion.header>

      <Routes>
        {/* Dashboard */}
        <Route path="/" element={<Dashboard
          handleSelectGame={handleSelectGame}
          lastInput={lastInput}
          prediction={prediction}
          insight={insight}
          shapValues={shapValues}
          setIsBetModalOpen={setIsBetModalOpen}
          betSuccess={betSuccess}
        />} />
        <Route path="/dashboard" element={<Dashboard
          handleSelectGame={handleSelectGame}
          lastInput={lastInput}
          prediction={prediction}
          insight={insight}
          shapValues={shapValues}
          setIsBetModalOpen={setIsBetModalOpen}
          betSuccess={betSuccess}
        />} />

        {/* Teams */}
        <Route path="/teams" element={<TeamsEnhanced />} />
        <Route path="/teams/:teamId" element={<TeamDetail />} />

        {/* Players */}
        <Route path="/players" element={<PlayersEnhanced />} />

        {/* Schedule */}
        <Route path="/schedule" element={<Schedule />} />
        <Route path="/matchup/:matchupId" element={<Matchup />} />

        {/* Other Routes */}
        <Route path="/portfolio" element={<PortfolioEnhanced />} />
        <Route path="/analytics" element={<AnalyticsEnhanced />} />
        <Route path="/pipeline" element={<PipelineEnhanced />} />
        <Route path="/knowledge" element={<MemorySearchEnhanced />} />
        <Route path="/chat" element={<ChatEnhanced />} />
        <Route path="/settings" element={<SettingsEnhanced />} />
      </Routes>

      <BetPlacementModal
        isOpen={isBetModalOpen}
        onClose={handleBetModalClose}
        prediction={prediction}
        gameData={lastInput}
      />
    </div>
  );
}

const TabButton = ({ icon, label, active, onClick }) => (
  <motion.button
    whileHover={{ scale: 1.02 }}
    whileTap={{ scale: 0.98 }}
    onClick={onClick}
    className={`tab-button ${active ? 'active' : ''}`}
  >
    {icon}
    <span>{label}</span>
  </motion.button>
);

// Dashboard Component
const Dashboard = ({ handleSelectGame, lastInput, prediction, insight, shapValues, setIsBetModalOpen, betSuccess }) => (
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
);

export default App;
