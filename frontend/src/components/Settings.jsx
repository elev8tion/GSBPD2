import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Settings as SettingsIcon, DollarSign, Bell, Palette, Key, Save, RefreshCw, Shield } from 'lucide-react';

const Settings = () => {
  const [settings, setSettings] = useState({
    // Sport Preferences
    enabledSports: ['nfl', 'nba'],
    defaultSport: 'nfl',
    favoriteTeams: [],

    // Bankroll Management
    totalBankroll: 1000,
    maxBetPerGame: 50,
    maxBetType: 'fixed', // 'fixed' or 'percentage'
    kellyEnabled: false,
    riskTolerance: 'moderate', // 'conservative', 'moderate', 'aggressive'

    // API Configuration
    oddsApiKey: '',
    openaiApiKey: '',

    // Display Preferences
    theme: 'dark',
    chartType: 'bar',
    oddsFormat: 'american', // 'american' or 'decimal'

    // Notifications
    emailNotifications: false,
    lineMovementAlerts: true,
    betResultNotifications: true
  });

  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Load settings from localStorage
    const savedSettings = localStorage.getItem('gsbpd2_settings');
    if (savedSettings) {
      try {
        setSettings(JSON.parse(savedSettings));
      } catch (error) {
        console.error('Failed to load settings:', error);
      }
    }
  }, []);

  const handleSave = () => {
    setLoading(true);
    try {
      localStorage.setItem('gsbpd2_settings', JSON.stringify(settings));
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (error) {
      console.error('Failed to save settings:', error);
      alert('Failed to save settings');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    if (confirm('Are you sure you want to reset all settings to defaults?')) {
      const defaultSettings = {
        enabledSports: ['nfl', 'nba'],
        defaultSport: 'nfl',
        favoriteTeams: [],
        totalBankroll: 1000,
        maxBetPerGame: 50,
        maxBetType: 'fixed',
        kellyEnabled: false,
        riskTolerance: 'moderate',
        oddsApiKey: '',
        openaiApiKey: '',
        theme: 'dark',
        chartType: 'bar',
        oddsFormat: 'american',
        emailNotifications: false,
        lineMovementAlerts: true,
        betResultNotifications: true
      };
      setSettings(defaultSettings);
      localStorage.setItem('gsbpd2_settings', JSON.stringify(defaultSettings));
    }
  };

  const toggleSport = (sport) => {
    setSettings(prev => ({
      ...prev,
      enabledSports: prev.enabledSports.includes(sport)
        ? prev.enabledSports.filter(s => s !== sport)
        : [...prev.enabledSports, sport]
    }));
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px', maxWidth: '1200px', margin: '0 auto' }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card-elevated"
        style={{ padding: '40px', textAlign: 'center' }}
      >
        <SettingsIcon size={48} style={{ color: 'var(--primary)', marginBottom: '16px' }} />
        <h2 style={{
          fontSize: '32px',
          fontWeight: '700',
          marginBottom: '8px',
          background: 'linear-gradient(135deg, var(--primary), var(--secondary))',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }}>
          Settings & Preferences
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>
          Customize your betting dashboard experience
        </p>
      </motion.div>

      {saved && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          style={{
            padding: '16px 20px',
            background: 'rgba(0, 255, 136, 0.1)',
            border: '1px solid var(--success)',
            borderRadius: 'var(--radius-md)',
            color: 'var(--success)',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            justifyContent: 'center'
          }}
        >
          <Save size={20} />
          <span>Settings saved successfully!</span>
        </motion.div>
      )}

      {/* Sport Preferences */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="section"
      >
        <div className="section-header">
          <Shield className="section-icon" size={24} />
          <h2 className="section-title">Sport Preferences</h2>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div>
            <label className="input-label" style={{ marginBottom: '12px', display: 'block' }}>
              Enabled Sports
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: '12px' }}>
              {['nfl', 'nba', 'mlb', 'nhl'].map((sport) => (
                <motion.div
                  key={sport}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => toggleSport(sport)}
                  className="card"
                  style={{
                    padding: '16px',
                    cursor: 'pointer',
                    border: settings.enabledSports.includes(sport) ? '2px solid var(--success)' : '2px solid var(--border-subtle)',
                    background: settings.enabledSports.includes(sport) ? 'rgba(0, 255, 136, 0.1)' : 'var(--bg-card)',
                    textAlign: 'center',
                    transition: 'all 0.2s'
                  }}
                >
                  <div style={{
                    fontSize: '24px',
                    marginBottom: '8px'
                  }}>
                    {sport === 'nfl' && '🏈'}
                    {sport === 'nba' && '🏀'}
                    {sport === 'mlb' && '⚾'}
                    {sport === 'nhl' && '🏒'}
                  </div>
                  <div style={{
                    fontSize: '14px',
                    fontWeight: '700',
                    color: settings.enabledSports.includes(sport) ? 'var(--success)' : 'var(--text-secondary)',
                    textTransform: 'uppercase'
                  }}>
                    {sport}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          <div className="input-group">
            <label className="input-label">Default Sport</label>
            <select
              className="input-field"
              value={settings.defaultSport}
              onChange={(e) => setSettings({ ...settings, defaultSport: e.target.value })}
            >
              {settings.enabledSports.map(sport => (
                <option key={sport} value={sport}>{sport.toUpperCase()}</option>
              ))}
            </select>
          </div>
        </div>
      </motion.div>

      {/* Bankroll Management */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="section"
      >
        <div className="section-header">
          <DollarSign className="section-icon" size={24} style={{ color: 'var(--success)' }} />
          <h2 className="section-title">Bankroll Management</h2>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="input-group">
            <label className="input-label">Total Bankroll</label>
            <div style={{ position: 'relative' }}>
              <DollarSign size={20} style={{
                position: 'absolute',
                left: '12px',
                top: '50%',
                transform: 'translateY(-50%)',
                color: 'var(--text-secondary)'
              }} />
              <input
                type="number"
                className="input-field"
                value={settings.totalBankroll}
                onChange={(e) => setSettings({ ...settings, totalBankroll: parseFloat(e.target.value) })}
                style={{ paddingLeft: '40px' }}
                step="10"
                min="0"
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            <div className="input-group">
              <label className="input-label">Max Bet Per Game</label>
              <input
                type="number"
                className="input-field"
                value={settings.maxBetPerGame}
                onChange={(e) => setSettings({ ...settings, maxBetPerGame: parseFloat(e.target.value) })}
                step="1"
                min="1"
              />
            </div>

            <div className="input-group">
              <label className="input-label">Bet Type</label>
              <select
                className="input-field"
                value={settings.maxBetType}
                onChange={(e) => setSettings({ ...settings, maxBetType: e.target.value })}
              >
                <option value="fixed">Fixed Amount ($)</option>
                <option value="percentage">Percentage (%)</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '16px', background: 'var(--bg-elevated)', borderRadius: 'var(--radius-md)' }}>
            <div>
              <div style={{ fontWeight: '600', color: 'var(--text-primary)', marginBottom: '4px' }}>
                Kelly Criterion
              </div>
              <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                Automatically calculate optimal bet sizes
              </div>
            </div>
            <div
              onClick={() => setSettings({ ...settings, kellyEnabled: !settings.kellyEnabled })}
              className="toggle-switch"
              style={{
                cursor: 'pointer',
                width: '52px',
                height: '28px',
                background: settings.kellyEnabled ? 'var(--success)' : 'var(--bg-hover)',
                borderRadius: '14px',
                position: 'relative',
                transition: 'background 0.3s'
              }}
            >
              <motion.div
                className="toggle-knob"
                animate={{ x: settings.kellyEnabled ? 26 : 2 }}
                style={{
                  width: '24px',
                  height: '24px',
                  background: 'white',
                  borderRadius: '12px',
                  position: 'absolute',
                  top: '2px'
                }}
              />
            </div>
          </div>

          <div className="input-group">
            <label className="input-label">Risk Tolerance</label>
            <div style={{ display: 'flex', gap: '8px' }}>
              {['conservative', 'moderate', 'aggressive'].map(level => (
                <motion.button
                  key={level}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setSettings({ ...settings, riskTolerance: level })}
                  className="card"
                  style={{
                    flex: 1,
                    padding: '12px',
                    cursor: 'pointer',
                    border: settings.riskTolerance === level ? '2px solid var(--primary)' : '2px solid transparent',
                    background: settings.riskTolerance === level ? 'rgba(0, 217, 255, 0.1)' : 'var(--bg-card)',
                    color: settings.riskTolerance === level ? 'var(--primary)' : 'var(--text-secondary)',
                    fontWeight: '600',
                    textTransform: 'capitalize',
                    fontSize: '14px',
                    transition: 'all 0.2s'
                  }}
                >
                  {level}
                </motion.button>
              ))}
            </div>
          </div>
        </div>
      </motion.div>

      {/* API Configuration */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="section"
      >
        <div className="section-header">
          <Key className="section-icon" size={24} style={{ color: 'var(--warning)' }} />
          <h2 className="section-title">API Configuration</h2>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="input-group">
            <label className="input-label">Odds API Key</label>
            <input
              type="password"
              className="input-field"
              value={settings.oddsApiKey}
              onChange={(e) => setSettings({ ...settings, oddsApiKey: e.target.value })}
              placeholder="Enter your Odds API key"
            />
            <p style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
              Get your API key from <a href="https://the-odds-api.com" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--primary)' }}>the-odds-api.com</a>
            </p>
          </div>

          <div className="input-group">
            <label className="input-label">OpenAI API Key (Optional)</label>
            <input
              type="password"
              className="input-field"
              value={settings.openaiApiKey}
              onChange={(e) => setSettings({ ...settings, openaiApiKey: e.target.value })}
              placeholder="Enter your OpenAI API key"
            />
            <p style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
              For enhanced AI insights and analysis
            </p>
          </div>
        </div>
      </motion.div>

      {/* Display Preferences */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="section"
      >
        <div className="section-header">
          <Palette className="section-icon" size={24} style={{ color: 'var(--accent)' }} />
          <h2 className="section-title">Display Preferences</h2>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="input-group">
            <label className="input-label">Theme</label>
            <div style={{ display: 'flex', gap: '12px' }}>
              {['dark', 'light'].map(theme => (
                <motion.button
                  key={theme}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setSettings({ ...settings, theme })}
                  className="card"
                  style={{
                    flex: 1,
                    padding: '16px',
                    cursor: 'pointer',
                    border: settings.theme === theme ? '2px solid var(--primary)' : '2px solid transparent',
                    background: settings.theme === theme ? 'rgba(0, 217, 255, 0.1)' : 'var(--bg-card)',
                    color: settings.theme === theme ? 'var(--primary)' : 'var(--text-secondary)',
                    fontWeight: '600',
                    textTransform: 'capitalize',
                    transition: 'all 0.2s'
                  }}
                >
                  {theme === 'dark' ? '🌙' : '☀️'} {theme}
                </motion.button>
              ))}
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-tertiary)', marginTop: '4px' }}>
              Note: Light mode is coming soon
            </p>
          </div>

          <div className="input-group">
            <label className="input-label">Chart Type</label>
            <select
              className="input-field"
              value={settings.chartType}
              onChange={(e) => setSettings({ ...settings, chartType: e.target.value })}
            >
              <option value="bar">Bar Chart</option>
              <option value="line">Line Chart</option>
              <option value="area">Area Chart</option>
            </select>
          </div>

          <div className="input-group">
            <label className="input-label">Odds Format</label>
            <div style={{ display: 'flex', gap: '12px' }}>
              {['american', 'decimal'].map(format => (
                <motion.button
                  key={format}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setSettings({ ...settings, oddsFormat: format })}
                  className="card"
                  style={{
                    flex: 1,
                    padding: '16px',
                    cursor: 'pointer',
                    border: settings.oddsFormat === format ? '2px solid var(--primary)' : '2px solid transparent',
                    background: settings.oddsFormat === format ? 'rgba(0, 217, 255, 0.1)' : 'var(--bg-card)',
                    color: settings.oddsFormat === format ? 'var(--primary)' : 'var(--text-secondary)',
                    fontWeight: '600',
                    textTransform: 'capitalize',
                    transition: 'all 0.2s'
                  }}
                >
                  {format === 'american' ? '-110' : '1.91'}
                  <div style={{ fontSize: '12px', marginTop: '4px', opacity: 0.7 }}>
                    {format}
                  </div>
                </motion.button>
              ))}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Notifications */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="section"
      >
        <div className="section-header">
          <Bell className="section-icon" size={24} style={{ color: 'var(--info)' }} />
          <h2 className="section-title">Notifications</h2>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {[
            { key: 'emailNotifications', label: 'Email Notifications', description: 'Receive updates via email' },
            { key: 'lineMovementAlerts', label: 'Line Movement Alerts', description: 'Get notified when odds change significantly' },
            { key: 'betResultNotifications', label: 'Bet Result Notifications', description: 'Alerts when your bets are settled' }
          ].map(({ key, label, description }) => (
            <div key={key} style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '16px',
              background: 'var(--bg-elevated)',
              borderRadius: 'var(--radius-md)'
            }}>
              <div>
                <div style={{ fontWeight: '600', color: 'var(--text-primary)', marginBottom: '4px' }}>
                  {label}
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
                  {description}
                </div>
              </div>
              <div
                onClick={() => setSettings({ ...settings, [key]: !settings[key] })}
                className="toggle-switch"
                style={{
                  cursor: 'pointer',
                  width: '52px',
                  height: '28px',
                  background: settings[key] ? 'var(--success)' : 'var(--bg-hover)',
                  borderRadius: '14px',
                  position: 'relative',
                  transition: 'background 0.3s'
                }}
              >
                <motion.div
                  animate={{ x: settings[key] ? 26 : 2 }}
                  style={{
                    width: '24px',
                    height: '24px',
                    background: 'white',
                    borderRadius: '12px',
                    position: 'absolute',
                    top: '2px'
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Action Buttons */}
      <div style={{ display: 'flex', gap: '16px', position: 'sticky', bottom: '24px', paddingTop: '24px', background: 'var(--bg-dark)', zIndex: 10 }}>
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleReset}
          style={{
            flex: 1,
            padding: '16px',
            background: 'transparent',
            color: 'var(--text-secondary)',
            border: '2px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            fontWeight: '700',
            fontSize: '16px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px'
          }}
        >
          <RefreshCw size={20} />
          Reset to Defaults
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleSave}
          disabled={loading}
          style={{
            flex: 1,
            padding: '16px',
            background: loading ? 'var(--bg-hover)' : 'linear-gradient(135deg, var(--success), var(--primary))',
            color: loading ? 'var(--text-tertiary)' : 'var(--bg-dark)',
            border: 'none',
            borderRadius: 'var(--radius-md)',
            fontWeight: '700',
            fontSize: '16px',
            cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.5 : 1,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px'
          }}
        >
          <Save size={20} />
          {loading ? 'Saving...' : 'Save Settings'}
        </motion.button>
      </div>
    </div>
  );
};

export default Settings;
