import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';
import {
  ArrowLeft,
  TrendingUp,
  Activity,
  BarChart3,
  Calendar,
  Award,
  Target
} from 'lucide-react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { useNotification } from '../contexts/NotificationContext';
import { PlayerCardSkeleton, TableRowSkeleton } from './LoadingSkeleton';
import RefreshButton from './RefreshButton';
import DataFreshnessIndicator from './DataFreshnessIndicator';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const PlayerDetail = () => {
  const { playerId } = useParams();
  const navigate = useNavigate();
  const { showNotification } = useNotification();

  const [playerData, setPlayerData] = useState(null);
  const [seasonAverages, setSeasonAverages] = useState(null);
  const [gameLogs, setGameLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [activeTab, setActiveTab] = useState('overview'); // overview, gamelogs, charts

  useEffect(() => {
    fetchPlayerData();
  }, [playerId]);

  const fetchPlayerData = async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }

      // Fetch season averages
      const averagesResponse = await axios.get(
        `${API_BASE}/nba/stats/players/${playerId}/averages`
      );
      setSeasonAverages(averagesResponse.data);

      // Fetch game logs (last 10 games)
      const gameLogsResponse = await axios.get(
        `${API_BASE}/nba/stats/players/${playerId}/gamelogs?limit=10`
      );
      setGameLogs(gameLogsResponse.data.games || []);

      // Extract basic player info from averages endpoint
      setPlayerData({
        id: playerId,
        name: averagesResponse.data.player_name || `Player ${playerId}`,
        team: averagesResponse.data.team_abbreviation || 'N/A',
        position: averagesResponse.data.position || 'N/A',
        jersey: averagesResponse.data.jersey_number || 'N/A',
        // Generate image URLs from player ID
        image_url: `https://cdn.nba.com/headshots/nba/latest/1040x760/${playerId}.png`,
        image_url_small: `https://cdn.nba.com/headshots/nba/latest/260x190/${playerId}.png`
      });

      setLastUpdated(new Date().toISOString());

      if (isRefresh) {
        showNotification({
          type: 'success',
          message: 'Player stats refreshed successfully!'
        });
      }
    } catch (error) {
      console.error('Error fetching player data:', error);
      showNotification({
        type: 'error',
        title: 'Failed to Load Player Data',
        message: error.response?.data?.detail || 'Could not fetch player information. Please try again.'
      });
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    fetchPlayerData(true);
  };

  // Prepare radar chart data
  const getRadarData = () => {
    if (!seasonAverages) return [];

    return [
      { stat: 'PTS', value: parseFloat(seasonAverages.points_per_game || 0), max: 35 },
      { stat: 'REB', value: parseFloat(seasonAverages.rebounds_per_game || 0), max: 15 },
      { stat: 'AST', value: parseFloat(seasonAverages.assists_per_game || 0), max: 12 },
      { stat: 'STL', value: parseFloat(seasonAverages.steals_per_game || 0), max: 3 },
      { stat: 'BLK', value: parseFloat(seasonAverages.blocks_per_game || 0), max: 3 }
    ];
  };

  // Prepare game logs trend data
  const getTrendData = () => {
    return [...gameLogs].reverse().map((game, index) => ({
      game: index + 1,
      date: game.game_date,
      pts: parseInt(game.pts || 0),
      reb: parseInt(game.reb || 0),
      ast: parseInt(game.ast || 0)
    }));
  };

  if (loading) {
    return (
      <div>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{ marginBottom: '24px' }}
        >
          <PlayerCardSkeleton />
        </motion.div>
        <div style={{ display: 'grid', gap: '12px' }}>
          {[1, 2, 3, 4, 5].map(i => (
            <TableRowSkeleton key={i} columns={6} />
          ))}
        </div>
      </div>
    );
  }

  if (!playerData || !seasonAverages) {
    return (
      <div className="section" style={{ textAlign: 'center', padding: '60px 20px' }}>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>
          Player not found
        </p>
        <button
          className="button-primary"
          onClick={() => navigate('/players')}
          style={{
            padding: '10px 20px',
            background: 'var(--primary)',
            border: 'none',
            borderRadius: 'var(--radius-sm)',
            color: 'white',
            cursor: 'pointer'
          }}
        >
          Back to Players
        </button>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ marginBottom: '32px' }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
          <button
            onClick={() => navigate(-1)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              padding: '8px 14px',
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '500',
              transition: 'all 0.15s ease'
            }}
          >
            <ArrowLeft size={16} />
            Back
          </button>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {lastUpdated && <DataFreshnessIndicator lastUpdated={lastUpdated} />}
            <RefreshButton onRefresh={handleRefresh} loading={refreshing} lastRefresh={lastUpdated} />
          </div>
        </div>

        {/* Player Info Card */}
        <div className="section" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '20px', flexWrap: 'wrap' }}>
            <div style={{
              width: '120px',
              height: '120px',
              borderRadius: '50%',
              background: playerData.image_url ? 'transparent' : 'var(--primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '32px',
              fontWeight: '700',
              color: 'white',
              overflow: 'hidden',
              border: '3px solid var(--border-subtle)',
              flexShrink: 0
            }}>
              {playerData.image_url ? (
                <img
                  src={playerData.image_url_small}
                  alt={playerData.name}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover'
                  }}
                  onError={(e) => {
                    // Fallback to jersey number on error
                    e.target.style.display = 'none';
                    e.target.parentElement.style.background = 'var(--primary)';
                    e.target.parentElement.innerHTML = playerData.jersey;
                  }}
                />
              ) : (
                playerData.jersey
              )}
            </div>
            <div style={{ flex: 1 }}>
              <h1 style={{
                fontSize: '28px',
                fontWeight: '700',
                color: 'var(--text-primary)',
                marginBottom: '8px',
                letterSpacing: '-0.03em'
              }}>
                {playerData.name}
              </h1>
              <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
                <div className="badge info">
                  {playerData.team}
                </div>
                <div className="badge">
                  {playerData.position}
                </div>
                <div className="badge">
                  #{playerData.jersey}
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Tabs */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        style={{
          display: 'flex',
          gap: '12px',
          marginBottom: '24px',
          borderBottom: '1px solid var(--border-subtle)',
          paddingBottom: '12px'
        }}
      >
        <TabButton active={activeTab === 'overview'} onClick={() => setActiveTab('overview')}>
          <Award size={16} />
          Overview
        </TabButton>
        <TabButton active={activeTab === 'gamelogs'} onClick={() => setActiveTab('gamelogs')}>
          <Calendar size={16} />
          Game Logs
        </TabButton>
        <TabButton active={activeTab === 'charts'} onClick={() => setActiveTab('charts')}>
          <BarChart3 size={16} />
          Charts
        </TabButton>
      </motion.div>

      {/* Tab Content */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2 }}
      >
        {activeTab === 'overview' && (
          <OverviewTab seasonAverages={seasonAverages} gameLogs={gameLogs} />
        )}
        {activeTab === 'gamelogs' && (
          <GameLogsTab gameLogs={gameLogs} />
        )}
        {activeTab === 'charts' && (
          <ChartsTab
            radarData={getRadarData()}
            trendData={getTrendData()}
            seasonAverages={seasonAverages}
          />
        )}
      </motion.div>
    </div>
  );
};

