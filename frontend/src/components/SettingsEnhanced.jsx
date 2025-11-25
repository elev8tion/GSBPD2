import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Settings as SettingsIcon, Bell, Lock, Database, Palette, User, Shield, TrendingUp, DollarSign, Save } from 'lucide-react';
import { useSport } from '../contexts/SportContext';

const SettingsEnhanced = () => {
  const { selectedSport } = useSport();
  const [activeSection, setActiveSection] = useState('general');
  const [settings, setSettings] = useState({
    // General
    defaultSport: selectedSport,
    autoRefresh: true,
    refreshInterval: 30,

    // Notifications
    enableNotifications: true,
    predictionAlerts: true,
    portfolioUpdates: true,
    emailNotifications: false,

    // Betting
    defaultStake: 100,
    maxStake: 500,
    riskLevel: 'medium',
    autoTrackBets: true,

    // Model
    modelConfidenceThreshold: 0.65,
    useEnsemble: true,
    explainabilityMode: 'detailed',

    // Privacy
    shareAnalytics: false,
    dataRetention: 90
  });

  const [saved, setSaved] = useState(false);

  const sections = [
    { id: 'general', label: 'General', icon: <SettingsIcon size={18} /> },
    { id: 'notifications', label: 'Notifications', icon: <Bell size={18} /> },
    { id: 'betting', label: 'Betting Preferences', icon: <DollarSign size={18} /> },
    { id: 'model', label: 'Model Settings', icon: <TrendingUp size={18} /> },
    { id: 'privacy', label: 'Privacy & Data', icon: <Shield size={18} /> }
  ];

  const handleSave = () => {
    // In production, this would save to backend
    console.log('Saving settings:', settings);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const updateSetting = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

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
              Settings
            </h2>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', margin: 0 }}>
              Configure your preferences and account settings
            </p>
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleSave}
            style={{
              padding: '10px 20px',
              background: 'var(--primary)',
              border: 'none',
              borderRadius: '8px',
              color: 'white',
              fontSize: '14px',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.15s ease',
              fontFamily: 'inherit',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <Save size={16} />
            Save Changes
          </motion.button>
        </div>
      </motion.div>

      {/* Success Message */}
      {saved && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          style={{
            padding: '12px 16px',
            background: 'rgba(0, 255, 136, 0.1)',
            border: '1px solid var(--success)',
            borderRadius: '8px',
            color: 'var(--success)',
            marginBottom: '24px',
            fontSize: '14px',
            fontWeight: '600',
            textAlign: 'center'
          }}
        >
          ✓ Settings saved successfully!
        </motion.div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '240px 1fr', gap: '24px' }}>
        {/* Sidebar Navigation */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}
        >
          {sections.map(section => (
            <motion.button
              key={section.id}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setActiveSection(section.id)}
              style={{
                padding: '12px 16px',
                background: activeSection === section.id ? 'var(--bg-card)' : 'transparent',
                border: `1px solid ${activeSection === section.id ? 'var(--border-subtle)' : 'transparent'}`,
                borderRadius: '8px',
                color: activeSection === section.id ? 'var(--text-primary)' : 'var(--text-secondary)',
                fontSize: '14px',
                fontWeight: '500',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                fontFamily: 'inherit',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                textAlign: 'left'
              }}
            >
              <div style={{ display: 'flex', color: activeSection === section.id ? 'var(--primary)' : 'var(--text-tertiary)' }}>
                {section.icon}
              </div>
              {section.label}
            </motion.button>
          ))}
        </motion.div>

        {/* Settings Content */}
        <motion.div
          key={activeSection}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          {activeSection === 'general' && (
            <GeneralSettings settings={settings} updateSetting={updateSetting} />
          )}
          {activeSection === 'notifications' && (
            <NotificationSettings settings={settings} updateSetting={updateSetting} />
          )}
          {activeSection === 'betting' && (
            <BettingSettings settings={settings} updateSetting={updateSetting} />
          )}
          {activeSection === 'model' && (
            <ModelSettings settings={settings} updateSetting={updateSetting} />
          )}
          {activeSection === 'privacy' && (
            <PrivacySettings settings={settings} updateSetting={updateSetting} />
          )}
        </motion.div>
      </div>
    </div>
  );
};

