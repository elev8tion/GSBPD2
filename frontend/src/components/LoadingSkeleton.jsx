import React from 'react';
import { motion } from 'framer-motion';

// Shimmer animation keyframes
const shimmerAnimation = {
  animate: {
    backgroundPosition: ['200% 0', '-200% 0'],
  },
  transition: {
    duration: 2,
    repeat: Infinity,
    ease: 'linear',
  }
};

// Base skeleton with shimmer effect
const SkeletonBase = ({ width = '100%', height = '20px', borderRadius = '8px', style = {} }) => (
  <motion.div
    {...shimmerAnimation}
    style={{
      width,
      height,
      borderRadius,
      background: 'linear-gradient(90deg, var(--bg-elevated) 25%, var(--bg-card) 50%, var(--bg-elevated) 75%)',
      backgroundSize: '200% 100%',
      ...style
    }}
  />
);

// Card skeleton with header and body
export const CardSkeleton = () => (
  <div style={{
    background: 'var(--bg-card)',
    border: '1px solid var(--border-subtle)',
    borderRadius: 'var(--radius-md)',
    padding: '20px'
  }}>
    {/* Header */}
    <div style={{ marginBottom: '16px' }}>
      <SkeletonBase width="40%" height="24px" />
    </div>

    {/* Body */}
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <SkeletonBase width="100%" height="16px" />
      <SkeletonBase width="90%" height="16px" />
      <SkeletonBase width="80%" height="16px" />
    </div>
  </div>
);

// Table row skeleton
export const TableRowSkeleton = ({ columns = 4 }) => (
  <tr>
    {Array.from({ length: columns }).map((_, index) => (
      <td key={index} style={{ padding: '12px' }}>
        <SkeletonBase height="16px" />
      </td>
    ))}
  </tr>
);

// Player card skeleton
export const PlayerCardSkeleton = () => (
  <div style={{
    background: 'var(--bg-card)',
    border: '1px solid var(--border-subtle)',
    borderRadius: 'var(--radius-md)',
    padding: '16px'
  }}>
    {/* Name */}
    <div style={{ marginBottom: '12px' }}>
      <SkeletonBase width="70%" height="20px" />
    </div>

    {/* Position & Team */}
    <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
      <SkeletonBase width="60px" height="16px" borderRadius="12px" />
      <SkeletonBase width="80px" height="16px" borderRadius="12px" />
    </div>

    {/* Stats */}
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '8px' }}>
      <div>
        <SkeletonBase width="100%" height="24px" style={{ marginBottom: '4px' }} />
        <SkeletonBase width="60%" height="12px" />
      </div>
      <div>
        <SkeletonBase width="100%" height="24px" style={{ marginBottom: '4px' }} />
        <SkeletonBase width="60%" height="12px" />
      </div>
      <div>
        <SkeletonBase width="100%" height="24px" style={{ marginBottom: '4px' }} />
        <SkeletonBase width="60%" height="12px" />
      </div>
    </div>
  </div>
);

// Team card skeleton
export const TeamCardSkeleton = () => (
  <div style={{
    background: 'var(--bg-card)',
    border: '1px solid var(--border-subtle)',
    borderRadius: 'var(--radius-md)',
    padding: '20px'
  }}>
    {/* Team name */}
    <div style={{ marginBottom: '16px' }}>
      <SkeletonBase width="60%" height="22px" />
    </div>

    {/* Conference/Division */}
    <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
      <SkeletonBase width="70px" height="16px" borderRadius="12px" />
      <SkeletonBase width="90px" height="16px" borderRadius="12px" />
    </div>

    {/* Stats grid */}
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
      <div>
        <SkeletonBase width="100%" height="28px" style={{ marginBottom: '4px' }} />
        <SkeletonBase width="70%" height="14px" />
      </div>
      <div>
        <SkeletonBase width="100%" height="28px" style={{ marginBottom: '4px' }} />
        <SkeletonBase width="70%" height="14px" />
      </div>
    </div>
  </div>
);

// Stats grid skeleton
export const StatsGridSkeleton = ({ rows = 3, cols = 3 }) => (
  <div style={{
    display: 'grid',
    gridTemplateColumns: `repeat(${cols}, 1fr)`,
    gap: '16px'
  }}>
    {Array.from({ length: rows * cols }).map((_, index) => (
      <div key={index} style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-md)',
        padding: '16px',
        textAlign: 'center'
      }}>
        <SkeletonBase width="80%" height="32px" style={{ margin: '0 auto 8px' }} />
        <SkeletonBase width="60%" height="14px" style={{ margin: '0 auto' }} />
      </div>
    ))}
  </div>
);

// Schedule game skeleton
export const ScheduleGameSkeleton = () => (
  <div style={{
    background: 'var(--bg-card)',
    border: '1px solid var(--border-subtle)',
    borderRadius: 'var(--radius-md)',
    padding: '16px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  }}>
    <div style={{ flex: 1 }}>
      <SkeletonBase width="70%" height="18px" style={{ marginBottom: '8px' }} />
      <SkeletonBase width="50%" height="14px" />
    </div>
    <div style={{ flex: 1, textAlign: 'center' }}>
      <SkeletonBase width="80px" height="24px" style={{ margin: '0 auto' }} />
    </div>
    <div style={{ flex: 1, textAlign: 'right' }}>
      <SkeletonBase width="70%" height="18px" style={{ marginBottom: '8px', marginLeft: 'auto' }} />
      <SkeletonBase width="50%" height="14px" style={{ marginLeft: 'auto' }} />
    </div>
  </div>
);

// List skeleton (multiple items)
export const ListSkeleton = ({ count = 5, type = 'card' }) => {
  const SkeletonComponent = {
    card: CardSkeleton,
    player: PlayerCardSkeleton,
    team: TeamCardSkeleton,
    game: ScheduleGameSkeleton
  }[type] || CardSkeleton;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {Array.from({ length: count }).map((_, index) => (
        <SkeletonComponent key={index} />
      ))}
    </div>
  );
};

// Grid skeleton (for cards layout)
export const GridSkeleton = ({ count = 6, columns = 3, type = 'player' }) => {
  const SkeletonComponent = {
    player: PlayerCardSkeleton,
    team: TeamCardSkeleton,
    card: CardSkeleton
  }[type] || PlayerCardSkeleton;

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: `repeat(auto-fill, minmax(300px, 1fr))`,
      gap: '16px'
    }}>
      {Array.from({ length: count }).map((_, index) => (
        <SkeletonComponent key={index} />
      ))}
    </div>
  );
};

export default SkeletonBase;