// Tab Components
const TabButton = ({ children, active, onClick }) => (
  <motion.button
    whileHover={{ scale: 1.02 }}
    whileTap={{ scale: 0.98 }}
    onClick={onClick}
    style={{
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: '10px 18px',
      background: active ? 'var(--bg-elevated)' : 'transparent',
      border: 'none',
      borderBottom: active ? '2px solid var(--primary)' : '2px solid transparent',
      color: active ? 'var(--primary)' : 'var(--text-secondary)',
      fontSize: '14px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'all 0.15s ease',
      fontFamily: 'inherit'
    }}
  >
    {children}
  </motion.button>
);

const OverviewTab = ({ seasonAverages, gameLogs }) => {
  const last5Games = gameLogs.slice(0, 5);
  const last5Avg = last5Games.length > 0 ? {
    pts: (last5Games.reduce((sum, g) => sum + parseInt(g.pts || 0), 0) / last5Games.length).toFixed(1),
    reb: (last5Games.reduce((sum, g) => sum + parseInt(g.reb || 0), 0) / last5Games.length).toFixed(1),
    ast: (last5Games.reduce((sum, g) => sum + parseInt(g.ast || 0), 0) / last5Games.length).toFixed(1)
  } : null;

  return (
    <div style={{ display: 'grid', gap: '20px' }}>
      {/* Season Averages */}
      <div className="section" style={{ padding: '24px' }}>
        <h3 style={{
          fontSize: '18px',
          fontWeight: '600',
          color: 'var(--text-primary)',
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <TrendingUp size={18} />
          Season Averages (2024-25)
        </h3>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
          gap: '16px'
        }}>
          <StatCard label="PPG" value={seasonAverages.points_per_game} color="var(--primary)" />
          <StatCard label="RPG" value={seasonAverages.rebounds_per_game} color="var(--success)" />
          <StatCard label="APG" value={seasonAverages.assists_per_game} color="var(--warning)" />
          <StatCard label="FG%" value={`${seasonAverages.field_goal_pct}%`} color="#9333EA" />
          <StatCard label="3P%" value={`${seasonAverages.three_point_pct}%`} color="#EC4899" />
          <StatCard label="FT%" value={`${seasonAverages.free_throw_pct}%`} color="#14B8A6" />
        </div>
      </div>

      {/* Last 5 Games Average */}
      {last5Avg && (
        <div className="section" style={{ padding: '24px' }}>
          <h3 style={{
            fontSize: '18px',
            fontWeight: '600',
            color: 'var(--text-primary)',
            marginBottom: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <Activity size={18} />
            Last 5 Games Average
          </h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
            gap: '16px'
          }}>
            <StatCard label="PPG" value={last5Avg.pts} color="var(--primary)" />
            <StatCard label="RPG" value={last5Avg.reb} color="var(--success)" />
            <StatCard label="APG" value={last5Avg.ast} color="var(--warning)" />
          </div>
        </div>
      )}
    </div>
  );
};

