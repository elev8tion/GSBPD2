import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';

const ExplainabilityChart = ({ shapValues }) => {
    if (!shapValues || Object.keys(shapValues).length === 0) return null;

    const data = Object.entries(shapValues).map(([feature, value]) => ({
        feature: feature.replace('_', ' ').toUpperCase(),
        value: value,
        color: value > 0 ? '#00FF88' : '#FF3E9D'  // New success and danger colors
    })).sort((a, b) => Math.abs(b.value) - Math.abs(a.value));

    return (
        <div className="card" style={{ padding: '28px' }}>
            <h3 style={{
                fontSize: '12px',
                color: 'var(--text-secondary)',
                marginBottom: '24px',
                textTransform: 'uppercase',
                letterSpacing: '2px',
                fontWeight: '600'
            }}>Why this prediction? (AI Logic)</h3>
            <div style={{ height: '280px', width: '100%' }}>
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data} layout="vertical" margin={{ left: 40 }}>
                        <XAxis type="number" hide />
                        <YAxis
                            dataKey="feature"
                            type="category"
                            stroke="#A0A0A0"
                            fontSize={11}
                            width={120}
                            tickLine={false}
                            axisLine={false}
                        />
                        <Tooltip
                            cursor={{ fill: 'rgba(255,255,255,0.03)' }}
                            contentStyle={{
                                backgroundColor: '#141414',
                                border: '1px solid #252525',
                                borderRadius: '12px',
                                boxShadow: '0 4px 16px rgba(0, 0, 0, 0.5)'
                            }}
                            formatter={(value) => [value.toFixed(4), "Impact"]}
                            labelStyle={{ color: '#FFFFFF' }}
                            itemStyle={{ color: '#A0A0A0' }}
                        />
                        <ReferenceLine x={0} stroke="#2F2F2F" strokeWidth={2} />
                        <Bar dataKey="value" radius={[0, 8, 8, 0]}>
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
            <p style={{
                fontSize: '12px',
                textAlign: 'center',
                color: 'var(--text-tertiary)',
                marginTop: '16px',
                lineHeight: '1.5'
            }}>
                <span style={{ color: 'var(--success)' }}>Green bars</span> push the prediction higher (Positive Spread), <span style={{ color: 'var(--danger)' }}>Pink bars</span> push it lower.
            </p>
        </div>
    );
};

export default ExplainabilityChart;
