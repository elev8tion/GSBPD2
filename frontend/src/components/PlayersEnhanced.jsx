import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Search, User, TrendingUp, Activity, Trophy, ArrowUpDown, Filter, ChevronRight } from 'lucide-react';
import { useSport } from '../contexts/SportContext';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const PlayersEnhanced = () => {
  const navigate = useNavigate();
  const { selectedSport } = useSport();
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPosition, setSelectedPosition] = useState('All');
  const [selectedTeam, setSelectedTeam] = useState('All');
  const [teams, setTeams] = useState([]);
  const [sortBy, setSortBy] = useState('ppg');
  const [sortOrder, setSortOrder] = useState('desc');

  useEffect(() => {
    fetchPlayers();
    fetchTeams();
  }, [selectedSport]);

  const fetchPlayers = async () => {
    try {
      setLoading(true);
      const endpoint = selectedSport === 'NBA' ? '/nba/players' : '/nfl/players';
      const response = await axios.get(`${API_BASE}${endpoint}`);
      setPlayers(response.data.players || []);
    } catch (error) {
      console.error('Error fetching players:', error);
      setPlayers([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchTeams = async () => {
    try {
      const endpoint = selectedSport === 'NBA' ? '/nba/teams' : '/nfl/teams';
      const response = await axios.get(`${API_BASE}${endpoint}`);
      setTeams(response.data.teams || []);
    } catch (error) {
      console.error('Error fetching teams:', error);
    }
  };

  const filteredPlayers = players
    .filter(player => {
      const matchesSearch = player.name?.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesPosition = selectedPosition === 'All' || player.position?.includes(selectedPosition);
      const matchesTeam = selectedTeam === 'All' || player.team_id === selectedTeam;
      return matchesSearch && matchesPosition && matchesTeam;
    })
    .sort((a, b) => {
      let aVal, bVal;
      switch (sortBy) {
        case 'ppg':
          aVal = a.ppg || 0;
          bVal = b.ppg || 0;
          break;
        case 'rpg':
          aVal = a.rpg || 0;
          bVal = b.rpg || 0;
          break;
        case 'apg':
          aVal = a.apg || 0;
          bVal = b.apg || 0;
          break;
        case 'name':
          return sortOrder === 'desc'
            ? (b.name || '').localeCompare(a.name || '')
            : (a.name || '').localeCompare(b.name || '');
        default:
          return 0;
      }
      return sortOrder === 'desc' ? bVal - aVal : aVal - bVal;
    });

  const positions = selectedSport === 'NBA'
    ? ['All', 'G', 'F', 'C']
    : ['All', 'QB', 'RB', 'WR', 'TE', 'OL', 'DL', 'LB', 'DB', 'K'];

  const toggleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'desc' ? 'asc' : 'desc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

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
          {selectedSport} Players
        </h2>
        <p style={{ fontSize: '14px', color: 'var(--text-secondary)', margin: 0 }}>
          {filteredPlayers.length} players • Browse stats, profiles, and performance metrics
        </p>
      </motion.div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '12px',
          marginBottom: '24px'
        }}
      >
        {/* Search */}
        <div style={{ position: 'relative' }}>
          <Search
            size={16}
            style={{
              position: 'absolute',
              left: '12px',
              top: '50%',
              transform: 'translateY(-50%)',
              color: 'var(--text-tertiary)'
            }}
          />
          <input
            type="text"
            placeholder="Search players..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-field"
            style={{ paddingLeft: '38px' }}
          />
        </div>

        {/* Position Filter */}
        <select
          value={selectedPosition}
          onChange={(e) => setSelectedPosition(e.target.value)}
          className="input-field"
        >
          {positions.map(pos => (
            <option key={pos} value={pos}>
              {pos === 'All' ? 'All Positions' : pos}
            </option>
          ))}
        </select>

        {/* Team Filter */}
        <select
          value={selectedTeam}
          onChange={(e) => setSelectedTeam(e.target.value)}
          className="input-field"
        >
          <option value="All">All Teams</option>
          {teams.map(team => (
            <option key={team.team_id} value={team.team_id}>{team.name}</option>
          ))}
        </select>
      </motion.div>

      {/* Sort Controls */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.15 }}
        style={{
          display: 'flex',
          gap: '8px',
          marginBottom: '20px',
          flexWrap: 'wrap'
        }}
      >
        <SortButton
          active={sortBy === 'name'}
          onClick={() => toggleSort('name')}
          order={sortBy === 'name' ? sortOrder : null}
        >
          Name
        </SortButton>
        <SortButton
          active={sortBy === 'ppg'}
          onClick={() => toggleSort('ppg')}
          order={sortBy === 'ppg' ? sortOrder : null}
        >
          Points
        </SortButton>
        <SortButton
          active={sortBy === 'rpg'}
          onClick={() => toggleSort('rpg')}
          order={sortBy === 'rpg' ? sortOrder : null}
        >
          Rebounds
        </SortButton>
        <SortButton
          active={sortBy === 'apg'}
          onClick={() => toggleSort('apg')}
          order={sortBy === 'apg' ? sortOrder : null}
        >
          Assists
        </SortButton>
      </motion.div>

      {/* Players Grid */}
      {loading ? (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '400px'
        }}>
          <div className="loading-spinner"></div>
        </div>
      ) : filteredPlayers.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="section"
          style={{
            textAlign: 'center',
            padding: '80px 20px'
          }}
        >
          <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
            {players.length === 0
              ? `No ${selectedSport} player data available yet`
              : 'No players found matching your filters'}
          </p>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: '16px'
          }}
        >
          {filteredPlayers.map((player, index) => (
            <PlayerCard
              key={player.player_id || index}
              player={player}
              index={index}
              sport={selectedSport}
              onClick={() => navigate(`/players/${player.player_id}`)}
            />
          ))}
        </motion.div>
      )}
    </div>
  );
};

