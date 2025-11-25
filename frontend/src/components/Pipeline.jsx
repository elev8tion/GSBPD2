import React, { useState } from 'react';
import axios from 'axios';
import { Video, Cpu, Layers, ArrowRight, PlayCircle, Film, Youtube } from 'lucide-react';
import { motion } from 'framer-motion';

const API_URL = 'http://localhost:8000';

// Mock data for demonstration
const MOCK_GAME_RESULTS = {
    status: 'success',
    data: [
        {
            game_id: 'demo-1',
            home_team: 'Chiefs',
            away_team: 'Bills',
            home_score: 27,
            away_score: 24,
            quarter: 'Final'
        },
        {
            game_id: 'demo-2',
            home_team: 'Eagles',
            away_team: '49ers',
            home_score: 31,
            away_score: 17,
            quarter: 'Final'
        },
        {
            game_id: 'demo-3',
            home_team: 'Cowboys',
            away_team: 'Packers',
            home_score: 20,
            away_score: 23,
            quarter: '4th - 2:45'
        }
    ]
};

const MOCK_SGP_SUGGESTIONS = {
    'demo-1': [
        {
            name: 'High-Scoring Shootout',
            total_odds: 6.2,
            reasoning: 'Both teams averaging 28+ PPG. Chiefs offense explosive with Mahomes. Over 51.5 total points + Chiefs ML.'
        },
        {
            name: 'Mahomes Special',
            total_odds: 4.8,
            reasoning: 'Patrick Mahomes Over 2.5 Pass TDs + Chiefs -2.5 spread. Mahomes has 3+ TDs in 6 of last 8 games.'
        },
        {
            name: 'Defensive Battle',
            total_odds: 5.1,
            reasoning: 'Under 51.5 points + Bills +2.5 spread. Bills defense ranked #3, allowing only 18.2 PPG.'
        }
    ],
    'demo-2': [
        {
            name: 'Eagles Domination',
            total_odds: 5.5,
            reasoning: 'Eagles ML + Over 45.5 points. Hurts averaging 320 total yards per game, 49ers secondary struggling.'
        },
        {
            name: 'Rushing Attack',
            total_odds: 4.2,
            reasoning: 'Eagles -7 spread + Total rushing yards Over 180.5. Both teams rely heavily on ground game.'
        },
        {
            name: 'QB Duel',
            total_odds: 6.8,
            reasoning: 'Hurts Over 1.5 Rush TDs + Purdy Over 280.5 Pass Yards. Both QBs in MVP conversation.'
        }
    ],
    'demo-3': [
        {
            name: 'Packers Upset',
            total_odds: 7.5,
            reasoning: 'Packers ML +150 + Under 48.5. Packers defense improved, Cowboys struggling on the road.'
        },
        {
            name: 'Low Scoring Affair',
            total_odds: 4.5,
            reasoning: 'Under 48.5 total + Cowboys -3 spread. Cold weather game, both defenses ranked top 10.'
        },
        {
            name: 'Dak Prescott Special',
            total_odds: 5.9,
            reasoning: 'Prescott Over 2.5 TDs + Cowboys -3. Dak has 3+ TDs in 5 straight home games.'
        }
    ]
};

