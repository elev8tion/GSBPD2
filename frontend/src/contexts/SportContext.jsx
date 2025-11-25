import React, { createContext, useContext, useState, useEffect } from 'react';

const SportContext = createContext();

export const useSport = () => {
  const context = useContext(SportContext);
  if (!context) {
    throw new Error('useSport must be used within a SportProvider');
  }
  return context;
};

export const SportProvider = ({ children }) => {
  const [selectedSport, setSelectedSport] = useState(() => {
    // Load from localStorage if available
    return localStorage.getItem('selectedSport') || 'NBA';
  });

  useEffect(() => {
    // Save to localStorage whenever it changes
    localStorage.setItem('selectedSport', selectedSport);
  }, [selectedSport]);

  const toggleSport = () => {
    setSelectedSport(prev => prev === 'NBA' ? 'NFL' : 'NBA');
  };

  return (
    <SportContext.Provider value={{ selectedSport, setSelectedSport, toggleSport }}>
      {children}
    </SportContext.Provider>
  );
};