const GeneralSettings = ({ settings, updateSetting }) => (
  <div className="section" style={{ padding: '24px' }}>
    <h3 style={{
      fontSize: '18px',
      fontWeight: '600',
      color: 'var(--text-primary)',
      margin: '0 0 20px 0',
      letterSpacing: '-0.02em'
    }}>
      General Settings
    </h3>

    <SettingRow
      label="Default Sport"
      description="Choose your preferred sport for the dashboard"
    >
      <select
        value={settings.defaultSport}
        onChange={(e) => updateSetting('defaultSport', e.target.value)}
        className="input-field"
        style={{ width: '200px' }}
      >
        <option value="NBA">NBA</option>
        <option value="NFL">NFL</option>
      </select>
    </SettingRow>

    <SettingRow
      label="Auto Refresh"
      description="Automatically refresh data at regular intervals"
    >
      <ToggleSwitch
        checked={settings.autoRefresh}
        onChange={(checked) => updateSetting('autoRefresh', checked)}
      />
    </SettingRow>

    {settings.autoRefresh && (
      <SettingRow
        label="Refresh Interval"
        description="How often to refresh data (in seconds)"
      >
        <input
          type="number"
          value={settings.refreshInterval}
          onChange={(e) => updateSetting('refreshInterval', parseInt(e.target.value))}
          className="input-field"
          style={{ width: '120px' }}
          min="10"
          max="300"
        />
      </SettingRow>
    )}
  </div>
);

const NotificationSettings = ({ settings, updateSetting }) => (
  <div className="section" style={{ padding: '24px' }}>
    <h3 style={{
      fontSize: '18px',
      fontWeight: '600',
      color: 'var(--text-primary)',
      margin: '0 0 20px 0',
      letterSpacing: '-0.02em'
    }}>
      Notification Preferences
    </h3>

    <SettingRow
      label="Enable Notifications"
      description="Receive notifications about important events"
    >
      <ToggleSwitch
        checked={settings.enableNotifications}
        onChange={(checked) => updateSetting('enableNotifications', checked)}
      />
    </SettingRow>

    <SettingRow
      label="Prediction Alerts"
      description="Get notified when new predictions are available"
    >
      <ToggleSwitch
        checked={settings.predictionAlerts}
        onChange={(checked) => updateSetting('predictionAlerts', checked)}
        disabled={!settings.enableNotifications}
      />
    </SettingRow>

    <SettingRow
      label="Portfolio Updates"
      description="Notifications when bets are resolved"
    >
      <ToggleSwitch
        checked={settings.portfolioUpdates}
        onChange={(checked) => updateSetting('portfolioUpdates', checked)}
        disabled={!settings.enableNotifications}
      />
    </SettingRow>

    <SettingRow
      label="Email Notifications"
      description="Receive important updates via email"
    >
      <ToggleSwitch
        checked={settings.emailNotifications}
        onChange={(checked) => updateSetting('emailNotifications', checked)}
      />
    </SettingRow>
  </div>
);

const BettingSettings = ({ settings, updateSetting }) => (
  <div className="section" style={{ padding: '24px' }}>
    <h3 style={{
      fontSize: '18px',
      fontWeight: '600',
      color: 'var(--text-primary)',
      margin: '0 0 20px 0',
      letterSpacing: '-0.02em'
    }}>
      Betting Preferences
    </h3>

    <SettingRow
      label="Default Stake"
      description="Your standard bet amount ($)"
    >
      <input
        type="number"
        value={settings.defaultStake}
        onChange={(e) => updateSetting('defaultStake', parseFloat(e.target.value))}
        className="input-field"
        style={{ width: '150px' }}
        min="1"
      />
    </SettingRow>

    <SettingRow
      label="Maximum Stake"
      description="Maximum allowed bet amount ($)"
    >
      <input
        type="number"
        value={settings.maxStake}
        onChange={(e) => updateSetting('maxStake', parseFloat(e.target.value))}
        className="input-field"
        style={{ width: '150px' }}
        min="1"
      />
    </SettingRow>

    <SettingRow
      label="Risk Level"
      description="Your preferred betting risk level"
    >
      <select
        value={settings.riskLevel}
        onChange={(e) => updateSetting('riskLevel', e.target.value)}
        className="input-field"
        style={{ width: '200px' }}
      >
        <option value="low">Conservative</option>
        <option value="medium">Moderate</option>
        <option value="high">Aggressive</option>
      </select>
    </SettingRow>

    <SettingRow
      label="Auto-Track Bets"
      description="Automatically add predictions to your portfolio"
    >
      <ToggleSwitch
        checked={settings.autoTrackBets}
        onChange={(checked) => updateSetting('autoTrackBets', checked)}
      />
    </SettingRow>
  </div>
);

