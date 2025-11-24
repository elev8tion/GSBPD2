import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const StatsChart = ({ data }) => {
    const chartData = [
        { name: 'Team Str', value: data.team_strength, color: '#8b5cf6' },
        { name: 'Opp Str', value: data.opponent_strength, color: '#06b6d4' },
        { name: 'Home Adv', value: data.home_advantage * 50, color: '#10b981' }, // Scale up for visibility
    ];

    return (
        <div className="h-64 w-full mt-8">
            <h3 className="text-sm text-gray-400 mb-4 text-center uppercase tracking-widest">Matchup Analysis</h3>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                    <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis hide />
                    <Tooltip
                        cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                        contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                    />
                    <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                        {chartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default StatsChart;
