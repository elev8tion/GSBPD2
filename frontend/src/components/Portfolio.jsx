import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Wallet, TrendingUp, TrendingDown } from 'lucide-react';

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

    if (loading) return <div className="text-center text-gray-500">Loading portfolio...</div>;

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-3 gap-4">
                <div className="glass-panel p-4 text-center">
                    <div className="text-gray-400 text-xs uppercase tracking-widest mb-1">Total Wagered</div>
                    <div className="text-2xl font-bold text-white">${totalWagered.toFixed(2)}</div>
                </div>
                <div className="glass-panel p-4 text-center">
                    <div className="text-gray-400 text-xs uppercase tracking-widest mb-1">Win Rate</div>
                    <div className="text-2xl font-bold text-green-400">
                        {bets.length > 0 ? ((wins / bets.length) * 100).toFixed(0) : 0}%
                    </div>
                </div>
                <div className="glass-panel p-4 text-center">
                    <div className="text-gray-400 text-xs uppercase tracking-widest mb-1">Net Profit</div>
                    <div className="text-2xl font-bold text-purple-400">
                        ${(wins * 50 - losses * 50).toFixed(2)} <span className="text-xs text-gray-500">(Est)</span>
                    </div>
                </div>
            </div>

            <div className="glass-panel p-6">
                <div className="flex items-center gap-2 mb-4">
                    <Wallet className="text-purple-400" size={20} />
                    <h2 className="text-lg font-semibold text-slate-200">Bet History (Memvid Storage)</h2>
                </div>

                <div className="space-y-3">
                    {bets.length === 0 ? (
                        <p className="text-gray-500 text-center py-4">No bets recorded yet.</p>
                    ) : (
                        bets.map((bet, index) => (
                            <div key={index} className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg border border-slate-700">
                                <div>
                                    <div className="font-bold text-white">{bet.home_team} vs {bet.away_team}</div>
                                    <div className="text-xs text-gray-400">
                                        {bet.bet_type} • Odds: {bet.odds} • Pred: {bet.prediction_used.toFixed(1)}
                                    </div>
                                </div>
                                <div className="text-right">
                                    <div className="font-mono text-cyan-400">${bet.wager_amount}</div>
                                    <div className="text-xs text-gray-500">
                                        {index % 2 === 0 ? (
                                            <span className="flex items-center gap-1 text-green-500"><TrendingUp size={12} /> Win</span>
                                        ) : (
                                            <span className="flex items-center gap-1 text-red-500"><TrendingDown size={12} /> Loss</span>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};

export default Portfolio;
