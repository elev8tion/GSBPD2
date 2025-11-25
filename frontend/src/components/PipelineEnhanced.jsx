import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { GitMerge, Database, CheckCircle, XCircle, Clock, RefreshCw, TrendingUp, Activity, BarChart3, AlertCircle } from 'lucide-react';
import { useSport } from '../contexts/SportContext';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const PipelineEnhanced = () => {
  const { selectedSport } = useSport();
  const [pipelineStatus, setPipelineStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchPipelineStatus();
  }, [selectedSport]);

  const fetchPipelineStatus = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/pipeline/status`);
      setPipelineStatus(response.data);
    } catch (error) {
      console.error('Failed to fetch pipeline status:', error);
      // Use mock data for now
      setPipelineStatus(generateMockPipelineStatus());
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchPipelineStatus();
    setTimeout(() => setRefreshing(false), 1000);
  };

  const generateMockPipelineStatus = () => ({
    lastUpdate: new Date().toISOString(),
    stages: [
      {
        id: 'data-collection',
        name: 'Data Collection',
        status: 'success',
        duration: '2.4s',
        items: {
          'Team Stats': 'success',
          'Player Stats': 'success',
          'Game Results': 'success',
          'Injury Reports': 'warning'
        }
      },
      {
        id: 'data-processing',
        name: 'Data Processing',
        status: 'success',
        duration: '5.1s',
        items: {
          'Data Cleaning': 'success',
          'Feature Engineering': 'success',
          'Normalization': 'success'
        }
      },
      {
        id: 'model-training',
        name: 'Model Training',
        status: 'success',
        duration: '12.8s',
        items: {
          'XGBoost Model': 'success',
          'Neural Network': 'success',
          'Ensemble': 'success'
        }
      },
      {
        id: 'validation',
        name: 'Validation',
        status: 'success',
        duration: '3.2s',
        items: {
          'Cross-Validation': 'success',
          'Backtesting': 'success',
          'Performance Metrics': 'success'
        }
      }
    ],
    metrics: {
      totalRecords: 15420,
      processed: 15420,
      accuracy: 72.5,
      latency: 23.5
    }
  });

  const status = pipelineStatus || generateMockPipelineStatus();

  return (
    <div>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ marginBottom: '32px' }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <h2 style={{
              fontSize: '24px',
              fontWeight: '600',
              color: 'var(--text-primary)',
              marginBottom: '6px',
              letterSpacing: '-0.03em'
            }}>
              Data Pipeline
            </h2>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', margin: 0 }}>
              {selectedSport} data processing • Last updated: {new Date(status.lastUpdate).toLocaleString()}
            </p>
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleRefresh}
            disabled={refreshing}
            style={{
              padding: '10px 18px',
              background: 'var(--primary)',
              border: 'none',
              borderRadius: '8px',
              color: 'white',
              fontSize: '13px',
              fontWeight: '600',
              cursor: refreshing ? 'not-allowed' : 'pointer',
              transition: 'all 0.15s ease',
              fontFamily: 'inherit',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              opacity: refreshing ? 0.6 : 1
            }}
          >
            <RefreshCw size={16} style={{ animation: refreshing ? 'spin 1s linear infinite' : 'none' }} />
            {refreshing ? 'Refreshing...' : 'Refresh Status'}
          </motion.button>
        </div>
      </motion.div>

      {/* Metrics Dashboard */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '16px',
          marginBottom: '32px'
        }}
      >
        <MetricCard
          icon={<Database size={20} />}
          label="Total Records"
          value={status.metrics.totalRecords.toLocaleString()}
          color="var(--primary)"
        />
        <MetricCard
          icon={<CheckCircle size={20} />}
          label="Processed"
          value={status.metrics.processed.toLocaleString()}
          color="var(--success)"
        />
        <MetricCard
          icon={<TrendingUp size={20} />}
          label="Model Accuracy"
          value={`${status.metrics.accuracy.toFixed(1)}%`}
          color="var(--success)"
        />
        <MetricCard
          icon={<Activity size={20} />}
          label="Avg Latency"
          value={`${status.metrics.latency.toFixed(1)}ms`}
          color="var(--info)"
        />
      </motion.div>

      {/* Pipeline Stages */}
      {loading ? (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '400px'
        }}>
          <div className="loading-spinner"></div>
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.15 }}
          style={{ display: 'grid', gap: '20px' }}
        >
          {status.stages.map((stage, index) => (
            <StageCard key={stage.id} stage={stage} index={index} />
          ))}
        </motion.div>
      )}
    </div>
  );
};

const MetricCard = ({ icon, label, value, color }) => (
  <div className="metric-card">
    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
      <div style={{
        color,
        background: `${color}15`,
        padding: '8px',
        borderRadius: '8px',
        display: 'flex'
      }}>
        {icon}
      </div>
      <span className="metric-label" style={{ margin: 0 }}>{label}</span>
    </div>
    <div className="metric-value" style={{ color }}>{value}</div>
  </div>
);

const StageCard = ({ stage, index }) => {
  const statusConfig = {
    success: { color: 'var(--success)', icon: <CheckCircle size={18} />, label: 'SUCCESS' },
    warning: { color: 'var(--warning)', icon: <AlertCircle size={18} />, label: 'WARNING' },
    error: { color: 'var(--danger)', icon: <XCircle size={18} />, label: 'ERROR' },
    running: { color: 'var(--info)', icon: <Clock size={18} />, label: 'RUNNING' }
  };

  const config = statusConfig[stage.status] || statusConfig.success;

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.05 }}
      className="section"
      style={{
        padding: '24px',
        borderLeft: `4px solid ${config.color}`
      }}
    >
      {/* Stage Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ color: config.color, display: 'flex' }}>
            <GitMerge size={24} />
          </div>
          <div>
            <h3 style={{
              fontSize: '16px',
              fontWeight: '600',
              color: 'var(--text-primary)',
              margin: '0 0 4px 0',
              letterSpacing: '-0.02em'
            }}>
              {stage.name}
            </h3>
            <p style={{ fontSize: '12px', color: 'var(--text-tertiary)', margin: 0 }}>
              Duration: {stage.duration}
            </p>
          </div>
        </div>
        <div className="badge" style={{ background: `${config.color}15`, color: config.color, border: 'none' }}>
          {config.icon}
          <span style={{ marginLeft: '6px' }}>{config.label}</span>
        </div>
      </div>

      {/* Stage Items */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
        gap: '12px'
      }}>
        {Object.entries(stage.items).map(([itemName, itemStatus], idx) => (
          <StageItem
            key={itemName}
            name={itemName}
            status={itemStatus}
            index={idx}
          />
        ))}
      </div>
    </motion.div>
  );
};

const StageItem = ({ name, status, index }) => {
  const itemConfig = {
    success: { color: 'var(--success)', icon: <CheckCircle size={14} /> },
    warning: { color: 'var(--warning)', icon: <AlertCircle size={14} /> },
    error: { color: 'var(--danger)', icon: <XCircle size={14} /> },
    running: { color: 'var(--info)', icon: <Clock size={14} /> }
  };

  const config = itemConfig[status] || itemConfig.success;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.02 }}
      style={{
        padding: '12px 14px',
        background: 'var(--bg-elevated)',
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '8px'
      }}
    >
      <span style={{ fontSize: '13px', color: 'var(--text-primary)', fontWeight: '500' }}>
        {name}
      </span>
      <div style={{ color: config.color, display: 'flex', flexShrink: 0 }}>
        {config.icon}
      </div>
    </motion.div>
  );
};

export default PipelineEnhanced;
