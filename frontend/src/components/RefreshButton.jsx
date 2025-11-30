import React from 'react';
import { motion } from 'framer-motion';
import { RefreshCw } from 'lucide-react';

const RefreshButton = ({ onRefresh, loading = false, lastRefresh = null, size = 'md' }) => {
  const sizes = {
    sm: { padding: '6px 12px', fontSize: '13px', iconSize: 14 },
    md: { padding: '8px 16px', fontSize: '14px', iconSize: 16 },
    lg: { padding: '10px 20px', fontSize: '15px', iconSize: 18 }
  };

  const currentSize = sizes[size] || sizes.md;

  const formatLastRefresh = () => {
    if (!lastRefresh) return 'Never refreshed';

    const now = Date.now();
    const lastRefreshTime = new Date(lastRefresh).getTime();
    const seconds = Math.floor((now - lastRefreshTime) / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);

    if (seconds < 60) {
      return `Refreshed ${seconds}s ago`;
    } else if (minutes < 60) {
      return `Refreshed ${minutes}m ago`;
    } else if (hours < 24) {
      return `Refreshed ${hours}h ago`;
    } else {
      return `Refreshed ${Math.floor(hours / 24)}d ago`;
    }
  };

  return (
    <motion.button
      whileHover={{ scale: loading ? 1 : 1.05 }}
      whileTap={{ scale: loading ? 1 : 0.95 }}
      onClick={onRefresh}
      disabled={loading}
      title={formatLastRefresh()}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '8px',
        padding: currentSize.padding,
        background: loading ? 'var(--bg-card)' : 'var(--primary)',
        border: `1px solid ${loading ? 'var(--border-subtle)' : 'transparent'}`,
        borderRadius: 'var(--radius-sm)',
        color: loading ? 'var(--text-secondary)' : 'white',
        fontSize: currentSize.fontSize,
        fontWeight: '600',
        cursor: loading ? 'not-allowed' : 'pointer',
        transition: 'all 0.2s ease',
        opacity: loading ? 0.6 : 1
      }}
    >
      <motion.div
        animate={{ rotate: loading ? 360 : 0 }}
        transition={{
          duration: 1,
          repeat: loading ? Infinity : 0,
          ease: 'linear'
        }}
        style={{ display: 'flex', alignItems: 'center' }}
      >
        <RefreshCw size={currentSize.iconSize} />
      </motion.div>
      <span>{loading ? 'Refreshing...' : 'Refresh'}</span>
    </motion.button>
  );
};

export default RefreshButton;
