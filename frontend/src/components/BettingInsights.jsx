import { useState, useEffect } from 'react';
import axios from 'axios';

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
    if (!odds) return 'text-gray-400';
    if (odds < 1.5) return 'text-green-400';  // Heavy favorite
    if (odds < 2.0) return 'text-blue-400';   // Moderate favorite
    return 'text-orange-400';                  // Underdog
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-gray-400">Loading betting insights...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-red-400">{error}</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white">Betting Insights</h2>
          <p className="text-gray-400 text-sm mt-1">AI-powered analysis from DraftKings lines</p>
        </div>
        <button
          onClick={fetchBettingInsights}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm"
        >
          Refresh
        </button>
      </div>

      {/* Insights Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {insights.map((insight) => (
          <div
            key={insight.game_id}
            className="bg-[#1a1a1a] border border-gray-800 rounded-lg p-6 hover:border-gray-700 transition-colors"
          >
            {/* Game Header */}
            <div className="mb-4">
              <h3 className="text-lg font-semibold text-white mb-1">
                {insight.matchup}
              </h3>
              <p className="text-sm text-gray-400">
                {formatTime(insight.commence_time)}
              </p>
            </div>

            {/* Betting Lines */}
            <div className="grid grid-cols-2 gap-4 mb-4">
              {/* Spread */}
              <div className="bg-[#0a0a0a] rounded-lg p-3">
                <div className="text-xs text-gray-500 uppercase mb-1">Spread</div>
                <div className="text-xl font-bold text-white">
                  {insight.spread > 0 ? '+' : ''}{insight.spread}
                </div>
                <div className="text-xs text-gray-400 mt-1">
                  Favorite: {insight.favorite}
                </div>
              </div>

              {/* Total */}
              <div className="bg-[#0a0a0a] rounded-lg p-3">
                <div className="text-xs text-gray-500 uppercase mb-1">Total (O/U)</div>
                <div className="text-xl font-bold text-white">
                  {insight.total}
                </div>
                <div className="text-xs text-gray-400 mt-1 flex justify-between">
                  <span>O: {insight.betting_analysis.over_odds}</span>
                  <span>U: {insight.betting_analysis.under_odds}</span>
                </div>
              </div>
            </div>

            {/* Implied Probabilities */}
            {insight.implied_probabilities.home && (
              <div className="bg-[#0a0a0a] rounded-lg p-3 mb-4">
                <div className="text-xs text-gray-500 uppercase mb-2">Implied Probabilities</div>
                <div className="flex justify-between items-center">
                  <div>
                    <div className="text-sm text-gray-400">Home</div>
                    <div className={`text-lg font-semibold ${getOddsColor(insight.implied_probabilities.home / 100)}`}>
                      {insight.implied_probabilities.home}%
                    </div>
                  </div>
                  <div className="text-gray-600">vs</div>
                  <div className="text-right">
                    <div className="text-sm text-gray-400">Away</div>
                    <div className={`text-lg font-semibold ${getOddsColor(insight.implied_probabilities.away / 100)}`}>
                      {insight.implied_probabilities.away}%
                    </div>
                  </div>
                </div>
                {insight.betting_analysis.market_efficiency && (
                  <div className="mt-2 pt-2 border-t border-gray-800">
                    <div className="text-xs text-gray-500">
                      Market Efficiency: {insight.betting_analysis.market_efficiency}%
                      <span className="ml-2 text-gray-600">(includes vig)</span>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Recommendation */}
            <div className="bg-blue-900/20 border border-blue-900/50 rounded-lg p-3">
              <div className="text-xs text-blue-400 uppercase mb-1">Analysis</div>
              <div className="text-sm text-gray-300">
                {insight.recommendation}
              </div>
            </div>
          </div>
        ))}
      </div>

      {insights.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          No betting insights available
        </div>
      )}

      {/* Disclaimer */}
      <div className="bg-yellow-900/20 border border-yellow-900/50 rounded-lg p-4 text-center">
        <p className="text-xs text-yellow-400">
          ⚠️ For entertainment purposes only. Bet responsibly. Never wager more than you can afford to lose.
        </p>
      </div>
    </div>
  );
};

export default BettingInsights;
