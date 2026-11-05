import { useState } from 'react'
import { API_BASE } from '../api/client'

export default function ApiDocsView() {
  const [copiedKey, setCopiedKey] = useState<string | null>(null)

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text)
    setCopiedKey(key)
    setTimeout(() => setCopiedKey(null), 2000)
  }

  const curlUpload = `curl -X POST "${API_BASE}/detect/upload" \\
  -F "file=@/path/to/shelf_image.jpg" \\
  -F "modelname=zyn" \\
  -F "project=retail_audit" \\
  -F "routeId=ROUTE-001" \\
  -F "confidence=0.5"`

  const curlUrl = `curl -X POST "${API_BASE}/detect/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "modelname": "zyn",
    "project": "retail_audit",
    "routeId": "ROUTE-001",
    "imageKey": "IMG-01",
    "imageUrl": "https://example.com/raw_shelf.jpg",
    "categoryName": "product",
    "confidence": 0.5
  }'`

  return (
    <div className="api-docs-view">
      <div className="api-header-card">
        <div>
          <h3>Enterprise REST API Reference</h3>
          <p className="card-desc">
            Production FastAPI endpoints supporting high-throughput retail image inference,
            bounding box coordinates, and SQLite/PostgreSQL persistence.
          </p>
        </div>
        <div className="api-quick-links">
          <a
            href={`${API_BASE}/docs`}
            target="_blank"
            rel="noreferrer"
            className="btn small"
          >
            Open Swagger UI ↗
          </a>
          <a
            href={`${API_BASE}/redoc`}
            target="_blank"
            rel="noreferrer"
            className="btn small secondary"
          >
            Open ReDoc ↗
          </a>
        </div>
      </div>

      <div className="api-grid">
        {/* Endpoint 1: File Upload */}
        <div className="api-card">
          <div className="endpoint-badge-row">
            <span className="method-badge method-post">POST</span>
            <span className="endpoint-path">/detect/upload</span>
          </div>
          <p className="endpoint-desc">
            Accepts multipart image files directly from client apps or field cameras, performs
            YOLO bounding box regression, saves annotated images, and returns SKU summaries.
          </p>

          <div className="code-block-wrapper">
            <div className="code-header">
              <span>cURL Example (File Upload)</span>
              <button
                type="button"
                className="copy-btn"
                onClick={() => copyToClipboard(curlUpload, 'upload')}
              >
                {copiedKey === 'upload' ? '✓ Copied' : 'Copy'}
              </button>
            </div>
            <pre><code>{curlUpload}</code></pre>
          </div>
        </div>

        {/* Endpoint 2: Remote URL */}
        <div className="api-card">
          <div className="endpoint-badge-row">
            <span className="method-badge method-post">POST</span>
            <span className="endpoint-path">/detect/</span>
          </div>
          <p className="endpoint-desc">
            Executes inference on publicly accessible S3/Cloud image URLs with built-in SSRF protection
            and streaming memory bounds.
          </p>

          <div className="code-block-wrapper">
            <div className="code-header">
              <span>cURL Example (Remote Image URL)</span>
              <button
                type="button"
                className="copy-btn"
                onClick={() => copyToClipboard(curlUrl, 'url')}
              >
                {copiedKey === 'url' ? '✓ Copied' : 'Copy'}
              </button>
            </div>
            <pre><code>{curlUrl}</code></pre>
          </div>
        </div>

        {/* Endpoint 3: Models */}
        <div className="api-card">
          <div className="endpoint-badge-row">
            <span className="method-badge method-get">GET</span>
            <span className="endpoint-path">/models</span>
          </div>
          <p className="endpoint-desc">
            Discovers all YOLO weights located in <code>app/models/</code> and returns live cache status.
          </p>
        </div>

        {/* Endpoint 4: Analytics */}
        <div className="api-card">
          <div className="endpoint-badge-row">
            <span className="method-badge method-get">GET</span>
            <span className="endpoint-path">/analytics/stats</span>
          </div>
          <p className="endpoint-desc">
            Computes historical compliance percentages, defect totals, and frequent violation distributions.
          </p>
        </div>
      </div>
    </div>
  )
}

