import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const StatsChart = ({ data }) => {
    const chartData = [
        { name: 'Team Str', value: data.team_strength, color: '#A855F7' },      // Secondary (Stellar Purple)
        { name: 'Opp Str', value: data.opponent_strength, color: '#00D9FF' },   // Primary (Electric Cyan)
        { name: 'Home Adv', value: data.home_advantage * 50, color: '#00FF88' }, // Success (Neon Green)
    ];

    return (
        <div className="card" style={{ padding: '28px' }}>
            <h3 style={{
                fontSize: '12px',
                color: 'var(--text-secondary)',
                marginBottom: '24px',
                textAlign: 'center',
                textTransform: 'uppercase',
                letterSpacing: '2px',
                fontWeight: '600'
            }}>Matchup Analysis</h3>
            <div style={{ height: '240px', width: '100%' }}>
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                        <XAxis
                            dataKey="name"
                            stroke="#A0A0A0"
                            fontSize={12}
                            tickLine={false}
                            axisLine={false}
                        />
                        <YAxis hide />
                        <Tooltip
                            cursor={{ fill: 'rgba(255,255,255,0.03)' }}
                            contentStyle={{
                                backgroundColor: '#141414',
                                border: '1px solid #252525',
                                borderRadius: '12px',
                                boxShadow: '0 4px 16px rgba(0, 0, 0, 0.5)'
                            }}
                            labelStyle={{ color: '#FFFFFF' }}
                            itemStyle={{ color: '#A0A0A0' }}
                        />
                        <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                            {chartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default StatsChart;
