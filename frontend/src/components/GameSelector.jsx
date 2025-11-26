import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Calendar, ChevronRight } from 'lucide-react';
import { useSport } from '../contexts/SportContext';

const GameSelector = ({ onSelectGame }) => {
    const { selectedSport } = useSport();
    const [games, setGames] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchGames = async () => {
            try {
                // Dynamically select endpoint based on selected sport
                const endpoint = selectedSport === 'NBA'
                    ? 'http://localhost:8000/nba/games'
                    : 'http://localhost:8000/games';

                const response = await axios.get(endpoint);

                // Handle different response structures
                const gamesData = response.data.games || response.data;
                setGames(gamesData);
            } catch (error) {
                console.error("Failed to fetch games:", error);
                setGames([]);
            } finally {
                setLoading(false);
            }
        };

        fetchGames();
    }, [selectedSport]);

    if (loading) {
        return (
            <div className="skeleton" style={{ height: '200px', marginBottom: '32px' }} />
        );
    }

    return (
        <div style={{ marginBottom: '32px' }}>
            <div className="section-header">
                <Calendar className="section-icon" size={24} />
                <h2 className="section-title">Upcoming Games (Real-Time)</h2>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {games.map((game, index) => (
                    <motion.button
                        key={game.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.05 }}
                        whileHover={{ scale: 1.02, x: 4 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => onSelectGame({
                            team_strength: game.home_strength,
                            opponent_strength: game.away_strength,
                            home_advantage: 1,
                            label: `${game.home_team} vs ${game.away_team}`
                        })}
                        className="card"
                        style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            padding: '20px',
                            textAlign: 'left',
                            border: 'none',
                            cursor: 'pointer',
                            position: 'relative',
                            overflow: 'hidden'
                        }}
                    >
                        <div style={{ flex: 1 }}>
                            <div style={{
                                fontWeight: '700',
                                color: 'var(--text-primary)',
                                fontSize: '15px',
                                marginBottom: '8px',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px'
                            }}>
                                {game.home_team} <span style={{ color: 'var(--text-tertiary)' }}>vs</span> {game.away_team}
                            </div>
                            <div style={{
                                fontSize: '12px',
                                color: 'var(--text-secondary)',
                                fontFamily: 'monospace'
                            }}>{game.commence_time}</div>
                        </div>
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px'
                        }}>
                            <div style={{
                                fontSize: '12px',
                                background: 'var(--bg-elevated)',
                                padding: '6px 12px',
                                borderRadius: 'var(--radius-sm)',
                                color: 'var(--primary)',
                                fontWeight: '600',
                                border: '1px solid var(--border-subtle)'
                            }}>
                                Select
                            </div>
                            <ChevronRight size={16} style={{ color: 'var(--primary)' }} />
                        </div>
                    </motion.button>
                ))}
            </div>
        </div>
    );
};

export default GameSelector;
