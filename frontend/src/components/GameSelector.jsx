import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Calendar } from 'lucide-react';

const GameSelector = ({ onSelectGame }) => {
    const [games, setGames] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchGames = async () => {
            try {
                const response = await axios.get('http://localhost:8000/games');
                setGames(response.data);
            } catch (error) {
                console.error("Failed to fetch games:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchGames();
    }, []);

    if (loading) return <div className="text-center text-gray-500 text-sm">Loading upcoming games...</div>;

    return (
        <div className="mb-8">
            <div className="flex items-center gap-2 mb-4">
                <Calendar className="text-cyan-400" size={20} />
                <h2 className="text-lg font-semibold text-slate-200">Upcoming Games (Real-Time)</h2>
            </div>

            <div className="grid gap-3">
                {games.map((game) => (
                    <button
                        key={game.id}
                        onClick={() => onSelectGame({
                            team_strength: game.home_strength,
                            opponent_strength: game.away_strength,
                            home_advantage: 1, // Assuming user picks home team perspective
                            label: `${game.home_team} vs ${game.away_team}`
                        })}
                        className="flex items-center justify-between p-4 glass-panel hover:bg-slate-800/50 transition-colors text-left group"
                    >
                        <div>
                            <div className="font-bold text-white group-hover:text-cyan-400 transition-colors">
                                {game.home_team} vs {game.away_team}
                            </div>
                            <div className="text-xs text-gray-500">{game.commence_time}</div>
                        </div>
                        <div className="text-xs bg-slate-700 px-2 py-1 rounded text-gray-300">
                            Select
                        </div>
                    </button>
                ))}
            </div>
        </div>
    );
};

export default GameSelector;