const ModelSettings = ({ settings, updateSetting }) => (
  <div className="section" style={{ padding: '24px' }}>
    <h3 style={{
      fontSize: '18px',
      fontWeight: '600',
      color: 'var(--text-primary)',
      margin: '0 0 20px 0',
      letterSpacing: '-0.02em'
    }}>
      Model Configuration
    </h3>

    <SettingRow
      label="Confidence Threshold"
      description="Minimum confidence level for predictions (0-1)"
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <input
          type="range"
          value={settings.modelConfidenceThreshold}
          onChange={(e) => updateSetting('modelConfidenceThreshold', parseFloat(e.target.value))}
          min="0.5"
          max="0.95"
          step="0.05"
          style={{ flex: 1, maxWidth: '200px' }}
        />
        <span style={{ fontSize: '14px', fontWeight: '600', color: 'var(--text-primary)', minWidth: '40px' }}>
          {(settings.modelConfidenceThreshold * 100).toFixed(0)}%
        </span>
      </div>
    </SettingRow>

    <SettingRow
      label="Use Ensemble Model"
      description="Combine multiple models for better accuracy"
    >
      <ToggleSwitch
        checked={settings.useEnsemble}
        onChange={(checked) => updateSetting('useEnsemble', checked)}
      />
    </SettingRow>

    <SettingRow
      label="Explainability Mode"
      description="Level of detail in prediction explanations"
    >
      <select
        value={settings.explainabilityMode}
        onChange={(e) => updateSetting('explainabilityMode', e.target.value)}
        className="input-field"
        style={{ width: '200px' }}
      >
        <option value="simple">Simple</option>
        <option value="detailed">Detailed</option>
        <option value="expert">Expert</option>
      </select>
    </SettingRow>
  </div>
);

const PrivacySettings = ({ settings, updateSetting }) => (
  <div className="section" style={{ padding: '24px' }}>
    <h3 style={{
      fontSize: '18px',
      fontWeight: '600',
      color: 'var(--text-primary)',
      margin: '0 0 20px 0',
      letterSpacing: '-0.02em'
    }}>
      Privacy & Data
    </h3>

    <SettingRow
      label="Share Analytics"
      description="Help improve predictions by sharing anonymous usage data"
    >
      <ToggleSwitch
        checked={settings.shareAnalytics}
        onChange={(checked) => updateSetting('shareAnalytics', checked)}
      />
    </SettingRow>

    <SettingRow
      label="Data Retention"
      description="How long to keep historical data (days)"
    >
      <select
        value={settings.dataRetention}
        onChange={(e) => updateSetting('dataRetention', parseInt(e.target.value))}
        className="input-field"
        style={{ width: '200px' }}
      >
        <option value="30">30 days</option>
        <option value="90">90 days</option>
        <option value="180">6 months</option>
        <option value="365">1 year</option>
        <option value="-1">Forever</option>
      </select>
    </SettingRow>

    <div style={{
      marginTop: '24px',
      padding: '16px',
      background: 'rgba(255, 200, 0, 0.1)',
      border: '1px solid var(--warning)',
      borderRadius: '8px'
    }}>
      <p style={{ fontSize: '13px', color: 'var(--text-secondary)', margin: 0, lineHeight: '1.6' }}>
        <strong style={{ color: 'var(--warning)' }}>Note:</strong> Your betting data and predictions are stored securely and never shared with third parties. You can export or delete your data at any time.
      </p>
    </div>
  </div>
);

const SettingRow = ({ label, description, children }) => (
  <div style={{
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '20px 0',
    borderBottom: '1px solid var(--border-subtle)',
    gap: '20px'
  }}>
    <div style={{ flex: 1 }}>
      <div style={{
        fontSize: '14px',
        fontWeight: '600',
        color: 'var(--text-primary)',
        marginBottom: '4px'
      }}>
        {label}
      </div>
      <div style={{
        fontSize: '13px',
        color: 'var(--text-secondary)',
        lineHeight: '1.4'
      }}>
        {description}
      </div>
    </div>
    <div>{children}</div>
  </div>
);

const ToggleSwitch = ({ checked, onChange, disabled = false }) => (
  <motion.button
    whileTap={{ scale: disabled ? 1 : 0.95 }}
    onClick={() => !disabled && onChange(!checked)}
    disabled={disabled}
    style={{
      width: '48px',
      height: '28px',
      background: checked ? 'var(--primary)' : 'var(--bg-elevated)',
      border: `2px solid ${checked ? 'var(--primary)' : 'var(--border-subtle)'}`,
      borderRadius: '14px',
      cursor: disabled ? 'not-allowed' : 'pointer',
      position: 'relative',
      transition: 'all 0.2s ease',
      opacity: disabled ? 0.4 : 1
    }}
  >
    <motion.div
      animate={{ x: checked ? 20 : 0 }}
      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
      style={{
        width: '20px',
        height: '20px',
        background: 'white',
        borderRadius: '50%',
        position: 'absolute',
        top: '2px',
        left: '2px'
      }}
    />
  </motion.button>
);

export default SettingsEnhanced;
