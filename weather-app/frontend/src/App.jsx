import { useState } from 'react'
import './index.css'

function WeatherCard({ data }) {
  if (!data || data.error) return (
      <div className="error-toast">{data?.error || "No data available"}</div>
  );

  const { location, current, forecast } = data;

  return (
    <div className="weather-widget">
      <div className="weather-header">
        <h2 className="location-name">{location}</h2>
        <div className="stat-label">
            {new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' })}
        </div>
      </div>

      <div className="current-row">
        <div className="current-temp-container">
          <span className="current-temp">{current.temp}</span>
          <span className="current-unit">°C</span>
        </div>
        
        <div className="weather-stats">
          <div className="stat-item">
            <span className="stat-value">{current.wind} km/h</span>
            <span className="stat-label">Wind</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{current.humidity}%</span>
            <span className="stat-label">Humidity</span>
          </div>
        </div>
      </div>

      <div className="forecast-grid">
        {forecast.map((day, idx) => (
          <div key={idx} className="forecast-item">
            <span className="forecast-date">
                {new Date(day.date).toLocaleDateString(undefined, { weekday: 'short' })}
            </span>
            <div className="forecast-temps">
              {day.max_temp}°
              <span className="forecast-low">{day.min_temp}°</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function App() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setResult(null)
    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })
      
      if (!res.ok) {
        throw new Error('Service currently unavailable. Please try again.')
      }
      
      const data = await res.json()
      // Backend returns either { type: 'ai', message: ... } or { type: 'fallback', data: ... }
      setResult(data)
    } catch (error) {
      console.error(error)
      setResult({ type: 'error', message: error.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header>
        <h1>Weather AI</h1>
        <p className="subtitle">Your intelligent forecasting companion</p>
      </header>

      <div className="glass-card">
        <div className="search-container">
            <form onSubmit={handleSearch} className="search-form">
            <input 
                type="text" 
                placeholder="Ask anything... (e.g., 'Weather in NYC')" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={loading}
            />
            <button type="submit" disabled={loading}>
                {loading ? <span className="loader"></span> : 'Ask AI'}
            </button>
            </form>
        </div>

        {(result || loading) && (
          <div className="response-area">
             {loading && (
                 <div style={{textAlign: 'center', padding: '1rem'}}>
                     <span style={{color: 'var(--text-secondary)'}}>Analyzing atmospheric data...</span>
                 </div>
             )}
             
             {result && !loading && (
               <>
                 {result.type === 'ai' && (
                    <>
                        <div className="weather-badge">AI Response</div>
                        <div className="response-content">
                            {result.message}
                        </div>
                    </>
                 )}

                 {result.type === 'fallback' && (
                    <>
                        <div className="weather-badge badge-warning" title={result.error}>
                            AI Unavailable &bull; Live Data
                        </div>
                        <WeatherCard data={result.data} />
                        {result.error && result.error !== "API Key missing" && (
                            <div style={{
                                fontSize: '0.8rem', 
                                color: 'rgba(255, 255, 255, 0.4)', 
                                marginTop: '1rem',
                                textAlign: 'center'
                            }}>
                                <span style={{opacity: 0.7}}>Note: {result.error}</span>
                            </div>
                        )}
                    </>
                 )}
                 
                 {result.type === 'error' && (
                     <div className="error-toast">{result.message}</div>
                 )}
               </>
             )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
