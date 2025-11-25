import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';
import { ArrowLeft, TrendingUp, TrendingDown, Users, BarChart3, Activity, Target, Shield, Zap } from 'lucide-react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const TeamDetail = () => {
  const { teamId } = useParams();
  const navigate = useNavigate();
  const [team, setTeam] = useState(null);
  const [roster, setRoster] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTeamData();
  }, [teamId]);

  const fetchTeamData = async () => {
    try {
      setLoading(true);
      const [teamResponse, rosterResponse] = await Promise.all([
        axios.get(`${API_BASE}/nba/teams/${teamId}`),
        axios.get(`${API_BASE}/nba/teams/${teamId}/roster`).catch(() => ({ data: { players: [] } }))
      ]);

      setTeam(teamResponse.data);
      setRoster(rosterResponse.data.players || []);
    } catch (error) {
      console.error('Error fetching team data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh'
      }}>
        <div className="loading-spinner"></div>
      </div>
    );
  }

  if (!team) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px' }}>
        <p style={{ color: 'var(--text-secondary)' }}>Team not found</p>
        <button
          onClick={() => navigate('/teams')}
          style={{
            marginTop: '20px',
            padding: '10px 20px',
            background: 'var(--primary)',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontFamily: 'inherit'
          }}
        >
          Back to Teams
        </button>
      </div>
    );
  }

  const winPct = ((team.wins / (team.wins + team.losses)) * 100).toFixed(1);
  const isWinning = team.wins > team.losses;

  // Radar chart data
  const radarData = [
    { stat: 'Offense', value: Math.min((team.ppg / 120) * 100, 100) },
    { stat: 'Defense', value: Math.min(((120 - team.oppg) / 120) * 100, 100) },
    { stat: 'Rebounds', value: Math.min((team.rpg / 50) * 100, 100) },
    { stat: 'Assists', value: Math.min((team.apg / 30) * 100, 100) },
    { stat: 'Win Rate', value: parseFloat(winPct) },
  ];

  // Trend data (mock - would come from API in production)
  const trendData = [
    { game: 'G1', ppg: team.ppg - 5 },
    { game: 'G2', ppg: team.ppg - 3 },
    { game: 'G3', ppg: team.ppg - 1 },
    { game: 'G4', ppg: team.ppg + 2 },
    { game: 'G5', ppg: team.ppg },
  ];

  return (
    <div>
      {/* Back Button */}
      <motion.button
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        whileHover={{ x: -4 }}
        onClick={() => navigate(-1)}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '8px 12px',
          background: 'transparent',
          border: '1px solid var(--border-subtle)',
          borderRadius: '8px',
          color: 'var(--text-secondary)',
          fontSize: '13px',
          fontWeight: '500',
          cursor: 'pointer',
          marginBottom: '24px',
          fontFamily: 'inherit',
          transition: 'all 0.15s ease'
        }}
      >
        <ArrowLeft size={16} />
        Back
      </motion.button>

      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ marginBottom: '32px' }}
      >
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '12px', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <h1 style={{
              fontSize: '32px',
              fontWeight: '700',
              color: 'var(--text-primary)',
              margin: '0 0 8px 0',
              letterSpacing: '-0.04em'
            }}>
              {team.name}
            </h1>
            <p style={{
              fontSize: '14px',
              color: 'var(--text-secondary)',
              margin: 0
            }}>
              {team.conference} Conference • {team.division} Division
            </p>
          </div>
          <div className={`badge ${isWinning ? 'success' : 'danger'}`} style={{ padding: '10px 16px', fontSize: '16px' }}>
            {team.wins}-{team.losses}
          </div>
        </div>
      </motion.div>

      {/* Key Metrics */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '16px',
          marginBottom: '32px'
        }}
      >
        <MetricCard
          icon={<Target size={20} />}
          label="Win Percentage"
          value={`${winPct}%`}
          trend={isWinning ? '+12%' : '-8%'}
          trendPositive={isWinning}
        />
        <MetricCard
          icon={<Zap size={20} />}
          label="Points Per Game"
          value={team.ppg?.toFixed(1) || '0.0'}
          trend="+2.4"
          trendPositive={true}
        />
        <MetricCard
          icon={<Shield size={20} />}
          label="Opp. PPG"
          value={team.oppg?.toFixed(1) || '0.0'}
          trend="-1.8"
          trendPositive={true}
        />
        <MetricCard
          icon={<Activity size={20} />}
          label="Point Differential"
          value={((team.ppg - team.oppg) || 0).toFixed(1)}
          trend={team.ppg > team.oppg ? 'Positive' : 'Negative'}
          trendPositive={team.ppg > team.oppg}
        />
      </motion.div>

      {/* Charts Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
          gap: '24px',
          marginBottom: '32px'
        }}
      >
        {/* Radar Chart */}
        <div className="section" style={{ padding: '24px' }}>
          <h3 style={{
            fontSize: '16px',
            fontWeight: '600',
            color: 'var(--text-primary)',
            margin: '0 0 20px 0',
            letterSpacing: '-0.02em'
          }}>
            Team Performance Profile
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="var(--border-subtle)" />
              <PolarAngleAxis
                dataKey="stat"
                tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
              />
              <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: 'var(--text-tertiary)', fontSize: 10 }} />
              <Radar
                name="Stats"
                dataKey="value"
                stroke="var(--primary)"
                fill="var(--primary)"
                fillOpacity={0.3}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Trend Chart */}
        <div className="section" style={{ padding: '24px' }}>
          <h3 style={{
            fontSize: '16px',
            fontWeight: '600',
            color: 'var(--text-primary)',
            margin: '0 0 20px 0',
            letterSpacing: '-0.02em'
          }}>
            Scoring Trend (Last 5 Games)
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={trendData}>
              <defs>
                <linearGradient id="colorPpg" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="var(--primary)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
              <XAxis dataKey="game" tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
              <YAxis tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} domain={[90, 130]} />
              <Tooltip
                contentStyle={{
                  background: 'var(--bg-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '8px',
                  fontSize: '12px'
                }}
              />
              <Area
                type="monotone"
                dataKey="ppg"
                stroke="var(--primary)"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorPpg)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* Detailed Stats */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="section"
        style={{ marginBottom: '32px', padding: '24px' }}
      >
        <h3 style={{
          fontSize: '16px',
          fontWeight: '600',
          color: 'var(--text-primary)',
          margin: '0 0 20px 0',
          letterSpacing: '-0.02em'
        }}>
          Season Statistics
        </h3>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
          gap: '16px'
        }}>
          <StatDetail icon={<BarChart3 size={18} />} label="PPG" value={team.ppg?.toFixed(1) || '0.0'} />
          <StatDetail icon={<Shield size={18} />} label="OPPG" value={team.oppg?.toFixed(1) || '0.0'} />
          <StatDetail icon={<Users size={18} />} label="RPG" value={team.rpg?.toFixed(1) || '0.0'} />
          <StatDetail icon={<TrendingUp size={18} />} label="APG" value={team.apg?.toFixed(1) || '0.0'} />
          <StatDetail icon={<Target size={18} />} label="Wins" value={team.wins} />
          <StatDetail icon={<Activity size={18} />} label="Losses" value={team.losses} />
        </div>
      </motion.div>

      {/* Roster Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="section"
        style={{ padding: '24px' }}
      >
        <h3 style={{
          fontSize: '16px',
          fontWeight: '600',
          color: 'var(--text-primary)',
          margin: '0 0 20px 0',
          letterSpacing: '-0.02em'
        }}>
          Team Roster
        </h3>
        {roster.length === 0 ? (
          <div style={{
            padding: '40px 20px',
            textAlign: 'center',
            background: 'var(--bg-elevated)',
            borderRadius: '8px',
            border: '1px dashed var(--border-subtle)'
          }}>
            <p style={{ color: 'var(--text-tertiary)', margin: 0, fontSize: '14px' }}>
              Player roster data coming soon
            </p>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '12px' }}>
            {roster.map((player, index) => (
              <PlayerRow key={player.player_id || index} player={player} />
            ))}
          </div>
        )}
      </motion.div>
    </div>
  );
};

const MetricCard = ({ icon, label, value, trend, trendPositive }) => (
  <div className="metric-card" style={{ position: 'relative', overflow: 'hidden' }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
      <div style={{
        color: 'var(--primary)',
        background: 'rgba(0, 217, 255, 0.1)',
        padding: '8px',
        borderRadius: '8px',
        display: 'flex'
      }}>
        {icon}
      </div>
      <span className="metric-label" style={{ margin: 0 }}>{label}</span>
    </div>
    <div className="metric-value" style={{ marginBottom: '8px' }}>{value}</div>
    <div className={`metric-trend ${trendPositive ? 'positive' : 'negative'}`}>
      {trendPositive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
      {trend}
    </div>
  </div>
);

const StatDetail = ({ icon, label, value }) => (
  <div style={{
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    padding: '16px',
    background: 'var(--bg-elevated)',
    borderRadius: '8px',
    border: '1px solid var(--border-subtle)'
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
      <div style={{ color: 'var(--text-tertiary)', display: 'flex' }}>
        {icon}
      </div>
      <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: '500' }}>
        {label}
      </span>
    </div>
    <div style={{ fontSize: '20px', fontWeight: '600', color: 'var(--text-primary)' }}>
      {value}
    </div>
  </div>
);

const PlayerRow = ({ player }) => (
  <div style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '12px 16px',
    background: 'var(--bg-elevated)',
    borderRadius: '8px',
    border: '1px solid var(--border-subtle)',
    transition: 'all 0.15s ease',
    cursor: 'pointer'
  }}
  onMouseEnter={(e) => e.currentTarget.style.borderColor = 'var(--primary)'}
  onMouseLeave={(e) => e.currentTarget.style.borderColor = 'var(--border-subtle)'}
  >
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
      <div style={{
        width: '36px',
        height: '36px',
        background: 'var(--bg-card)',
        borderRadius: '50%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '13px',
        fontWeight: '600',
        color: 'var(--text-secondary)'
      }}>
        #{player.jersey_number || '0'}
      </div>
      <div>
        <div style={{ fontSize: '14px', fontWeight: '600', color: 'var(--text-primary)' }}>
          {player.name}
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-tertiary)' }}>
          {player.position}
        </div>
      </div>
    </div>
    {player.ppg > 0 && (
      <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: 'var(--text-secondary)' }}>
        <div>
          <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{player.ppg.toFixed(1)}</span> PPG
        </div>
        <div>
          <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{player.rpg.toFixed(1)}</span> RPG
        </div>
        <div>
          <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{player.apg.toFixed(1)}</span> APG
        </div>
      </div>
    )}
  </div>
);

export default TeamDetail;
