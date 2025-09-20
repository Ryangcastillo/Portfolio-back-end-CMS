import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react'
import './App.css'

// Components
import Navbar from './Navbar'
import Footer from './Footer'
import ChatBot from './ChatBot'

// Pages
import Home from './Portfolio/Home'
import DataAnalysis from './Portfolio/DataAnalysis'
import MachineLearning from './Portfolio/MachineLearning'
import WebApps from './Portfolio/WebApps'
import AIAgents from './Portfolio/AIAgents'

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false)

  useEffect(() => {
    // Check for saved theme preference or default to light mode
    const savedTheme = localStorage.getItem('theme')
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
      setIsDarkMode(true)
      document.documentElement.classList.add('dark')
    }
  }, [])

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode)
    if (!isDarkMode) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }

  return (
    <Router>
      <div className="min-h-screen bg-background text-foreground">
        <Navbar isDarkMode={isDarkMode} toggleTheme={toggleTheme} />
        
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/data-analysis" element={<DataAnalysis />} />
            <Route path="/machine-learning" element={<MachineLearning />} />
            <Route path="/web-apps" element={<WebApps />} />
            <Route path="/ai-agents" element={<AIAgents />} />
          </Routes>
        </main>

        <Footer />
        <ChatBot />
      </div>
    </Router>
  )
}

export default App

