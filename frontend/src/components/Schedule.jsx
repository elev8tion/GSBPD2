import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Calendar, Clock, MapPin, TrendingUp, Filter, ChevronRight } from 'lucide-react';
import { useSport } from '../contexts/SportContext';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const Schedule = () => {
  const navigate = useNavigate();
  const { selectedSport } = useSport();
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, upcoming, completed
  const [selectedDate, setSelectedDate] = useState('all');

  useEffect(() => {
    fetchSchedule();
  }, [selectedSport]);

  const fetchSchedule = async () => {
    try {
      setLoading(true);
      // Placeholder: In production, this would fetch real schedule data
      // For now, generate mock data
      const mockGames = generateMockGames();
      setGames(mockGames);
    } catch (error) {
      console.error('Error fetching schedule:', error);
    } finally {
      setLoading(false);
    }
  };

  const generateMockGames = () => {
    // Mock data until API is ready
    const teams = [
      'Boston Celtics', 'New York Knicks', 'Brooklyn Nets', 'Philadelphia 76ers',
      'Los Angeles Lakers', 'Golden State Warriors', 'Miami Heat', 'Denver Nuggets'
    ];

    const mockGames = [];
    const today = new Date();

    for (let i = 0; i < 15; i++) {
      const gameDate = new Date(today);
      gameDate.setDate(today.getDate() + i - 5);

      const homeTeam = teams[Math.floor(Math.random() * teams.length)];
      let awayTeam = teams[Math.floor(Math.random() * teams.length)];
      while (awayTeam === homeTeam) {
        awayTeam = teams[Math.floor(Math.random() * teams.length)];
      }

      const isCompleted = i < 5;
      const homeScore = isCompleted ? Math.floor(Math.random() * 40) + 90 : null;
      const awayScore = isCompleted ? Math.floor(Math.random() * 40) + 90 : null;

      mockGames.push({
        id: `game-${i}`,
        homeTeam,
        awayTeam,
        date: gameDate.toISOString(),
        time: '7:30 PM ET',
        venue: `${homeTeam} Arena`,
        status: isCompleted ? 'final' : 'scheduled',
        homeScore,
        awayScore
      });
    }

    return mockGames.sort((a, b) => new Date(a.date) - new Date(b.date));
  };

  const filteredGames = games.filter(game => {
    if (filter === 'upcoming') return game.status === 'scheduled';
    if (filter === 'completed') return game.status === 'final';
    return true;
  });

  const groupGamesByDate = (games) => {
    const grouped = {};
    games.forEach(game => {
      const date = new Date(game.date).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
      if (!grouped[date]) grouped[date] = [];
      grouped[date].push(game);
    });
    return grouped;
  };

  const groupedGames = groupGamesByDate(filteredGames);

  return (
    <div>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ marginBottom: '32px' }}
      >
        <h2 style={{
          fontSize: '24px',
          fontWeight: '600',
          color: 'var(--text-primary)',
          marginBottom: '6px',
          letterSpacing: '-0.03em'
        }}>
          {selectedSport} Schedule & Results
        </h2>
        <p style={{ fontSize: '14px', color: 'var(--text-secondary)', margin: 0 }}>
          Upcoming games and recent results
        </p>
      </motion.div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        style={{
          display: 'flex',
          gap: '12px',
          marginBottom: '24px',
          flexWrap: 'wrap'
        }}
      >
        <FilterButton active={filter === 'all'} onClick={() => setFilter('all')}>
          All Games
        </FilterButton>
        <FilterButton active={filter === 'upcoming'} onClick={() => setFilter('upcoming')}>
          Upcoming
        </FilterButton>
        <FilterButton active={filter === 'completed'} onClick={() => setFilter('completed')}>
          Completed
        </FilterButton>
      </motion.div>

      {/* Games List */}
      {loading ? (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '400px'
        }}>
          <div className="loading-spinner"></div>
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          {Object.entries(groupedGames).map(([date, dateGames], dateIndex) => (
            <div key={date} style={{ marginBottom: '32px' }}>
              <motion.div
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: dateIndex * 0.05 }}
                style={{
                  fontSize: '14px',
                  fontWeight: '600',
                  color: 'var(--text-secondary)',
                  marginBottom: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px'
                }}
              >
                <Calendar size={16} />
                {date}
              </motion.div>
              <div style={{ display: 'grid', gap: '12px' }}>
                {dateGames.map((game, gameIndex) => (
                  <GameCard
                    key={game.id}
                    game={game}
                    index={gameIndex}
                    onClick={() => navigate(`/matchup/${game.id}`)}
                  />
                ))}
              </div>
            </div>
          ))}
        </motion.div>
      )}

      {filteredGames.length === 0 && !loading && (
        <div className="section" style={{
          textAlign: 'center',
          padding: '60px 20px'
        }}>
          <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
            No games found for the selected filter
          </p>
        </div>
      )}
    </div>
  );
};

