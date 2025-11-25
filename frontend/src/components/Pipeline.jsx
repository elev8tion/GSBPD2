import React, { useState } from 'react';
import axios from 'axios';
import { Video, Cpu, Layers, ArrowRight, PlayCircle } from 'lucide-react';
import { motion } from 'framer-motion';

const API_URL = 'http://localhost:8000';

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
        <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
            {/* Ingestion Section */}
            <motion.section
                className="section"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
            >
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '32px' }}>
                    <motion.div
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        style={{
                            padding: '16px',
                            background: 'var(--bg-elevated)',
                            borderRadius: 'var(--radius-lg)',
                            border: '2px solid var(--accent)',
                            boxShadow: '0 0 20px rgba(255, 62, 157, 0.15)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}
                    >
                        <Video size={28} style={{ color: 'var(--accent)' }} />
                    </motion.div>
                    <div>
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

                <div style={{ display: 'flex', gap: '16px' }}>
                    <input
                        type="text"
                        value={filePath}
                        onChange={(e) => setFilePath(e.target.value)}
                        placeholder="/absolute/path/to/video.mp4"
                        className="input-field"
                        style={{
                            flex: 1,
                            fontFamily: 'monospace',
                            fontSize: '14px'
                        }}
                    />
                    <motion.button
                        whileHover={{ scale: 1.02, y: -2 }}
                        whileTap={{ scale: 0.98 }}
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
                            background: isIngesting ? 'var(--bg-elevated)' : 'var(--accent)',
                            color: isIngesting ? 'var(--text-secondary)' : 'var(--bg-dark)',
                            border: isIngesting ? '1px solid var(--border-subtle)' : 'none'
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
                </div>
            </motion.section>

            {/* YouTube Ingestion Section */}
            <motion.section
                className="section"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.1 }}
            >
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '32px' }}>
                    <motion.div
                        whileHover={{ scale: 1.1, rotate: 5 }}
                        style={{
                            padding: '16px',
                            background: 'var(--bg-elevated)',
                            borderRadius: 'var(--radius-lg)',
                            border: '2px solid var(--secondary)',
                            boxShadow: '0 0 20px rgba(168, 85, 247, 0.15)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}
                    >
                        <PlayCircle size={28} style={{ color: 'var(--secondary)' }} />
                    </motion.div>
                    <div>
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

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div style={{ display: 'flex', gap: '12px' }}>
                        <select
                            value={sport}
                            onChange={(e) => setSport(e.target.value)}
                            className="input-field"
                            style={{ width: '150px' }}
                        >
                            <option value="nfl">🏈 NFL</option>
                            <option value="nba">🏀 NBA</option>
                        </select>
                        <select
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            className="input-field"
                            style={{ width: '200px' }}
                        >
                            <option value="highlights">Game Highlights</option>
                            <option value="analysis">Game Analysis</option>
                            <option value="player-stats">Player Stats</option>
                        </select>
                    </div>

                    <div style={{ display: 'flex', gap: '16px' }}>
                        <input
                            type="text"
                            value={youtubeUrl}
                            onChange={(e) => setYoutubeUrl(e.target.value)}
                            placeholder="https://youtube.com/watch?v=..."
                            className="input-field"
                            style={{
                                flex: 1,
                                fontSize: '14px'
                            }}
                        />
                        <motion.button
                            whileHover={{ scale: 1.02, y: -2 }}
                            whileTap={{ scale: 0.98 }}
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
                                background: isProcessingYoutube ? 'var(--bg-elevated)' : 'var(--secondary)',
                                color: isProcessingYoutube ? 'var(--text-secondary)' : '#fff',
                                border: isProcessingYoutube ? '1px solid var(--border-subtle)' : 'none'
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
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
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
                        <div className="badge info" style={{ fontFamily: 'monospace' }}>
                            {ingestResult.data.length} items found
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
                                    borderBottom: '1px solid var(--border-subtle)'
                                }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '32px' }}>
                                        <div style={{ textAlign: 'center' }}>
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
                                        <div style={{ textAlign: 'center' }}>
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
                                        whileHover={{ scale: 1.05, x: 4 }}
                                        whileTap={{ scale: 0.95 }}
                                        onClick={() => handleGenerateSGP(game)}
                                        disabled={loadingSgp === game.game_id}
                                        style={{
                                            padding: '12px 24px',
                                            background: loadingSgp === game.game_id ? 'var(--bg-card)' : 'transparent',
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
                                            opacity: loadingSgp === game.game_id ? 0.6 : 1
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
                                        <div className="grid-3">
                                            {sgpSuggestions[game.game_id].map((sgp, i) => (
                                                <motion.div
                                                    key={i}
                                                    initial={{ opacity: 0, y: 20 }}
                                                    animate={{ opacity: 1, y: 0 }}
                                                    transition={{ delay: i * 0.1 }}
                                                    whileHover={{ y: -4, scale: 1.02 }}
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
