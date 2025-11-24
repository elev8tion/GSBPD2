import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';

const ExplainabilityChart = ({ shapValues }) => {
    if (!shapValues || Object.keys(shapValues).length === 0) return null;

    const data = Object.entries(shapValues).map(([feature, value]) => ({
        feature: feature.replace('_', ' ').toUpperCase(),
        value: value,
        color: value > 0 ? '#10b981' : '#ef4444'
    })).sort((a, b) => Math.abs(b.value) - Math.abs(a.value));

    return (
        <div className="glass-panel p-6 mt-6">
            <h3 className="text-sm text-gray-400 mb-4 uppercase tracking-widest">Why this prediction? (AI Logic)</h3>
            <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data} layout="vertical" margin={{ left: 40 }}>
                        <XAxis type="number" hide />
                        <YAxis
                            dataKey="feature"
                            type="category"
                            stroke="#94a3b8"
                            fontSize={10}
                            width={100}
                            tickLine={false}
                            axisLine={false}
                        />
                        <Tooltip
                            cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                            contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                            formatter={(value) => [value.toFixed(4), "Impact"]}
                        />
                        <ReferenceLine x={0} stroke="#475569" />
                        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
            <p className="text-xs text-center text-gray-500 mt-2">
                Green bars push the prediction higher (Positive Spread), Red bars push it lower.
            </p>
        </div>
    );
};

export default ExplainabilityChart;
