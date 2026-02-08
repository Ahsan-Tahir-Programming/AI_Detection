import { useState, useEffect } from 'react'
import './App.css'
import DetectionForm from './components/DetectionForm'
import ResultsDisplay from './components/ResultsDisplay'
import Gallery from './components/Gallery'

interface DetectionFormData {
  modelname: string
  project: string
  imageKey: string
  imageUrl: string
  categoryName: string
  routeId: string
  visitDate: string
}

interface DetectionResult {
  success: boolean
  data?: {
    id?: number
    requestId?: string
    project?: string
    routeId?: string
    imageKey?: string[]
    imageSize?: number[]
    visitDate?: string
    detectedSKU?: Record<string, any>
    originalImageUrl?: string
    processedImageUrl?: string
    detections?: any[]
    createdAt?: string
  }
  error?: string
}

function App() {
  const [results, setResults] = useState<DetectionResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Server-backed gallery (pagination)
  const [gallery, setGallery] = useState<any[]>([])
  const [page, setPage] = useState(1)
  const [pageSize] = useState(12)
  const [total, setTotal] = useState(0)

  const fetchGallery = async (pageToLoad = 1) => {
    try {
      const res = await fetch(
        `http://localhost:8000/detections/?page=${pageToLoad}&page_size=${pageSize}`
      )
      const payload = await res.json()
      if (res.ok && payload.success) {
        setGallery(payload.data.items)
        setTotal(payload.data.total)
        setPage(pageToLoad)
      }
    } catch (e) {
      console.error('Failed to fetch gallery', e)
    }
  }

  const handleRemoveFromGallery = async (requestId: string) => {
    try {
      const res = await fetch(`http://localhost:8000/detections/${requestId}`, { method: 'DELETE' })
      if (res.ok) {
        // refresh current page
        fetchGallery(page)
      }
    } catch (e) {
      console.error('Failed to delete', e)
    }
  }

  // fetch initial gallery
  useEffect(() => {
    fetchGallery(1)
  }, [])

  const handleDetection = async (formData: DetectionFormData) => {
    setLoading(true)
    setError(null)
    setResults(null)
    try {
      const response = await fetch('http://localhost:8000/detect/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      const data = await response.json()

      if (!response.ok || data.success === false) {
        // Backend returned an error
        const errMsg = data?.error || data?.detail || 'Detection failed'
        setError(errMsg)
        setResults(null)
        return
      }

      // Success
      setResults({success: true, data})

      // Refresh server-backed gallery
      await fetchGallery(1)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred'
      setError(errorMessage)
      setResults(null)
    } finally {
      setLoading(false)
    }
  }

  // Theme (light/dark) — default to light when not explicitly set
  useEffect(() => {
    const saved = localStorage.getItem('theme')
    if (saved === 'dark') {
      document.documentElement.classList.add('theme-dark')
    } else {
      document.documentElement.classList.remove('theme-dark')
    }
    console.log('App mounted — theme:', saved)
  }, [])

  const toggleTheme = () => {
    const isDark = document.documentElement.classList.toggle('theme-dark')
    localStorage.setItem('theme', isDark ? 'dark' : 'light')
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-brand">
          <div className="logo-sm">🤖</div>
          <div>
            <h1>AI Detection System</h1>
            <p>Real-time object detection using YOLO models</p>
          </div>
        </div>
        <div style={{ position: 'absolute', right: 20, top: 18 }}>
          <button className="btn small" onClick={toggleTheme}>
            Toggle Theme
          </button>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          <DetectionForm onSubmit={handleDetection} loading={loading} />

          {error && (
            <div className="error-banner">
              <p>❌ Error: {error}</p>
            </div>
          )}

          {results && <ResultsDisplay result={results} />}

          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Processing detection...</p>
            </div>
          )}

          {/* Saved gallery */}
          <Gallery
            items={gallery}
            onRemove={handleRemoveFromGallery}
            page={page}
            total={total}
            pageSize={pageSize}
            onPageChange={(p) => fetchGallery(p)}
          />
        </div>
      </main>
    </div>
  )
}

export default App
