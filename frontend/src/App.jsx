import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Activity, Zap, Wallet, LayoutDashboard, GitMerge } from 'lucide-react';
import PredictionCard from './components/PredictionCard';
import GrokInsight from './components/GrokInsight';
import StatsChart from './components/StatsChart';
import GameSelector from './components/GameSelector';
import ExplainabilityChart from './components/ExplainabilityChart';
import Portfolio from './components/Portfolio';
import Pipeline from './components/Pipeline';

const API_URL = 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard'); // 'dashboard', 'portfolio', 'pipeline'
  const [prediction, setPrediction] = useState(null);
  const [insight, setInsight] = useState(null);
  const [shapValues, setShapValues] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [lastInput, setLastInput] = useState(null);

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

  return (
    <div className="min-h-screen bg-slate-900 text-white p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl shadow-lg shadow-purple-500/20">
              <Activity size={32} className="text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold tracking-tight">
                <span className="gradient-text">Grok's</span> Prediction Dashboard
              </h1>
              <p className="text-slate-400 text-sm">AI-Powered Sports Betting Intelligence</p>
            </div>
          </div>

          <div className="flex bg-slate-800 rounded-lg p-1 border border-slate-700">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${activeTab === 'dashboard' ? 'bg-slate-700 text-white shadow-sm' : 'text-gray-400 hover:text-white'}`}
            >
              <LayoutDashboard size={18} />
              <span className="text-sm font-medium">Dashboard</span>
            </button>
            <button
              onClick={() => setActiveTab('pipeline')}
              className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${activeTab === 'pipeline' ? 'bg-slate-700 text-white shadow-sm' : 'text-gray-400 hover:text-white'}`}
            >
              <GitMerge size={18} />
              <span className="text-sm font-medium">Pipeline</span>
            </button>
            <button
              onClick={() => setActiveTab('portfolio')}
              className={`flex items-center gap-2 px-4 py-2 rounded-md transition-all ${activeTab === 'portfolio' ? 'bg-slate-700 text-white shadow-sm' : 'text-gray-400 hover:text-white'}`}
            >
              <Wallet size={18} />
              <span className="text-sm font-medium">My Bets</span>
            </button>
          </div>
        </header>

        {activeTab === 'dashboard' && (
          <main className="grid md:grid-cols-2 gap-8">
            <div className="space-y-8">
              <section>
                <GameSelector onSelectGame={handleSelectGame} />

                <div className="flex items-center gap-2 mb-4">
                  <Zap className="text-yellow-400" size={20} />
                  <h2 className="text-lg font-semibold text-slate-200">Custom Parameters</h2>
                </div>
                <PredictionCard onPredict={handlePredict} isLoading={isLoading} />
              </section>

              {lastInput && (
                <motion.section
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <StatsChart data={lastInput} />
                </motion.section>
              )}
            </div>

            <div className="space-y-8">
              <section>
                <div className="flex items-center gap-2 mb-4">
                  <Activity className="text-cyan-400" size={20} />
                  <h2 className="text-lg font-semibold text-slate-200">Live Analysis</h2>
                </div>

                {prediction !== null ? (
                  <div className="space-y-6">
                    <div className="glass-panel p-8 text-center relative overflow-hidden">
                      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-500 via-cyan-500 to-purple-500" />
                      <h3 className="text-slate-400 uppercase tracking-widest text-sm mb-2">Predicted Spread Margin</h3>
                      <div className="text-6xl font-black text-white mb-2 tracking-tighter">
                        {prediction > 0 ? '+' : ''}{prediction.toFixed(1)}
                      </div>
                      <div className={`inline-block px-3 py-1 rounded-full text-xs font-bold ${prediction > 0 ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                        {prediction > 0 ? 'FAVORABLE' : 'UNFAVORABLE'}
                      </div>
                    </div>

                    <GrokInsight insight={insight} prediction={prediction} />

                    <ExplainabilityChart shapValues={shapValues} />
                  </div>
                ) : (
                  <div className="glass-panel p-12 text-center border-dashed border-2 border-slate-700 bg-transparent">
                    <p className="text-slate-500">
                      Waiting for input data...
                      <br />
                      <span className="text-xs opacity-50">Select a game or configure parameters</span>
                    </p>
                  </div>
                )}
              </section>
            </div>
          </main>
        )}

        {activeTab === 'pipeline' && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <Pipeline />
          </motion.div>
        )}

        {activeTab === 'portfolio' && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <Portfolio />
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default App;