const Pipeline = () => {
    const [filePath, setFilePath] = useState('');
    const [youtubeUrl, setYoutubeUrl] = useState('');
    const [sport, setSport] = useState('nfl');
    const [category, setCategory] = useState('highlights');
    const [isIngesting, setIsIngesting] = useState(false);
    const [isProcessingYoutube, setIsProcessingYoutube] = useState(false);
    const [ingestResult, setIngestResult] = useState(null);
    const [youtubeResult, setYoutubeResult] = useState(null);
    const [sgpSuggestions, setSgpSuggestions] = useState({});
    const [loadingSgp, setLoadingSgp] = useState(null);
    const [useMockData, setUseMockData] = useState(false);

    const handleIngest = async () => {
        if (!filePath) return;
        setIsIngesting(true);
        setIngestResult(null);
        setSgpSuggestions({});
        setUseMockData(false);

        try {
            const response = await axios.post(`${API_URL}/pipeline/ingest`, { file_path: filePath });
            if (response.data && response.data.data && response.data.data.length > 0) {
                setIngestResult(response.data);
            } else {
                // Use mock data if API returns empty results
                setIngestResult(MOCK_GAME_RESULTS);
                setSgpSuggestions(MOCK_SGP_SUGGESTIONS);
                setUseMockData(true);
            }
        } catch (error) {
            console.error("Ingestion failed:", error);
            // Use mock data on error
            setIngestResult(MOCK_GAME_RESULTS);
            setSgpSuggestions(MOCK_SGP_SUGGESTIONS);
            setUseMockData(true);
        } finally {
            setIsIngesting(false);
        }
    };

    const loadDemoData = () => {
        setIngestResult(MOCK_GAME_RESULTS);
        setSgpSuggestions(MOCK_SGP_SUGGESTIONS);
        setUseMockData(true);
    };

    const handleYoutubeIngest = async () => {
        if (!youtubeUrl) return;
        setIsProcessingYoutube(true);
        setYoutubeResult(null);

        try {
            const response = await axios.post(`${API_URL}/pipeline/youtube`, {
                url: youtubeUrl,
                sport: sport,
                category: category
            });
            setYoutubeResult(response.data);
        } catch (error) {
            console.error("YouTube ingestion failed:", error);
            alert("Failed to process YouTube video. Check console for details.");
        } finally {
            setIsProcessingYoutube(false);
        }
    };

    const handleGenerateSGP = async (game) => {
        setLoadingSgp(game.game_id);
        try {
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

    const sportOptions = [
        { value: 'nfl', label: 'NFL', icon: '🏈' },
        { value: 'nba', label: 'NBA', icon: '🏀' }
    ];

    const categoryOptions = [
        { value: 'highlights', label: 'Game Highlights' },
        { value: 'analysis', label: 'Game Analysis' },
        { value: 'player-stats', label: 'Player Stats' }
    ];

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '32px', maxWidth: '100%' }}>
            {/* Video Ingest Section */}
            <motion.section
                className="section"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
            >
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '32px', flexWrap: 'wrap' }}>
                    <motion.div
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        style={{
                            padding: '16px',
                            background: 'var(--bg-elevated)',
                            borderRadius: 'var(--radius-lg)',
                            border: '2px solid var(--accent)',
                            boxShadow: 'var(--glow-accent)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}
                    >
                        <Film size={28} style={{ color: 'var(--accent)' }} />
                    </motion.div>
                    <div style={{ flex: '1 1 auto', minWidth: '200px' }}>
                        <h2 style={{
                            fontSize: '24px',
                            fontWeight: '700',
                            margin: '0 0 4px 0',
                            color: 'var(--text-primary)'
                        }}>Video Ingest Pipeline</h2>
                        <p style={{
                            fontSize: '14px',
                            color: 'var(--text-secondary)',
                            margin: 0
                        }}>Analyze screen recordings for real-time SGP insights</p>
                    </div>
                </div>

                <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                    <input
                        type="text"
                        value={filePath}
                        onChange={(e) => setFilePath(e.target.value)}
                        placeholder="/absolute/path/to/video.mp4"
                        className="input-field"
                        style={{
                            flex: '1 1 300px',
                            fontFamily: 'monospace',
                            fontSize: '14px',
                            minWidth: 0
                        }}
                    />
                    <motion.button
                        whileHover={{ scale: 1.01 }}
                        whileTap={{ scale: 0.99 }}
                        onClick={handleIngest}
                        disabled={isIngesting || !filePath}
                        className="btn btn-primary"
                        style={{
                            padding: '16px 32px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            fontSize: '15px',
                            fontWeight: '700',
                            opacity: (isIngesting || !filePath) ? 0.5 : 1,
                            cursor: (isIngesting || !filePath) ? 'not-allowed' : 'pointer',
                            background: isIngesting ? 'var(--bg-elevated)' : 'rgba(255, 184, 0, 0.1)',
                            color: isIngesting ? 'var(--text-secondary)' : 'var(--accent)',
                            border: isIngesting ? '2px solid var(--border-subtle)' : '2px solid var(--accent)',
                            whiteSpace: 'nowrap'
                        }}
                    >
                        {isIngesting ? (
                            <>
                                <Cpu className="animate-spin" size={20} />
                                Processing...
                            </>
                        ) : (
                            <>
                                <PlayCircle size={20} />
                                Analyze Video
                            </>
                        )}
                    </motion.button>
                    <motion.button
                        whileHover={{ scale: 1.01 }}
                        whileTap={{ scale: 0.99 }}
                        onClick={loadDemoData}
                        className="btn"
                        style={{
                            padding: '16px 32px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            fontSize: '15px',
                            fontWeight: '700',
                            background: 'rgba(0, 217, 255, 0.1)',
                            color: 'var(--primary)',
                            border: '2px solid var(--primary)',
                            whiteSpace: 'nowrap'
                        }}
                    >
                        <Layers size={20} />
                        Load Demo Data
                    </motion.button>
                </div>
            </motion.section>

            {/* YouTube Ingestion Section */}
            <motion.section
                className="section"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.1 }}
            >
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '32px', flexWrap: 'wrap' }}>
                    <motion.div
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        style={{
                            padding: '16px',
                            background: 'var(--bg-elevated)',
                            borderRadius: 'var(--radius-lg)',
                            border: '2px solid var(--secondary)',
                            boxShadow: 'var(--glow-secondary)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}
                    >
                        <Youtube size={28} style={{ color: 'var(--secondary)' }} />
                    </motion.div>
                    <div style={{ flex: '1 1 auto', minWidth: '200px' }}>
                        <h2 style={{
                            fontSize: '24px',
                            fontWeight: '700',
                            margin: '0 0 4px 0',
                            color: 'var(--text-primary)'
                        }}>YouTube Video Pipeline</h2>
                        <p style={{
                            fontSize: '14px',
                            color: 'var(--text-secondary)',
                            margin: 0
                        }}>Process NFL/NBA game highlights and analysis videos</p>
                    </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    {/* Sport Selection - Chip Style */}
                    <div>
                        <label className="input-label" style={{ marginBottom: '12px', display: 'block' }}>
                            Sport
                        </label>
                        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', maxWidth: '400px' }}>
                            {sportOptions.map((option) => (
                                <motion.button
                                    key={option.value}
                                    whileHover={{ scale: 1.01 }}
                                    whileTap={{ scale: 0.99 }}
                                    onClick={() => setSport(option.value)}
                                    className="card"
                                    style={{
                                        flex: '0 0 120px',
                                        padding: '12px 16px',
                                        cursor: 'pointer',
                                        border: sport === option.value ? '2px solid var(--secondary)' : '2px solid var(--border-subtle)',
                                        background: sport === option.value ? 'rgba(168, 85, 247, 0.1)' : 'var(--bg-card)',
                                        color: sport === option.value ? 'var(--secondary)' : 'var(--text-secondary)',
                                        fontWeight: '600',
                                        textAlign: 'center',
                                        transition: 'all 0.2s',
                                        fontSize: '14px',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        gap: '8px'
                                    }}
                                >
                                    <span style={{ fontSize: '18px' }}>{option.icon}</span>
                                    {option.label}
                                </motion.button>
                            ))}
                        </div>
                    </div>

                    {/* Category Selection - Chip Style */}
                    <div>
                        <label className="input-label" style={{ marginBottom: '12px', display: 'block' }}>
                            Category
                        </label>
                        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', maxWidth: '500px' }}>
                            {categoryOptions.map((option) => (
                                <motion.button
                                    key={option.value}
                                    whileHover={{ scale: 1.01 }}
                                    whileTap={{ scale: 0.99 }}
                                    onClick={() => setCategory(option.value)}
                                    className="card"
                                    style={{
                                        flex: '0 0 140px',
                                        padding: '12px 16px',
                                        cursor: 'pointer',
                                        border: category === option.value ? '2px solid var(--primary)' : '2px solid var(--border-subtle)',
                                        background: category === option.value ? 'rgba(0, 217, 255, 0.1)' : 'var(--bg-card)',
                                        color: category === option.value ? 'var(--primary)' : 'var(--text-secondary)',
                                        fontWeight: '600',
                                        textAlign: 'center',
                                        transition: 'all 0.2s',
                                        fontSize: '13px'
                                    }}
                                >
                                    {option.label}
                                </motion.button>
                            ))}
                        </div>
                    </div>

                    {/* URL Input */}
                    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                        <input
                            type="text"
                            value={youtubeUrl}
                            onChange={(e) => setYoutubeUrl(e.target.value)}
                            placeholder="https://youtube.com/watch?v=..."
                            className="input-field"
                            style={{
                                flex: '1 1 300px',
                                fontSize: '14px',
                                minWidth: 0
                            }}
                        />
                        <motion.button
                            whileHover={{ scale: 1.01 }}
                            whileTap={{ scale: 0.99 }}
                            onClick={handleYoutubeIngest}
                            disabled={isProcessingYoutube || !youtubeUrl}
                            className="btn btn-primary"
                            style={{
                                padding: '16px 32px',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px',
                                fontSize: '15px',
                                fontWeight: '700',
                                opacity: (isProcessingYoutube || !youtubeUrl) ? 0.5 : 1,
                                cursor: (isProcessingYoutube || !youtubeUrl) ? 'not-allowed' : 'pointer',
                                background: isProcessingYoutube ? 'var(--bg-elevated)' : 'rgba(168, 85, 247, 0.1)',
                                color: isProcessingYoutube ? 'var(--text-secondary)' : 'var(--secondary)',
                                border: isProcessingYoutube ? '2px solid var(--border-subtle)' : '2px solid var(--secondary)',
                                whiteSpace: 'nowrap'
                            }}
                        >
                            {isProcessingYoutube ? (
                                <>
                                    <Cpu className="animate-spin" size={20} />
                                    Processing...
                                </>
                            ) : (
                                <>
                                    <PlayCircle size={20} />
                                    Process Video
                                </>
                            )}
                        </motion.button>
                    </div>

                    {youtubeResult && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="card"
                            style={{
                                padding: '20px',
                                background: 'var(--bg-elevated)',
                                borderLeft: '3px solid var(--secondary)'
                            }}
                        >
                            <div style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
                                {youtubeResult.status === 'success' ? (
                                    <>
                                        <strong style={{ color: 'var(--secondary)' }}>✓ Success!</strong> Processed{' '}
                                        {youtubeResult.frames} frames from {youtubeResult.sport.toUpperCase()} {youtubeResult.category}
                                    </>
                                ) : (
                                    <>
                                        <strong style={{ color: 'var(--accent)' }}>⚠ Error:</strong> {youtubeResult.message}
                                    </>
                                )}
                            </div>
                        </motion.div>
                    )}
                </div>
            </motion.section>

            {/* Results Section */}
            {ingestResult && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.2 }}
                    style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}
                >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <Layers size={24} style={{ color: 'var(--primary)' }} />
                            <h3 style={{
                                fontSize: '20px',
                                fontWeight: '600',
                                color: 'var(--text-primary)',
                                margin: 0
                            }}>
                                Detected Games & Insights
                            </h3>
                        </div>
                        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                            {useMockData && (
                                <div style={{
                                    padding: '6px 12px',
                                    background: 'var(--accent)',
                                    borderRadius: 'var(--radius-md)',
                                    fontSize: '12px',
                                    fontWeight: '600',
                                    color: 'var(--text-primary)'
                                }}>
                                    Demo Data
                                </div>
                            )}
                            <div className="badge info" style={{ fontFamily: 'monospace' }}>
                                {ingestResult.data.length} items found
                            </div>
                        </div>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                        {ingestResult.data.map((game, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="card"
                                style={{ padding: 0, overflow: 'hidden' }}
                            >
                                <div style={{
                                    padding: '28px',
                                    background: 'var(--bg-elevated)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'space-between',
                                    borderBottom: '1px solid var(--border-subtle)',
                                    flexWrap: 'wrap',
                                    gap: '20px'
                                }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '32px', flexWrap: 'wrap' }}>
                                        <div style={{ textAlign: 'center', minWidth: '80px' }}>
                                            <div style={{
                                                fontSize: '11px',
                                                color: 'var(--text-tertiary)',
                                                textTransform: 'uppercase',
                                                letterSpacing: '1.5px',
                                                marginBottom: '8px',
                                                fontWeight: '600'
                                            }}>Home</div>
                                            <div style={{
                                                fontWeight: '700',
                                                color: 'var(--text-primary)',
                                                fontSize: '18px',
                                                marginBottom: '8px'
                                            }}>{game.home_team}</div>
                                            <div style={{
                                                fontSize: '36px',
                                                fontWeight: '900',
                                                color: 'var(--primary)',
                                                lineHeight: 1
                                            }}>{game.home_score}</div>
                                        </div>
                                        <div style={{
                                            color: 'var(--text-tertiary)',
                                            fontWeight: '700',
                                            fontSize: '20px'
                                        }}>VS</div>
                                        <div style={{ textAlign: 'center', minWidth: '80px' }}>
                                            <div style={{
                                                fontSize: '11px',
                                                color: 'var(--text-tertiary)',
                                                textTransform: 'uppercase',
                                                letterSpacing: '1.5px',
                                                marginBottom: '8px',
                                                fontWeight: '600'
                                            }}>Away</div>
                                            <div style={{
                                                fontWeight: '700',
                                                color: 'var(--text-primary)',
                                                fontSize: '18px',
                                                marginBottom: '8px'
                                            }}>{game.away_team}</div>
                                            <div style={{
                                                fontSize: '36px',
                                                fontWeight: '900',
                                                color: 'var(--secondary)',
                                                lineHeight: 1
                                            }}>{game.away_score}</div>
                                        </div>
                                    </div>

                                    <motion.button
                                        whileHover={{ scale: 1.01 }}
                                        whileTap={{ scale: 0.99 }}
                                        onClick={() => handleGenerateSGP(game)}
                                        disabled={loadingSgp === game.game_id}
                                        style={{
                                            padding: '12px 24px',
                                            background: loadingSgp === game.game_id ? 'var(--bg-card)' : 'rgba(0, 217, 255, 0.1)',
                                            color: 'var(--primary)',
                                            border: `2px solid var(--primary)`,
                                            borderRadius: 'var(--radius-md)',
                                            fontSize: '14px',
                                            fontWeight: '700',
                                            cursor: loadingSgp === game.game_id ? 'not-allowed' : 'pointer',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '8px',
                                            transition: 'all 0.2s ease',
                                            opacity: loadingSgp === game.game_id ? 0.6 : 1,
                                            whiteSpace: 'nowrap'
                                        }}
                                    >
                                        {loadingSgp === game.game_id ? (
                                            <Cpu className="animate-spin" size={18} />
                                        ) : (
                                            <Layers size={18} />
                                        )}
                                        Generate SGP
                                    </motion.button>
                                </div>

                                {/* SGP Suggestions */}
                                {sgpSuggestions[game.game_id] && (
                                    <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: 'auto', opacity: 1 }}
                                        transition={{ duration: 0.4 }}
                                        style={{
                                            padding: '28px',
                                            background: 'var(--bg-card)'
                                        }}
                                    >
                                        <h4 style={{
                                            fontSize: '11px',
                                            fontWeight: '700',
                                            color: 'var(--text-secondary)',
                                            textTransform: 'uppercase',
                                            letterSpacing: '2px',
                                            marginBottom: '20px',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '8px'
                                        }}>
                                            <Layers size={14} style={{ color: 'var(--secondary)' }} />
                                            AI-Optimized Parlay Suggestions
                                        </h4>
                                        <div style={{
                                            display: 'grid',
                                            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                                            gap: '16px'
                                        }}>
                                            {sgpSuggestions[game.game_id].map((sgp, i) => (
                                                <motion.div
                                                    key={i}
                                                    initial={{ opacity: 0, y: 20 }}
                                                    animate={{ opacity: 1, y: 0 }}
                                                    transition={{ delay: i * 0.1 }}
                                                    whileHover={{ y: -2 }}
                                                    className="card"
                                                    style={{
                                                        padding: '20px',
                                                        cursor: 'pointer',
                                                        position: 'relative',
                                                        borderLeft: `3px solid var(--secondary)`
                                                    }}
                                                >
                                                    <div style={{
                                                        display: 'flex',
                                                        justifyContent: 'space-between',
                                                        alignItems: 'flex-start',
                                                        marginBottom: '12px'
                                                    }}>
                                                        <div className="badge" style={{
                                                            background: 'rgba(168, 85, 247, 0.1)',
                                                            color: 'var(--secondary)',
                                                            border: '1px solid var(--secondary)',
                                                            fontSize: '11px',
                                                            fontWeight: '700'
                                                        }}>
                                                            {(sgp.total_odds).toFixed(2)}x ODDS
                                                        </div>
                                                        <motion.div
                                                            whileHover={{ x: 4 }}
                                                            transition={{ type: 'spring', stiffness: 300 }}
                                                        >
                                                            <ArrowRight size={16} style={{ color: 'var(--primary)' }} />
                                                        </motion.div>
                                                    </div>
                                                    <div style={{
                                                        fontSize: '15px',
                                                        fontWeight: '700',
                                                        color: 'var(--text-primary)',
                                                        marginBottom: '8px'
                                                    }}>{sgp.name}</div>
                                                    <div style={{
                                                        fontSize: '13px',
                                                        color: 'var(--text-secondary)',
                                                        lineHeight: '1.5',
                                                        display: '-webkit-box',
                                                        WebkitLineClamp: 2,
                                                        WebkitBoxOrient: 'vertical',
                                                        overflow: 'hidden'
                                                    }}>{sgp.reasoning}</div>
                                                </motion.div>
                                            ))}
                                        </div>
                                    </motion.div>
                                )}
                            </motion.div>
                        ))}
                    </div>
                </motion.div>
            )}
        </div>
    );
};

export default Pipeline;
