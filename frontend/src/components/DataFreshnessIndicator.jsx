import React from 'react';
import { Circle } from 'lucide-react';

const DataFreshnessIndicator = ({ lastUpdated }) => {
  if (!lastUpdated) {
    return null;
  }

  const now = Date.now();
  const lastUpdatedTime = new Date(lastUpdated).getTime();
  const minutesAgo = Math.floor((now - lastUpdatedTime) / (1000 * 60));
  const hoursAgo = Math.floor(minutesAgo / 60);

  // Determine freshness level
  let status = 'stale';
  let color = 'var(--danger)';
  let label = 'Stale';

  if (minutesAgo < 5) {
    status = 'live';
    color = 'var(--success)';
    label = 'Live';
  } else if (minutesAgo < 60) {
    status = 'fresh';
    color = 'var(--warning)';
    label = `${minutesAgo}m ago`;
  } else if (hoursAgo < 24) {
    status = 'aging';
    color = '#FF9500'; // Orange
    label = `${hoursAgo}h ago`;
  } else {
    const daysAgo = Math.floor(hoursAgo / 24);
    label = `${daysAgo}d ago`;
  }

  return (
    <div style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: '6px',
      padding: '6px 12px',
      background: 'var(--bg-elevated)',
      border: `1px solid ${color}20`,
      borderRadius: 'var(--radius-sm)',
      fontSize: '12px',
      fontWeight: '500'
    }}>
      <Circle
        size={8}
        fill={color}
        stroke={color}
        style={{
          animation: status === 'live' ? 'pulse 2s infinite' : 'none'
        }}
      />
      <span style={{ color: 'var(--text-secondary)' }}>
        {label}
      </span>

      {/* Add pulse animation to CSS if not already present */}
      <style>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.5;
          }
        }
      `}</style>
    </div>
  );
};

export default DataFreshnessIndicator;
