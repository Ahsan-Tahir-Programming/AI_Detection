import type { ActiveTab } from '../types'
import { API_BASE } from '../api/client'

interface NavbarProps {
  activeTab: ActiveTab
  activeModel: string
  totalDetections: number
}

const tabTitles: Record<ActiveTab, { title: string; subtitle: string }> = {
  studio: {
    title: 'Detection Studio',
    subtitle: 'Upload shelf images, tune confidence, and generate instant object annotations',
  },
  analytics: {
    title: 'Audit Analytics & Insights',
    subtitle: 'High-level compliance rates, defect distribution, and retail audit performance',
  },
  history: {
    title: 'Historical Audit Records',
    subtitle: 'Inspect, download, and manage previous AI detection runs and annotated files',
  },
  models: {
    title: 'YOLO Model Registry',
    subtitle: 'Discovered model weights, class mappings, and inference configuration',
  },
  api: {
    title: 'API & Integration Reference',
    subtitle: 'FastAPI endpoints, OpenAPI schemas, and cURL commands for backend consumption',
  },
}

export default function Navbar({ activeTab, activeModel, totalDetections }: NavbarProps) {
  const meta = tabTitles[activeTab] || tabTitles.studio

  return (
    <header className="top-navbar">
      <div className="navbar-breadcrumb">
        <div className="breadcrumb-path">
          <span className="platform-tag">ShelfVision</span>
          <span className="path-divider">/</span>
          <span className="current-page">{meta.title}</span>
        </div>
        <p className="navbar-subtitle">{meta.subtitle}</p>
      </div>

      <div className="navbar-actions">
        <div className="status-pill model-pill" title="Currently selected inference model">
          <span className="pill-dot"></span>
          <span className="pill-text">Model: <strong>{activeModel.toUpperCase()}</strong></span>
        </div>

        <div className="status-pill count-pill" title="Total saved detection records">
          <span className="pill-icon">📊</span>
          <span className="pill-text">{totalDetections} Audits</span>
        </div>

        <a
          href={`${API_BASE}/docs`}
          target="_blank"
          rel="noreferrer"
          className="btn-nav-action"
          title="Open interactive Swagger API Documentation"
        >
          <span>Swagger API</span>
          <span className="nav-arrow">↗</span>
        </a>
      </div>
    </header>
  )
}

