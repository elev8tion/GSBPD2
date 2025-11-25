import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Search, TrendingUp, TrendingDown, BarChart3, Users, ArrowUpDown, ChevronRight } from 'lucide-react';
import { useSport } from '../contexts/SportContext';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const TeamsEnhanced = () => {
  const navigate = useNavigate();
  const { selectedSport } = useSport();
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedConference, setSelectedConference] = useState('All');
  const [selectedDivision, setSelectedDivision] = useState('All');
  const [sortBy, setSortBy] = useState('wins'); // wins, ppg, winPct
  const [sortOrder, setSortOrder] = useState('desc');

  useEffect(() => {
    fetchTeams();
  }, [selectedSport]);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      const endpoint = selectedSport === 'NBA' ? '/nba/teams' : '/nfl/teams';
      const response = await axios.get(`${API_BASE}${endpoint}`);
      setTeams(response.data.teams || []);
    } catch (error) {
      console.error('Error fetching teams:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredTeams = teams
    .filter(team => {
      const matchesSearch = team.name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesConference = selectedConference === 'All' || team.conference === selectedConference;
      const matchesDivision = selectedDivision === 'All' || team.division === selectedDivision;
      return matchesSearch && matchesConference && matchesDivision;
    })
    .sort((a, b) => {
      let aVal, bVal;
      switch (sortBy) {
        case 'wins':
          aVal = a.wins;
          bVal = b.wins;
          break;
        case 'ppg':
          aVal = a.ppg || 0;
          bVal = b.ppg || 0;
          break;
        case 'winPct':
          aVal = a.win_percentage || 0;
          bVal = b.win_percentage || 0;
          break;
        default:
          return 0;
      }
      return sortOrder === 'desc' ? bVal - aVal : aVal - bVal;
    });

  const nbaDivisions = ['All', 'Atlantic', 'Central', 'Southeast', 'Northwest', 'Pacific', 'Southwest'];
  const nflDivisions = ['All', 'AFC East', 'AFC North', 'AFC South', 'AFC West', 'NFC East', 'NFC North', 'NFC South', 'NFC West'];
  const divisions = selectedSport === 'NBA' ? nbaDivisions : nflDivisions;

  const toggleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'desc' ? 'asc' : 'desc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

  return (
    <div style={{ padding: '0' }}>
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
          {selectedSport} Teams
        </h2>
        <p style={{ fontSize: '14px', color: 'var(--text-secondary)', margin: 0 }}>
          {filteredTeams.length} teams • Browse stats, rosters, and matchups
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
            placeholder="Search teams..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-field"
            style={{ paddingLeft: '38px' }}
          />
        </div>

        {/* Conference Filter */}
        <select
          value={selectedConference}
          onChange={(e) => setSelectedConference(e.target.value)}
          className="input-field"
        >
          <option value="All">All Conferences</option>
          <option value="Eastern">Eastern</option>
          <option value="Western">Western</option>
        </select>

        {/* Division Filter */}
        <select
          value={selectedDivision}
          onChange={(e) => setSelectedDivision(e.target.value)}
          className="input-field"
        >
          {divisions.map(div => (
            <option key={div} value={div}>
              {div === 'All' ? 'All Divisions' : div}
            </option>
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
          active={sortBy === 'wins'}
          onClick={() => toggleSort('wins')}
          order={sortBy === 'wins' ? sortOrder : null}
        >
          Wins
        </SortButton>
        <SortButton
          active={sortBy === 'winPct'}
          onClick={() => toggleSort('winPct')}
          order={sortBy === 'winPct' ? sortOrder : null}
        >
          Win %
        </SortButton>
        <SortButton
          active={sortBy === 'ppg'}
          onClick={() => toggleSort('ppg')}
          order={sortBy === 'ppg' ? sortOrder : null}
        >
          Points
        </SortButton>
      </motion.div>

      {/* Teams Grid */}
      {loading ? (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '80px 20px',
          minHeight: '400px'
        }}>
          <div className="loading-spinner"></div>
        </div>
      ) : filteredTeams.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{
            textAlign: 'center',
            padding: '80px 20px',
            background: 'var(--bg-card)',
            border: '1px solid var(--border-subtle)',
            borderRadius: '12px'
          }}
        >
          <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
            No teams found matching your filters
          </p>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: '16px'
          }}
        >
          {filteredTeams.map((team, index) => (
            <TeamCard
              key={team.team_id}
              team={team}
              index={index}
              onClick={() => navigate(`/teams/${team.team_id}`)}
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

const TeamCard = ({ team, index, onClick }) => {
  const winPercentage = ((team.wins / (team.wins + team.losses)) * 100).toFixed(1);
  const isWinning = team.wins > team.losses;

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
        position: 'relative',
        overflow: 'hidden'
      }}
      whileHover={{ y: -4, boxShadow: '0 8px 24px rgba(0, 0, 0, 0.12)' }}
    >
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
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
            {team.name}
          </h3>
          <p style={{
            fontSize: '12px',
            color: 'var(--text-tertiary)',
            margin: 0,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap'
          }}>
            {team.conference} • {team.division}
          </p>
        </div>
        <div className={`badge ${isWinning ? 'success' : 'danger'}`} style={{ marginLeft: '12px' }}>
          {team.wins}-{team.losses}
        </div>
      </div>

      {/* Win Percentage Bar */}
      <div style={{ marginBottom: '16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: '500' }}>Win Rate</span>
          <span style={{ fontSize: '13px', color: 'var(--text-primary)', fontWeight: '600' }}>{winPercentage}%</span>
        </div>
        <div style={{
          width: '100%',
          height: '4px',
          background: 'var(--bg-elevated)',
          borderRadius: '2px',
          overflow: 'hidden'
        }}>
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${winPercentage}%` }}
            transition={{ delay: index * 0.02 + 0.2, duration: 0.6, ease: 'easeOut' }}
            style={{
              height: '100%',
              background: winPercentage >= 60 ? 'var(--success)' : winPercentage >= 50 ? 'var(--warning)' : 'var(--danger)',
              borderRadius: '2px'
            }}
          />
        </div>
      </div>

      {/* Stats Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(2, 1fr)',
        gap: '8px',
        marginBottom: '12px'
      }}>
        <StatItem icon={<BarChart3 size={14} />} label="PPG" value={team.ppg?.toFixed(1) || '0.0'} />
        <StatItem icon={<TrendingDown size={14} />} label="OPPG" value={team.oppg?.toFixed(1) || '0.0'} />
        <StatItem icon={<Users size={14} />} label="RPG" value={team.rpg?.toFixed(1) || '0.0'} />
        <StatItem icon={<TrendingUp size={14} />} label="APG" value={team.apg?.toFixed(1) || '0.0'} />
      </div>

      {/* View Button */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-end',
        gap: '6px',
        color: 'var(--primary)',
        fontSize: '13px',
        fontWeight: '500',
        marginTop: '12px',
        paddingTop: '12px',
        borderTop: '1px solid var(--border-subtle)'
      }}>
        View Details
        <ChevronRight size={16} />
      </div>
    </motion.div>
  );
};

const StatItem = ({ icon, label, value }) => (
  <div style={{
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '8px 10px',
    background: 'var(--bg-elevated)',
    borderRadius: '6px'
  }}>
    <div style={{ color: 'var(--text-tertiary)', display: 'flex' }}>
      {icon}
    </div>
    <div style={{ flex: 1, minWidth: 0 }}>
      <p style={{ fontSize: '10px', color: 'var(--text-tertiary)', margin: '0 0 2px 0', textTransform: 'uppercase', fontWeight: '600', letterSpacing: '0.5px' }}>
        {label}
      </p>
      <p style={{ fontSize: '13px', color: 'var(--text-primary)', margin: 0, fontWeight: '600', overflow: 'hidden', textOverflow: 'ellipsis' }}>
        {value}
      </p>
    </div>
  </div>
);

export default TeamsEnhanced;
