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
            className="glass-panel p-6 w-full max-w-md mx-auto"
        >
            <div className="flex items-center gap-2 mb-6">
                <Brain className="text-purple-500" size={24} />
                <h2 className="text-xl font-bold">Game Parameters</h2>
            </div>

            <div className="space-y-6">
                <div>
                    <div className="flex justify-between mb-2">
                        <label className="text-sm text-gray-400">Team Strength</label>
                        <span className="text-purple-400 font-mono">{teamStrength}</span>
                    </div>
                    <input
                        type="range"
                        min="0"
                        max="100"
                        value={teamStrength}
                        onChange={(e) => setTeamStrength(Number(e.target.value))}
                        className="w-full accent-purple-500"
                    />
                </div>

                <div>
                    <div className="flex justify-between mb-2">
                        <label className="text-sm text-gray-400">Opponent Strength</label>
                        <span className="text-cyan-400 font-mono">{opponentStrength}</span>
                    </div>
                    <input
                        type="range"
                        min="0"
                        max="100"
                        value={opponentStrength}
                        onChange={(e) => setOpponentStrength(Number(e.target.value))}
                        className="w-full accent-cyan-500"
                    />
                </div>

                <div className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg cursor-pointer"
                    onClick={() => setHomeAdvantage(!homeAdvantage)}>
                    <div className="flex items-center gap-2">
                        <Home className={homeAdvantage ? "text-green-400" : "text-gray-500"} size={20} />
                        <span className="text-sm">Home Advantage</span>
                    </div>
                    <div className={`w-10 h-6 rounded-full p-1 transition-colors ${homeAdvantage ? 'bg-green-500' : 'bg-slate-600'}`}>
                        <div className={`w-4 h-4 bg-white rounded-full transition-transform ${homeAdvantage ? 'translate-x-4' : ''}`} />
                    </div>
                </div>

                <button
                    onClick={handleSubmit}
                    disabled={isLoading}
                    className="w-full py-3 bg-gradient-to-r from-purple-600 to-cyan-600 rounded-lg font-bold text-white shadow-lg hover:shadow-purple-500/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {isLoading ? 'Crunching Numbers...' : 'Predict Outcome'}
                </button>
            </div>
        </motion.div>
    );
};

export default PredictionCard;
