import React, { useState } from 'react';
import axios from 'axios';
import { Video, Cpu, Layers, ArrowRight, PlayCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const API_URL = 'http://localhost:8000';

const Pipeline = () => {
    const [filePath, setFilePath] = useState('');
    const [isIngesting, setIsIngesting] = useState(false);
    const [ingestResult, setIngestResult] = useState(null);
    const [sgpSuggestions, setSgpSuggestions] = useState({});
    const [loadingSgp, setLoadingSgp] = useState(null);

    const handleIngest = async () => {
        if (!filePath) return;
        setIsIngesting(true);
        setIngestResult(null);
        setSgpSuggestions({});

        try {
            const response = await axios.post(`${API_URL}/pipeline/ingest`, { file_path: filePath });
            setIngestResult(response.data);
        } catch (error) {
            console.error("Ingestion failed:", error);
            alert("Failed to ingest video. Check console for details.");
        } finally {
            setIsIngesting(false);
        }
    };

    const handleGenerateSGP = async (game) => {
        setLoadingSgp(game.game_id);
        try {
            // We use the extracted data to request an SGP
            // We assume a prediction margin based on the extracted score for this demo
            // In a real scenario, we'd run the prediction model *on* the extracted data first
            const margin = game.home_score - game.away_score;

            const response = await axios.post(`${API_URL}/pipeline/sgp`, {
                game_id: game.game_id,
                prediction_margin: margin,
                home_team: game.home_team,
                away_team: game.away_team
            });

            setSgpSuggestions(prev => ({
                ...prev,
                [game.game_id]: response.data
            }));
        } catch (error) {
            console.error("SGP Generation failed:", error);
        } finally {
            setLoadingSgp(null);
        }
    };

    return (
        <div className="space-y-8">
            {/* Ingestion Section */}
            <section className="glass-panel p-6">
                <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-pink-500/20 rounded-lg text-pink-400">
                        <Video size={24} />
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-white">Video Ingest Pipeline</h2>
                        <p className="text-sm text-slate-400">Analyze screen recordings for real-time SGP insights</p>
                    </div>
                </div>

                <div className="flex gap-4">
                    <input
                        type="text"
                        value={filePath}
                        onChange={(e) => setFilePath(e.target.value)}
                        placeholder="/absolute/path/to/video.mp4"
                        className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-pink-500 transition-colors font-mono text-sm"
                    />
                    <button
                        onClick={handleIngest}
                        disabled={isIngesting || !filePath}
                        className={`px-6 py-3 rounded-lg font-bold flex items-center gap-2 transition-all ${isIngesting
                                ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                                : 'bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white shadow-lg shadow-pink-500/20'
                            }`}
                    >
                        {isIngesting ? (
                            <>
                                <Cpu className="animate-spin" size={18} />
                                Processing...
                            </>
                        ) : (
                            <>
                                <PlayCircle size={18} />
                                Analyze Video
                            </>
                        )}
                    </button>
                </div>
            </section>

            {/* Results Section */}
            {ingestResult && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-6"
                >
                    <div className="flex items-center justify-between">
                        <h3 className="text-lg font-semibold text-slate-200 flex items-center gap-2">
                            <Layers size={20} className="text-cyan-400" />
                            Detected Games & Insights
                        </h3>
                        <span className="text-xs font-mono text-slate-500">
                            {ingestResult.data.length} items found
                        </span>
                    </div>

                    <div className="grid gap-4">
                        {ingestResult.data.map((game, index) => (
                            <div key={index} className="glass-panel p-0 overflow-hidden border border-slate-700/50">
                                <div className="p-4 bg-slate-800/50 flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <div className="text-center">
                                            <div className="text-xs text-slate-500 uppercase tracking-wider">Home</div>
                                            <div className="font-bold text-white text-lg">{game.home_team}</div>
                                            <div className="text-2xl font-black text-slate-200">{game.home_score}</div>
                                        </div>
                                        <div className="text-slate-600 font-bold text-xl">VS</div>
                                        <div className="text-center">
                                            <div className="text-xs text-slate-500 uppercase tracking-wider">Away</div>
                                            <div className="font-bold text-white text-lg">{game.away_team}</div>
                                            <div className="text-2xl font-black text-slate-200">{game.away_score}</div>
                                        </div>
                                    </div>

                                    <button
                                        onClick={() => handleGenerateSGP(game)}
                                        disabled={loadingSgp === game.game_id}
                                        className="px-4 py-2 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 border border-cyan-500/50 rounded-lg text-sm font-bold transition-all flex items-center gap-2"
                                    >
                                        {loadingSgp === game.game_id ? (
                                            <Cpu className="animate-spin" size={16} />
                                        ) : (
                                            <Layers size={16} />
                                        )}
                                        Generate SGP
                                    </button>
                                </div>

                                {/* SGP Suggestions */}
                                {sgpSuggestions[game.game_id] && (
                                    <motion.div
                                        initial={{ height: 0 }}
                                        animate={{ height: 'auto' }}
                                        className="bg-slate-900/50 border-t border-slate-700 p-4"
                                    >
                                        <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">
                                            AI-Optimized Parlay Suggestions
                                        </h4>
                                        <div className="grid md:grid-cols-3 gap-3">
                                            {sgpSuggestions[game.game_id].map((sgp, i) => (
                                                <div key={i} className="bg-slate-800 rounded-lg p-3 border border-slate-700 hover:border-cyan-500/50 transition-colors cursor-pointer group">
                                                    <div className="flex justify-between items-start mb-2">
                                                        <span className="text-xs font-bold text-purple-400 bg-purple-400/10 px-2 py-0.5 rounded">
                                                            {(sgp.total_odds).toFixed(2)}x Odds
                                                        </span>
                                                        <ArrowRight size={14} className="text-slate-600 group-hover:text-cyan-400 transition-colors" />
                                                    </div>
                                                    <div className="text-sm font-medium text-white mb-1">{sgp.name}</div>
                                                    <div className="text-xs text-slate-500 line-clamp-2">{sgp.reasoning}</div>
                                                </div>
                                            ))}
                                        </div>
                                    </motion.div>
                                )}
                            </div>
                        ))}
                    </div>
                </motion.div>
            )}
        </div>
    );
};

export default Pipeline;