const GameLogsTab = ({ gameLogs }) => (
  <div className="section" style={{ padding: '24px', overflowX: 'auto' }}>
    <h3 style={{
      fontSize: '18px',
      fontWeight: '600',
      color: 'var(--text-primary)',
      marginBottom: '20px'
    }}>
      Recent Games
    </h3>
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ borderBottom: '2px solid var(--border-subtle)' }}>
          <th style={tableHeaderStyle}>Date</th>
          <th style={tableHeaderStyle}>Matchup</th>
          <th style={tableHeaderStyle}>PTS</th>
          <th style={tableHeaderStyle}>REB</th>
          <th style={tableHeaderStyle}>AST</th>
          <th style={tableHeaderStyle}>STL</th>
          <th style={tableHeaderStyle}>BLK</th>
          <th style={tableHeaderStyle}>FG%</th>
          <th style={tableHeaderStyle}>MIN</th>
        </tr>
      </thead>
      <tbody>
        {gameLogs.map((game, index) => (
          <motion.tr
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.05 }}
            style={{
              borderBottom: '1px solid var(--border-subtle)',
              transition: 'background 0.15s ease'
            }}
            whileHover={{ backgroundColor: 'var(--bg-elevated)' }}
          >
            <td style={tableCellStyle}>{game.game_date}</td>
            <td style={tableCellStyle}>{game.matchup}</td>
            <td style={{ ...tableCellStyle, fontWeight: '700', color: 'var(--primary)' }}>
              {game.pts}
            </td>
            <td style={tableCellStyle}>{game.reb}</td>
            <td style={tableCellStyle}>{game.ast}</td>
            <td style={tableCellStyle}>{game.stl}</td>
            <td style={tableCellStyle}>{game.blk}</td>
            <td style={tableCellStyle}>{game.fg_pct}%</td>
            <td style={tableCellStyle}>{game.min}</td>
          </motion.tr>
        ))}
      </tbody>
    </table>
    {gameLogs.length === 0 && (
      <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-secondary)' }}>
        No game logs available
      </div>
    )}
  </div>
);

