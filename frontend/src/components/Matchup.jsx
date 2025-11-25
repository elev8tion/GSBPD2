import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, TrendingUp, TrendingDown, Users, BarChart3, Target, Shield, Zap, Activity, Flame } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend } from 'recharts';

const Matchup = () => {
  const { matchupId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  // Mock data - would come from API in production
  const matchup = {
    homeTeam: {
      name: 'Los Angeles Lakers',
      wins: 12,
      losses: 5,
      ppg: 116.4,
      oppg: 110.2,
      rpg: 45.8,
      apg: 27.3,
      fgPct: 47.2,
      threePtPct: 36.8,
      ftPct: 78.5,
      last5: ['W', 'W', 'L', 'W', 'W'],
      streak: 'W3'
    },
    awayTeam: {
      name: 'Boston Celtics',
      wins: 14,
      losses: 3,
      ppg: 119.8,
      oppg: 107.5,
      rpg: 46.2,
      apg: 28.9,
      fgPct: 48.5,
      threePtPct: 38.2,
      ftPct: 81.3,
      last5: ['W', 'W', 'W', 'L', 'W'],
      streak: 'W2'
    },
    gameInfo: {
      date: '2025-11-30',
      time: '7:30 PM ET',
      venue: 'Crypto.com Arena',
      series: 'LAL leads 1-0',
      lastMeeting: 'LAL 115, BOS 112 (Nov 10)'
    },
    prediction: {
      favorite: 'Boston Celtics',
      spread: -3.5,
      confidence: 68
    }
  };

  const { homeTeam, awayTeam } = matchup;

  // Comparison data
  const comparisonData = [
    { stat: 'PPG', home: homeTeam.ppg, away: awayTeam.ppg },
    { stat: 'OPPG', home: homeTeam.oppg, away: awayTeam.oppg },
    { stat: 'RPG', home: homeTeam.rpg, away: awayTeam.rpg },
    { stat: 'APG', home: homeTeam.apg, away: awayTeam.apg },
  ];

  // Shooting percentages
  const shootingData = [
    { stat: 'FG%', home: homeTeam.fgPct, away: awayTeam.fgPct },
    { stat: '3PT%', home: homeTeam.threePtPct, away: awayTeam.threePtPct },
    { stat: 'FT%', home: homeTeam.ftPct, away: awayTeam.ftPct },
  ];

  // Radar chart
  const radarData = [
    {
      stat: 'Offense',
      home: Math.min((homeTeam.ppg / 120) * 100, 100),
      away: Math.min((awayTeam.ppg / 120) * 100, 100)
    },
    {
      stat: 'Defense',
      home: Math.min(((120 - homeTeam.oppg) / 120) * 100, 100),
      away: Math.min(((120 - awayTeam.oppg) / 120) * 100, 100)
    },
    {
      stat: 'Rebounds',
      home: Math.min((homeTeam.rpg / 50) * 100, 100),
      away: Math.min((awayTeam.rpg / 50) * 100, 100)
    },
    {
      stat: 'Assists',
      home: Math.min((homeTeam.apg / 30) * 100, 100),
      away: Math.min((awayTeam.apg / 30) * 100, 100)
    },
    {
      stat: 'Win%',
      home: (homeTeam.wins / (homeTeam.wins + homeTeam.losses)) * 100,
      away: (awayTeam.wins / (awayTeam.wins + awayTeam.losses)) * 100
    }
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
        className="section"
        style={{ marginBottom: '24px', padding: '28px' }}
      >
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '20px',
          flexWrap: 'wrap'
        }}>
          {/* Away Team */}
          <div style={{ flex: 1, textAlign: 'left' }}>
            <h2 style={{
              fontSize: '24px',
              fontWeight: '700',
              color: 'var(--text-primary)',
              margin: '0 0 8px 0',
              letterSpacing: '-0.03em'
            }}>
              {awayTeam.name}
            </h2>
            <div className="badge success" style={{ fontSize: '13px' }}>
              {awayTeam.wins}-{awayTeam.losses}
            </div>
            <div style={{
              marginTop: '12px',
              fontSize: '13px',
              color: 'var(--text-secondary)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}>
              <Flame size={14} />
              {awayTeam.streak}
            </div>
          </div>

          {/* VS */}
          <div style={{
            padding: '16px 24px',
            background: 'var(--bg-elevated)',
            borderRadius: '12px',
            border: '1px solid var(--border-subtle)'
          }}>
            <div style={{
              fontSize: '28px',
              fontWeight: '700',
              color: 'var(--text-primary)',
              textAlign: 'center',
              letterSpacing: '-0.02em'
            }}>
              VS
            </div>
            <div style={{
              fontSize: '11px',
              color: 'var(--text-tertiary)',
              textAlign: 'center',
              marginTop: '8px',
              textTransform: 'uppercase',
              fontWeight: '600',
              letterSpacing: '0.5px'
            }}>
              {matchup.gameInfo.date}
            </div>
            <div style={{
              fontSize: '12px',
              color: 'var(--text-secondary)',
              textAlign: 'center',
              marginTop: '4px'
            }}>
              {matchup.gameInfo.time}
            </div>
          </div>

          {/* Home Team */}
          <div style={{ flex: 1, textAlign: 'right' }}>
            <h2 style={{
              fontSize: '24px',
              fontWeight: '700',
              color: 'var(--text-primary)',
              margin: '0 0 8px 0',
              letterSpacing: '-0.03em'
            }}>
              {homeTeam.name}
            </h2>
            <div className="badge success" style={{ fontSize: '13px' }}>
              {homeTeam.wins}-{homeTeam.losses}
            </div>
            <div style={{
              marginTop: '12px',
              fontSize: '13px',
              color: 'var(--text-secondary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-end',
              gap: '6px'
            }}>
              <Flame size={14} />
              {homeTeam.streak}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Prediction */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="section"
        style={{
          marginBottom: '24px',
          padding: '24px',
          background: 'linear-gradient(135deg, rgba(0, 217, 255, 0.05), rgba(99, 102, 241, 0.05))',
          border: '1px solid var(--primary)'
        }}
      >
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '20px',
          flexWrap: 'wrap'
        }}>
          <div>
            <div style={{
              fontSize: '12px',
              color: 'var(--text-secondary)',
              fontWeight: '600',
              marginBottom: '8px',
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>
              AI Prediction
            </div>
            <div style={{
              fontSize: '20px',
              fontWeight: '700',
              color: 'var(--primary)',
              letterSpacing: '-0.02em'
            }}>
              {matchup.prediction.favorite} {matchup.prediction.spread > 0 ? '+' : ''}{matchup.prediction.spread}
            </div>
          </div>
          <div style={{
            padding: '12px 20px',
            background: 'var(--bg-card)',
            borderRadius: '8px',
            border: '1px solid var(--border-subtle)'
          }}>
            <div style={{
              fontSize: '11px',
              color: 'var(--text-tertiary)',
              marginBottom: '4px',
              textTransform: 'uppercase',
              fontWeight: '600',
              letterSpacing: '0.5px'
            }}>
              Confidence
            </div>
            <div style={{
              fontSize: '24px',
              fontWeight: '700',
              color: 'var(--text-primary)'
            }}>
              {matchup.prediction.confidence}%
            </div>
          </div>
        </div>
      </motion.div>

      {/* Stats Comparison */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
          gap: '24px',
          marginBottom: '24px'
        }}
      >
        {/* Bar Chart */}
        <div className="section" style={{ padding: '24px' }}>
          <h3 style={{
            fontSize: '16px',
            fontWeight: '600',
            color: 'var(--text-primary)',
            margin: '0 0 20px 0',
            letterSpacing: '-0.02em'
          }}>
            Team Stats Comparison
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={comparisonData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" />
              <XAxis dataKey="stat" tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
              <YAxis tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} />
              <Tooltip
                contentStyle={{
                  background: 'var(--bg-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '8px',
                  fontSize: '12px'
                }}
              />
              <Legend />
              <Bar dataKey="away" fill="#6366f1" name={awayTeam.name} radius={[4, 4, 0, 0]} />
              <Bar dataKey="home" fill="var(--primary)" name={homeTeam.name} radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Radar Chart */}
        <div className="section" style={{ padding: '24px' }}>
          <h3 style={{
            fontSize: '16px',
            fontWeight: '600',
            color: 'var(--text-primary)',
            margin: '0 0 20px 0',
            letterSpacing: '-0.02em'
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
              <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: 'var(--text-tertiary)', fontSize: 10 }} />
              <Radar
                name={awayTeam.name}
                dataKey="away"
                stroke="#6366f1"
                fill="#6366f1"
                fillOpacity={0.3}
              />
              <Radar
                name={homeTeam.name}
                dataKey="home"
                stroke="var(--primary)"
                fill="var(--primary)"
                fillOpacity={0.3}
              />
              <Legend />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* Shooting Stats */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="section"
        style={{ marginBottom: '24px', padding: '24px' }}
      >
        <h3 style={{
          fontSize: '16px',
          fontWeight: '600',
          color: 'var(--text-primary)',
          margin: '0 0 20px 0',
          letterSpacing: '-0.02em'
        }}>
          Shooting Percentages
        </h3>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '20px'
        }}>
          {shootingData.map((item, index) => (
            <ComparisonStat
              key={index}
              label={item.stat}
              awayValue={item.away}
              homeValue={item.home}
              awayTeam={awayTeam.name}
              homeTeam={homeTeam.name}
            />
          ))}
        </div>
      </motion.div>

      {/* Recent Form */}
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
          Last 5 Games
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <FormStreak team={awayTeam.name} results={awayTeam.last5} />
          <FormStreak team={homeTeam.name} results={homeTeam.last5} />
        </div>
      </motion.div>
    </div>
  );
};

