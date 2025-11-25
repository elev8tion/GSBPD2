import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, User, TrendingUp, Activity, Trophy } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const Players = () => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPosition, setSelectedPosition] = useState('All');
  const [selectedTeam, setSelectedTeam] = useState('All');
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    fetchPlayers();
    fetchTeams();
  }, []);

  const fetchPlayers = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/nba/players`);
      setPlayers(response.data.players || []);
    } catch (error) {
      console.error('Error fetching players:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTeams = async () => {
    try {
      const response = await axios.get(`${API_BASE}/nba/teams`);
      setTeams(response.data.teams || []);
    } catch (error) {
      console.error('Error fetching teams:', error);
    }
  };

  const filteredPlayers = players.filter(player => {
    const matchesSearch = player.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPosition = selectedPosition === 'All' || player.position.includes(selectedPosition);
    const matchesTeam = selectedTeam === 'All' || player.team_id === selectedTeam;
    return matchesSearch && matchesPosition && matchesTeam;
  });

  const positions = ['All', 'G', 'F', 'C'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">NBA Players</h1>
        <p className="text-slate-400">Browse all NBA players with stats and profiles</p>
      </div>

      {/* Filters */}
      <div className="max-w-7xl mx-auto mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
          <input
            type="text"
            placeholder="Search players..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Position Filter */}
        <select
          value={selectedPosition}
          onChange={(e) => setSelectedPosition(e.target.value)}
          className="px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {positions.map(pos => (
            <option key={pos} value={pos}>
              {pos === 'All' ? 'All Positions' : `Position: ${pos}`}
            </option>
          ))}
        </select>

        {/* Team Filter */}
        <select
          value={selectedTeam}
          onChange={(e) => setSelectedTeam(e.target.value)}
          className="px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="All">All Teams</option>
          {teams.map(team => (
            <option key={team.team_id} value={team.team_id}>{team.name}</option>
          ))}
        </select>
      </div>

      {/* Players Grid */}
      {loading ? (
        <div className="max-w-7xl mx-auto flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredPlayers.map((player) => (
            <PlayerCard key={player.player_id} player={player} />
          ))}
        </div>
      )}

      {filteredPlayers.length === 0 && !loading && (
        <div className="max-w-7xl mx-auto text-center py-20">
          <p className="text-slate-400 text-lg">No players found matching your filters</p>
        </div>
      )}
    </div>
  );
};

const PlayerCard = ({ player }) => {
  const isRookie = player.experience === 'R';

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 hover:border-blue-500 transition-all cursor-pointer group">
      {/* Player Header */}
      <div className="flex items-start space-x-3 mb-3">
        <div className="w-12 h-12 bg-slate-700 rounded-full flex items-center justify-center">
          <User size={24} className="text-slate-400" />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-bold text-white truncate group-hover:text-blue-400 transition-colors">
            {player.name}
          </h3>
          <p className="text-slate-400 text-sm truncate">{player.team_name}</p>
        </div>
        <div className="text-right">
          <div className="text-white font-bold text-lg">#{player.jersey_number}</div>
          <div className="text-slate-400 text-xs">{player.position}</div>
        </div>
      </div>

      {/* Player Info */}
      <div className="grid grid-cols-2 gap-2 mb-3 text-sm">
        <InfoItem label="Height" value={player.height} />
        <InfoItem label="Age" value={player.age} />
        <InfoItem label="Experience" value={isRookie ? 'Rookie' : `${player.experience} yrs`} />
        <InfoItem label="School" value={player.school} truncate />
      </div>

      {/* Stats (if available) */}
      {(player.ppg > 0 || player.rpg > 0 || player.apg > 0) && (
        <div className="grid grid-cols-3 gap-2 mb-3">
          <StatBadge label="PPG" value={player.ppg.toFixed(1)} />
          <StatBadge label="RPG" value={player.rpg.toFixed(1)} />
          <StatBadge label="APG" value={player.apg.toFixed(1)} />
        </div>
      )}

      {/* View Button */}
      <button className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-sm transition-colors">
        View Profile
      </button>
    </div>
  );
};

const InfoItem = ({ label, value, truncate = false }) => (
  <div>
    <p className="text-slate-500 text-xs">{label}</p>
    <p className={`text-white font-medium ${truncate ? 'truncate' : ''}`}>{value}</p>
  </div>
);

const StatBadge = ({ label, value }) => (
  <div className="bg-slate-700/50 rounded-lg p-2 text-center">
    <p className="text-slate-400 text-xs mb-1">{label}</p>
    <p className="text-white font-bold">{value}</p>
  </div>
);

export default Players;