const SortButton = ({ children, active, onClick, order }) => (
  <motion.button
    whileHover={{ scale: 1.02 }}
    whileTap={{ scale: 0.98 }}
    onClick={onClick}
    style={{
      padding: '8px 14px',
      background: active ? 'var(--bg-elevated)' : 'transparent',
      border: `1px solid ${active ? 'var(--primary)' : 'var(--border-subtle)'}`,
      borderRadius: '8px',
      color: active ? 'var(--primary)' : 'var(--text-secondary)',
      fontSize: '13px',
      fontWeight: '500',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '6px',
      transition: 'all 0.15s ease',
      fontFamily: 'inherit'
    }}
  >
    {children}
    {active && <ArrowUpDown size={14} style={{ opacity: order === 'desc' ? 1 : 0.5 }} />}
  </motion.button>
);

const PlayerCard = ({ player, index, sport, onClick }) => {
  const hasStats = player.ppg > 0 || player.rpg > 0 || player.apg > 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.02 }}
      onClick={onClick}
      className="section"
      style={{
        cursor: 'pointer',
        padding: '20px',
        transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
        position: 'relative'
      }}
      whileHover={{ y: -4, boxShadow: '0 8px 24px rgba(0, 0, 0, 0.12)' }}
    >
      {/* Player Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px', marginBottom: '16px' }}>
        <div style={{
          width: '48px',
          height: '48px',
          background: 'linear-gradient(135deg, var(--primary), var(--success))',
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0
        }}>
          <User size={24} style={{ color: 'white' }} />
        </div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <h3 style={{
            fontSize: '16px',
            fontWeight: '600',
            color: 'var(--text-primary)',
            margin: '0 0 4px 0',
            letterSpacing: '-0.02em',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap'
          }}>
            {player.name || 'Unknown Player'}
          </h3>
          <p style={{
            fontSize: '12px',
            color: 'var(--text-tertiary)',
            margin: 0,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap'
          }}>
            {player.team_name || 'Free Agent'}
          </p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{
            fontSize: '18px',
            fontWeight: '700',
            color: 'var(--text-primary)',
            lineHeight: 1
          }}>
            #{player.jersey_number || '0'}
          </div>
          <div style={{
            fontSize: '11px',
            color: 'var(--text-secondary)',
            marginTop: '4px',
            fontWeight: '600'
          }}>
            {player.position || 'N/A'}
          </div>
        </div>
      </div>

      {/* Player Info */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(2, 1fr)',
        gap: '8px',
        marginBottom: '12px',
        padding: '12px',
        background: 'var(--bg-elevated)',
        borderRadius: '8px',
        border: '1px solid var(--border-subtle)'
      }}>
        <InfoItem label="Height" value={player.height || 'N/A'} />
        <InfoItem label="Age" value={player.age || 'N/A'} />
        <InfoItem label="Experience" value={player.experience === 'R' ? 'Rookie' : `${player.experience || 0} yrs`} />
        <InfoItem label="College" value={player.school || 'N/A'} />
      </div>

      {/* Stats */}
      {hasStats && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '8px',
          marginBottom: '12px'
        }}>
          <StatBadge label="PPG" value={(player.ppg || 0).toFixed(1)} icon={<TrendingUp size={14} />} />
          <StatBadge label="RPG" value={(player.rpg || 0).toFixed(1)} icon={<Activity size={14} />} />
          <StatBadge label="APG" value={(player.apg || 0).toFixed(1)} icon={<Trophy size={14} />} />
        </div>
      )}

      {/* View Button */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-end',
        gap: '6px',
        color: 'var(--primary)',
        fontSize: '13px',
        fontWeight: '500',
        paddingTop: '12px',
        borderTop: '1px solid var(--border-subtle)'
      }}>
        View Profile
        <ChevronRight size={16} />
      </div>
    </motion.div>
  );
};

const InfoItem = ({ label, value }) => (
  <div>
    <p style={{
      fontSize: '10px',
      color: 'var(--text-tertiary)',
      margin: '0 0 4px 0',
      textTransform: 'uppercase',
      fontWeight: '600',
      letterSpacing: '0.5px'
    }}>
      {label}
    </p>
    <p style={{
      fontSize: '13px',
      color: 'var(--text-primary)',
      margin: 0,
      fontWeight: '600',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap'
    }}>
      {value}
    </p>
  </div>
);

const StatBadge = ({ label, value, icon }) => (
  <div style={{
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '10px 8px',
    background: 'var(--bg-elevated)',
    borderRadius: '8px',
    border: '1px solid var(--border-subtle)'
  }}>
    <div style={{ color: 'var(--primary)', marginBottom: '6px' }}>
      {icon}
    </div>
    <p style={{
      fontSize: '10px',
      color: 'var(--text-tertiary)',
      margin: '0 0 4px 0',
      fontWeight: '600'
    }}>
      {label}
    </p>
    <p style={{
      fontSize: '16px',
      color: 'var(--text-primary)',
      margin: 0,
      fontWeight: '700'
    }}>
      {value}
    </p>
  </div>
);

export default PlayersEnhanced;