const ComparisonStat = ({ label, awayValue, homeValue, awayTeam, homeTeam }) => {
  const awayBetter = awayValue > homeValue;
  const homeBetter = homeValue > awayValue;

  return (
    <div>
      <div style={{
        fontSize: '13px',
        fontWeight: '600',
        color: 'var(--text-secondary)',
        marginBottom: '12px',
        textAlign: 'center'
      }}>
        {label}
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          padding: '12px 16px',
          background: awayBetter ? 'rgba(0, 255, 136, 0.05)' : 'var(--bg-elevated)',
          borderRadius: '8px',
          border: `1px solid ${awayBetter ? 'var(--success)' : 'transparent'}`
        }}>
          <span style={{
            fontSize: '13px',
            color: 'var(--text-secondary)',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap'
          }}>
            {awayTeam}
          </span>
          <span style={{
            fontSize: '15px',
            fontWeight: '700',
            color: awayBetter ? 'var(--success)' : 'var(--text-primary)'
          }}>
            {awayValue}%
          </span>
        </div>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          padding: '12px 16px',
          background: homeBetter ? 'rgba(0, 255, 136, 0.05)' : 'var(--bg-elevated)',
          borderRadius: '8px',
          border: `1px solid ${homeBetter ? 'var(--success)' : 'transparent'}`
        }}>
          <span style={{
            fontSize: '13px',
            color: 'var(--text-secondary)',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap'
          }}>
            {homeTeam}
          </span>
          <span style={{
            fontSize: '15px',
            fontWeight: '700',
            color: homeBetter ? 'var(--success)' : 'var(--text-primary)'
          }}>
            {homeValue}%
          </span>
        </div>
      </div>
    </div>
  );
};

const FormStreak = ({ team, results }) => (
  <div>
    <div style={{
      fontSize: '14px',
      fontWeight: '600',
      color: 'var(--text-primary)',
      marginBottom: '12px'
    }}>
      {team}
    </div>
    <div style={{ display: 'flex', gap: '8px' }}>
      {results.map((result, index) => (
        <div
          key={index}
          className={`badge ${result === 'W' ? 'success' : 'danger'}`}
          style={{
            flex: 1,
            padding: '12px',
            fontSize: '14px',
            fontWeight: '700',
            textAlign: 'center'
          }}
        >
          {result}
        </div>
      ))}
    </div>
  </div>
);

export default Matchup;
