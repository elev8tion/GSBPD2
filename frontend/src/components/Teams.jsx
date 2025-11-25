import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, TrendingUp, TrendingDown, Users, BarChart3 } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedConference, setSelectedConference] = useState('All');
  const [selectedDivision, setSelectedDivision] = useState('All');
  const [selectedSport, setSelectedSport] = useState('NBA');

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

  const filteredTeams = teams.filter(team => {
    const matchesSearch = team.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesConference = selectedConference === 'All' || team.conference === selectedConference;
    const matchesDivision = selectedDivision === 'All' || team.division === selectedDivision;
    return matchesSearch && matchesConference && matchesDivision;
  });

  const nbaDivisions = ['All', 'Atlantic', 'Central', 'Southeast', 'Northwest', 'Pacific', 'Southwest'];
  const nflDivisions = ['All', 'AFC East', 'AFC North', 'AFC South', 'AFC West', 'NFC East', 'NFC North', 'NFC South', 'NFC West'];
  const divisions = selectedSport === 'NBA' ? nbaDivisions : nflDivisions;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">{selectedSport} Teams</h1>
        <p className="text-slate-400">Browse all {selectedSport === 'NBA' ? '30 NBA' : '32 NFL'} teams with live stats and profiles</p>
      </div>

      {/* Filters */}
      <div className="max-w-7xl mx-auto mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Sport Selector */}
        <select
          value={selectedSport}
          onChange={(e) => setSelectedSport(e.target.value)}
          className="px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 font-semibold"
        >
          <option value="NBA">🏀 NBA</option>
          <option value="NFL">🏈 NFL</option>
        </select>
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
          <input
            type="text"
            placeholder="Search teams..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Conference Filter */}
        <select
          value={selectedConference}
          onChange={(e) => setSelectedConference(e.target.value)}
          className="px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="All">All Conferences</option>
          <option value="Eastern">Eastern Conference</option>
          <option value="Western">Western Conference</option>
        </select>

        {/* Division Filter */}
        <select
          value={selectedDivision}
          onChange={(e) => setSelectedDivision(e.target.value)}
          className="px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {divisions.map(div => (
            <option key={div} value={div}>{div === 'All' ? 'All Divisions' : `${div} Division`}</option>
          ))}
        </select>
      </div>

      {/* Teams Grid */}
      {loading ? (
        <div className="max-w-7xl mx-auto flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTeams.map((team) => (
            <TeamCard key={team.team_id} team={team} />
          ))}
        </div>
      )}

      {filteredTeams.length === 0 && !loading && (
        <div className="max-w-7xl mx-auto text-center py-20">
          <p className="text-slate-400 text-lg">No teams found matching your filters</p>
        </div>
      )}
    </div>
  );
};

const TeamCard = ({ team }) => {
  const winPercentage = ((team.wins / (team.wins + team.losses)) * 100).toFixed(1);
  const isWinning = team.wins > team.losses;

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 hover:border-blue-500 transition-all cursor-pointer group">
      {/* Team Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-xl font-bold text-white mb-1 group-hover:text-blue-400 transition-colors">
            {team.name}
          </h3>
          <p className="text-slate-400 text-sm">{team.division} • {team.conference}</p>
        </div>
        <div className={`px-3 py-1 rounded-full text-sm font-semibold ${
          isWinning ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
        }`}>
          {team.wins}-{team.losses}
        </div>
      </div>

      {/* Win Percentage */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-slate-400 text-sm">Win %</span>
          <span className="text-white font-semibold">{winPercentage}%</span>
        </div>
        <div className="w-full bg-slate-700 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all ${
              winPercentage >= 60 ? 'bg-green-500' :
              winPercentage >= 50 ? 'bg-yellow-500' :
              'bg-red-500'
            }`}
            style={{ width: `${winPercentage}%` }}
          ></div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <StatItem
          icon={<BarChart3 size={16} />}
          label="PPG"
          value={team.ppg ? team.ppg.toFixed(1) : '0.0'}
        />
        <StatItem
          icon={<TrendingDown size={16} />}
          label="OPPG"
          value={team.oppg ? team.oppg.toFixed(1) : '0.0'}
        />
        <StatItem
          icon={<Users size={16} />}
          label="RPG"
          value={team.rpg ? team.rpg.toFixed(1) : '0.0'}
        />
        <StatItem
          icon={<TrendingUp size={16} />}
          label="APG"
          value={team.apg ? team.apg.toFixed(1) : '0.0'}
        />
      </div>

      {/* View Profile Button */}
      <button className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors">
        View Profile
      </button>
    </div>
  );
};

const StatItem = ({ icon, label, value }) => (
  <div className="flex items-center space-x-2 bg-slate-700/50 rounded-lg p-2">
    <div className="text-slate-400">{icon}</div>
    <div className="flex-1">
      <p className="text-slate-400 text-xs">{label}</p>
      <p className="text-white font-semibold">{value}</p>
    </div>
  </div>
);

export default Teams;
