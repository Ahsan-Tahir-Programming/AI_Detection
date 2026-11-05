import { useState, useEffect, useCallback } from 'react'
import './App.css'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import DetectionForm from './components/DetectionForm'
import ResultsDisplay from './components/ResultsDisplay'
import Gallery from './components/Gallery'
import AnalyticsView from './components/AnalyticsView'
import ModelRegistryView from './components/ModelRegistryView'
import ApiDocsView from './components/ApiDocsView'
import type {
  DetectionFormData,
  DetectionResult,
  GalleryItem,
  ActiveTab,
  ModelDetail,
} from './types'
import {
  detectViaUrl,
  detectViaUpload,
  fetchDetections,
  deleteDetection,
  fetchModels,
} from './api/client'

function App() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('studio')
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState<boolean>(false)
  const [theme, setTheme] = useState<'light' | 'dark'>('dark')

  const [results, setResults] = useState<DetectionResult | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)

  // Discovered backend models
  const [availableModels, setAvailableModels] = useState<string[]>(['zyn'])
  const [modelsDetails, setModelsDetails] = useState<ModelDetail[]>([])
  const [selectedModel, setSelectedModel] = useState<string>('zyn')

  // Server-backed gallery state
  const [gallery, setGallery] = useState<GalleryItem[]>([])
  const [page, setPage] = useState<number>(1)
  const [pageSize] = useState<number>(12)
  const [total, setTotal] = useState<number>(0)

  // Load models on mount
  useEffect(() => {
    let isMounted = true
    async function loadModels() {
      try {
        const res = await fetchModels()
        if (isMounted) {
          if (res.models && res.models.length > 0) {
            setAvailableModels(res.models)
            setSelectedModel(res.models[0])
          }
          if (res.details) {
            setModelsDetails(res.details)
          }
        }
      } catch (err) {
        console.warn('Could not query /models endpoint, defaulting to ["zyn"]', err)
      }
    }
    loadModels()
    return () => {
      isMounted = false
    }
  }, [])

  // Memoized fetchGallery
  const fetchGallery = useCallback(
    async (pageToLoad: number = 1) => {
      try {
        const payload = await fetchDetections(pageToLoad, pageSize)
        if (payload.success) {
          setGallery(payload.data.items)
          setTotal(payload.data.total)
          setPage(pageToLoad)
        }
      } catch (e) {
        console.error('Failed to fetch gallery records:', e)
      }
    },
    [pageSize]
  )

  useEffect(() => {
    fetchGallery(1)
  }, [fetchGallery])

  const handleRemoveFromGallery = async (requestId: string) => {
    try {
      await deleteDetection(requestId)
      await fetchGallery(page)
    } catch (e) {
      console.error('Failed to delete detection record:', e)
      alert('Failed to delete record. Please try again.')
    }
  }

  const handleDetection = async (formData: DetectionFormData) => {
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      let data
      if (formData.imageFile) {
        data = await detectViaUpload(formData.imageFile, formData)
      } else {
        data = await detectViaUrl(formData)
      }

      setResults({ success: true, data })
      await fetchGallery(1)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred during inference'
      setError(errorMessage)
      setResults({ success: false, error: errorMessage })
    } finally {
      setLoading(false)
    }
  }

  // Theme synchronization
  useEffect(() => {
    const saved = localStorage.getItem('theme') as 'light' | 'dark' | null
    const initialTheme = saved || 'dark'
    setTheme(initialTheme)
    if (initialTheme === 'dark') {
      document.documentElement.classList.add('theme-dark')
    } else {
      document.documentElement.classList.remove('theme-dark')
    }
  }, [])

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark'
    setTheme(newTheme)
    localStorage.setItem('theme', newTheme)
    if (newTheme === 'dark') {
      document.documentElement.classList.add('theme-dark')
    } else {
      document.documentElement.classList.remove('theme-dark')
    }
  }

  return (
    <div className="app-shell">
      {/* Left Collapsible Navigation Sidebar */}
      <Sidebar
        activeTab={activeTab}
        onTabChange={(tab) => {
          setActiveTab(tab)
          window.scrollTo({ top: 0, behavior: 'smooth' })
        }}
        isCollapsed={isSidebarCollapsed}
        onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        totalHistory={total}
        theme={theme}
        onToggleTheme={toggleTheme}
      />

      {/* Main Workspace Area */}
      <div className="main-viewport">
        <Navbar
          activeTab={activeTab}
          activeModel={selectedModel}
          totalDetections={total}
        />

        <main className="page-content">
          {activeTab === 'studio' && (
            <div className="studio-layout">
              <DetectionForm
                onSubmit={handleDetection}
                loading={loading}
                availableModels={availableModels}
              />

              {error && (
                <div className="error-banner">
                  <p>❌ <strong>Inference Error:</strong> {error}</p>
                </div>
              )}

              {loading && (
                <div className="loading">
                  <div className="spinner"></div>
                  <p>Running YOLO inference and generating bounding boxes...</p>
                </div>
              )}

              {results && <ResultsDisplay result={results} />}
            </div>
          )}

          {activeTab === 'analytics' && <AnalyticsView />}

          {activeTab === 'history' && (
            <Gallery
              items={gallery}
              onRemove={handleRemoveFromGallery}
              page={page}
              total={total}
              pageSize={pageSize}
              onPageChange={(p) => fetchGallery(p)}
            />
          )}

          {activeTab === 'models' && (
            <ModelRegistryView
              modelsDetails={modelsDetails}
              activeModel={selectedModel}
              onSelectModel={(name) => {
                setSelectedModel(name)
                setActiveTab('studio')
              }}
            />
          )}

          {activeTab === 'api' && <ApiDocsView />}
        </main>
      </div>
    </div>
  )
}

export default App
