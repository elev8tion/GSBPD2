import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { SportProvider } from './contexts/SportContext'
import { NotificationProvider } from './contexts/NotificationContext'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <SportProvider>
        <NotificationProvider>
          <App />
        </NotificationProvider>
      </SportProvider>
    </BrowserRouter>
  </StrictMode>,
)
