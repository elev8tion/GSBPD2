import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, RefreshCw } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const BettingInsights = () => {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBettingInsights();
  }, []);

  const fetchBettingInsights = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE}/nba/betting-insights`);
      setInsights(response.data.insights || []);
    } catch (err) {
      console.error('Error fetching betting insights:', err);
      setError('Failed to load betting insights');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  };

  const getOddsColor = (odds) => {
    if (!odds) return 'text-slate-400';
    if (odds < 1.5) return 'text-green-400';  // Heavy favorite
    if (odds < 2.0) return 'text-blue-400';   // Moderate favorite
    return 'text-orange-400';                  // Underdog
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
        <div className="max-w-7xl mx-auto flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
        <div className="max-w-7xl mx-auto flex items-center justify-center py-20">
          <div className="text-red-400">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Betting Insights</h1>
            <p className="text-slate-400">AI-powered analysis from DraftKings lines</p>
          </div>
          <button
            onClick={fetchBettingInsights}
            className="flex items-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          >
            <RefreshCw size={18} />
            Refresh
          </button>
        </div>
      </div>

      {/* Insights Grid */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6">
        {insights.map((insight) => (
          <div
            key={insight.game_id}
            className="bg-slate-800 border border-slate-700 rounded-xl p-6 hover:border-blue-500 transition-all"
          >
            {/* Game Header */}
            <div className="mb-4">
              <h3 className="text-xl font-bold text-white mb-1">
                {insight.matchup}
              </h3>
              <p className="text-sm text-slate-400">
                {formatTime(insight.commence_time)}
              </p>
            </div>

            {/* Team Stats Comparison */}
            {insight.team_stats?.home && insight.team_stats?.away && (
              <div className="bg-slate-700/50 rounded-lg p-4 mb-4">
                <div className="text-xs text-slate-400 uppercase mb-3 font-semibold">Team Stats (Season Avg)</div>
                <div className="grid grid-cols-3 gap-3">
                  {/* Points Per Game */}
                  <div>
                    <div className="text-xs text-slate-500 text-center mb-1">PPG</div>
                    <div className="flex justify-between items-center">
                      <span className={`text-sm font-semibold ${
                        parseFloat(insight.team_stats.home.pts) > parseFloat(insight.team_stats.away.pts)
                          ? 'text-green-400' : 'text-slate-400'
                      }`}>
                        {insight.team_stats.home.pts}
                      </span>
                      <span className="text-xs text-slate-600 mx-1">vs</span>
                      <span className={`text-sm font-semibold ${
                        parseFloat(insight.team_stats.away.pts) > parseFloat(insight.team_stats.home.pts)
                          ? 'text-green-400' : 'text-slate-400'
                      }`}>
                        {insight.team_stats.away.pts}
                      </span>
                    </div>
                  </div>

                  {/* Rebounds Per Game */}
                  <div>
                    <div className="text-xs text-slate-500 text-center mb-1">RPG</div>
                    <div className="flex justify-between items-center">
                      <span className={`text-sm font-semibold ${
                        parseFloat(insight.team_stats.home.reb) > parseFloat(insight.team_stats.away.reb)
                          ? 'text-green-400' : 'text-slate-400'
                      }`}>
                        {insight.team_stats.home.reb}
                      </span>
                      <span className="text-xs text-slate-600 mx-1">vs</span>
                      <span className={`text-sm font-semibold ${
                        parseFloat(insight.team_stats.away.reb) > parseFloat(insight.team_stats.home.reb)
                          ? 'text-green-400' : 'text-slate-400'
                      }`}>
                        {insight.team_stats.away.reb}
                      </span>
                    </div>
                  </div>

                  {/* Assists Per Game */}
                  <div>
                    <div className="text-xs text-slate-500 text-center mb-1">APG</div>
                    <div className="flex justify-between items-center">
                      <span className={`text-sm font-semibold ${
                        parseFloat(insight.team_stats.home.ast) > parseFloat(insight.team_stats.away.ast)
                          ? 'text-green-400' : 'text-slate-400'
                      }`}>
                        {insight.team_stats.home.ast}
                      </span>
                      <span className="text-xs text-slate-600 mx-1">vs</span>
                      <span className={`text-sm font-semibold ${
                        parseFloat(insight.team_stats.away.ast) > parseFloat(insight.team_stats.home.ast)
                          ? 'text-green-400' : 'text-slate-400'
                      }`}>
                        {insight.team_stats.away.ast}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Betting Lines */}
            <div className="grid grid-cols-2 gap-4 mb-4">
              {/* Spread */}
              <div className="bg-slate-700/50 rounded-lg p-3">
                <div className="text-xs text-slate-500 uppercase mb-1">Spread</div>
                <div className="text-xl font-bold text-white">
                  {insight.spread > 0 ? '+' : ''}{insight.spread}
                </div>
                <div className="text-xs text-slate-400 mt-1">
                  Favorite: {insight.favorite}
                </div>
              </div>

              {/* Total */}
              <div className="bg-slate-700/50 rounded-lg p-3">
                <div className="text-xs text-slate-500 uppercase mb-1">Total (O/U)</div>
                <div className="text-xl font-bold text-white">
                  {insight.total}
                </div>
                <div className="text-xs text-slate-400 mt-1 flex justify-between">
                  <span>O: {insight.betting_analysis.over_odds}</span>
                  <span>U: {insight.betting_analysis.under_odds}</span>
                </div>
              </div>
            </div>

            {/* Implied Probabilities */}
            {insight.implied_probabilities.home && (
              <div className="bg-slate-700/50 rounded-lg p-3 mb-4">
                <div className="text-xs text-slate-500 uppercase mb-2 font-semibold">Implied Probabilities</div>
                <div className="flex justify-between items-center">
                  <div>
                    <div className="text-sm text-slate-400">Home</div>
                    <div className={`text-lg font-semibold ${getOddsColor(insight.implied_probabilities.home / 100)}`}>
                      {insight.implied_probabilities.home}%
                    </div>
                  </div>
                  <div className="text-slate-600">vs</div>
                  <div className="text-right">
                    <div className="text-sm text-slate-400">Away</div>
                    <div className={`text-lg font-semibold ${getOddsColor(insight.implied_probabilities.away / 100)}`}>
                      {insight.implied_probabilities.away}%
                    </div>
                  </div>
                </div>
                {insight.betting_analysis.market_efficiency && (
                  <div className="mt-2 pt-2 border-t border-slate-700">
                    <div className="text-xs text-slate-500">
                      Market Efficiency: {insight.betting_analysis.market_efficiency}%
                      <span className="ml-2 text-slate-600">(includes vig)</span>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Key Players */}
            {insight.top_players?.home && insight.top_players?.away && (
              <div className="bg-slate-700/50 rounded-lg p-4 mb-4">
                <div className="text-xs text-slate-400 uppercase mb-3 font-semibold">Top Scorers</div>
                <div className="grid grid-cols-2 gap-4">
                  {/* Home Team Players */}
                  <div>
                    <div className="text-xs text-slate-500 mb-2">Home</div>
                    <div className="space-y-2">
                      {insight.top_players.home.slice(0, 3).map((player, idx) => (
                        <div key={idx} className="flex justify-between items-center">
                          <span className="text-sm text-white truncate mr-2">
                            {player.name}
                          </span>
                          <span className="text-sm font-semibold text-blue-400">
                            {player.ppg} PPG
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Away Team Players */}
                  <div>
                    <div className="text-xs text-slate-500 mb-2">Away</div>
                    <div className="space-y-2">
                      {insight.top_players.away.slice(0, 3).map((player, idx) => (
                        <div key={idx} className="flex justify-between items-center">
                          <span className="text-sm text-white truncate mr-2">
                            {player.name}
                          </span>
                          <span className="text-sm font-semibold text-orange-400">
                            {player.ppg} PPG
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Recommendation */}
            <div className="bg-blue-600/10 border border-blue-500/30 rounded-lg p-4">
              <div className="text-xs text-blue-400 uppercase mb-2 font-semibold">AI Analysis</div>
              <div className="text-sm text-white leading-relaxed">
                {insight.recommendation}
              </div>
            </div>
          </div>
        ))}
      </div>

      {insights.length === 0 && (
        <div className="max-w-7xl mx-auto text-center py-20">
          <p className="text-slate-400 text-lg">No betting insights available</p>
        </div>
      )}

      {/* Disclaimer */}
      <div className="max-w-7xl mx-auto mt-8 bg-yellow-900/20 border border-yellow-900/50 rounded-lg p-4 text-center">
        <p className="text-sm text-yellow-400">
          ⚠️ For entertainment purposes only. Bet responsibly. Never wager more than you can afford to lose.
        </p>
      </div>
    </div>
  );
};

export default BettingInsights;