const ChartsTab = ({ radarData, trendData, seasonAverages }) => (
  <div style={{ display: 'grid', gap: '20px' }}>
    {/* Performance Radar */}
    <div className="section" style={{ padding: '24px' }}>
      <h3 style={{
        fontSize: '18px',
        fontWeight: '600',
        color: 'var(--text-primary)',
        marginBottom: '20px'
      }}>
        Performance Profile
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <RadarChart data={radarData}>
          <PolarGrid stroke="var(--border-subtle)" />
          <PolarAngleAxis
            dataKey="stat"
            tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 'auto']}
            tick={{ fill: 'var(--text-tertiary)', fontSize: 10 }}
          />
          <Radar
            name="Stats"
            dataKey="value"
            stroke="var(--primary)"
            fill="var(--primary)"
            fillOpacity={0.6}
          />
          <Tooltip
            contentStyle={{
              background: 'var(--bg-elevated)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '8px'
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>

    {/* Game-by-Game Trends */}
    <div className="section" style={{ padding: '24px' }}>
      <h3 style={{
        fontSize: '18px',
        fontWeight: '600',
        color: 'var(--text-primary)',
        marginBottom: '20px'
      }}>
        Recent Performance Trend
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={trendData}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
          <XAxis
            dataKey="game"
            tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
            label={{ value: 'Game Number', position: 'insideBottom', offset: -5 }}
          />
          <YAxis tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
          <Tooltip
            contentStyle={{
              background: 'var(--bg-elevated)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '8px'
            }}
            labelFormatter={(value) => `Game ${value}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="pts"
            stroke="var(--primary)"
            strokeWidth={2}
            name="Points"
            dot={{ fill: 'var(--primary)', r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="reb"
            stroke="var(--success)"
            strokeWidth={2}
            name="Rebounds"
            dot={{ fill: 'var(--success)', r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="ast"
            stroke="var(--warning)"
            strokeWidth={2}
            name="Assists"
            dot={{ fill: 'var(--warning)', r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>

    {/* Shooting Breakdown */}
    {seasonAverages && (
      <div className="section" style={{ padding: '24px' }}>
        <h3 style={{
          fontSize: '18px',
          fontWeight: '600',
          color: 'var(--text-primary)',
          marginBottom: '20px'
        }}>
          Shooting Percentages
        </h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={[
            { name: 'FG%', value: parseFloat(seasonAverages.field_goal_pct || 0) },
            { name: '3P%', value: parseFloat(seasonAverages.three_point_pct || 0) },
            { name: 'FT%', value: parseFloat(seasonAverages.free_throw_pct || 0) }
          ]}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
            <XAxis
              dataKey="name"
              tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
            />
            <YAxis
              domain={[0, 100]}
              tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
              label={{ value: 'Percentage', angle: -90, position: 'insideLeft' }}
            />
            <Tooltip
              contentStyle={{
                background: 'var(--bg-elevated)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '8px'
              }}
              formatter={(value) => `${value}%`}
            />
            <Bar dataKey="value" fill="var(--primary)" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    )}
  </div>
);

const StatCard = ({ label, value, color }) => (
  <div style={{
    padding: '16px',
    background: 'var(--bg-elevated)',
    borderRadius: 'var(--radius-sm)',
    border: `1px solid ${color}20`,
    textAlign: 'center'
  }}>
    <div style={{
      fontSize: '24px',
      fontWeight: '700',
      color: color,
      marginBottom: '4px'
    }}>
      {value || '0.0'}
    </div>
    <div style={{
      fontSize: '12px',
      fontWeight: '600',
      color: 'var(--text-secondary)',
      textTransform: 'uppercase',
      letterSpacing: '0.05em'
    }}>
      {label}
    </div>
  </div>
);

const tableHeaderStyle = {
  padding: '12px 16px',
  textAlign: 'left',
  fontSize: '12px',
  fontWeight: '600',
  color: 'var(--text-secondary)',
  textTransform: 'uppercase',
  letterSpacing: '0.05em'
};

const tableCellStyle = {
  padding: '12px 16px',
  fontSize: '14px',
  color: 'var(--text-primary)'
};

export default PlayerDetail;