const FilterButton = ({ children, active, onClick }) => (
  <motion.button
    whileHover={{ scale: 1.02 }}
    whileTap={{ scale: 0.98 }}
    onClick={onClick}
    style={{
      padding: '10px 18px',
      background: active ? 'var(--primary)' : 'var(--bg-card)',
      border: `1px solid ${active ? 'var(--primary)' : 'var(--border-subtle)'}`,
      borderRadius: '8px',
      color: active ? 'white' : 'var(--text-secondary)',
      fontSize: '13px',
      fontWeight: '500',
      cursor: 'pointer',
      transition: 'all 0.15s ease',
      fontFamily: 'inherit'
    }}
  >
    {children}
  </motion.button>
);

const GameCard = ({ game, index, onClick }) => {
  const isCompleted = game.status === 'final';
  const homeWon = isCompleted && game.homeScore > game.awayScore;
  const awayWon = isCompleted && game.awayScore > game.homeScore;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.03 }}
      onClick={onClick}
      className="section"
      style={{
        padding: '20px',
        cursor: 'pointer',
        transition: 'all 0.2s ease'
      }}
      whileHover={{ y: -2, boxShadow: '0 8px 24px rgba(0, 0, 0, 0.12)' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '20px' }}>
        {/* Teams */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {/* Away Team */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '12px 16px',
            background: awayWon ? 'rgba(0, 255, 136, 0.05)' : 'var(--bg-elevated)',
            borderRadius: '8px',
            border: `1px solid ${awayWon ? 'var(--success)' : 'transparent'}`
          }}>
            <div style={{
              fontSize: '15px',
              fontWeight: '600',
              color: 'var(--text-primary)'
            }}>
              {game.awayTeam}
            </div>
            {isCompleted && (
              <div style={{
                fontSize: '20px',
                fontWeight: '700',
                color: awayWon ? 'var(--success)' : 'var(--text-secondary)'
              }}>
                {game.awayScore}
              </div>
            )}
          </div>

          {/* Home Team */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '12px 16px',
            background: homeWon ? 'rgba(0, 255, 136, 0.05)' : 'var(--bg-elevated)',
            borderRadius: '8px',
            border: `1px solid ${homeWon ? 'var(--success)' : 'transparent'}`
          }}>
            <div style={{
              fontSize: '15px',
              fontWeight: '600',
              color: 'var(--text-primary)'
            }}>
              {game.homeTeam}
            </div>
            {isCompleted && (
              <div style={{
                fontSize: '20px',
                fontWeight: '700',
                color: homeWon ? 'var(--success)' : 'var(--text-secondary)'
              }}>
                {game.homeScore}
              </div>
            )}
          </div>
        </div>

        {/* Game Info */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '8px',
          alignItems: 'flex-end',
          minWidth: '140px'
        }}>
          <div className={`badge ${isCompleted ? 'success' : 'info'}`}>
            {isCompleted ? 'FINAL' : game.time}
          </div>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '12px',
            color: 'var(--text-tertiary)'
          }}>
            <MapPin size={12} />
            <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {game.venue}
            </span>
          </div>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            color: 'var(--primary)',
            fontSize: '13px',
            fontWeight: '500',
            marginTop: '4px'
          }}>
            View Details
            <ChevronRight size={14} />
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default Schedule;
