import type { DetectionResult } from '../types'
import { getDownloadUrl } from '../api/client'

interface ResultsDisplayProps {
  result: DetectionResult
}

export default function ResultsDisplay({ result }: ResultsDisplayProps) {
  if (!result.success) {
    return (
      <div className="results error-result">
        <div className="error-card-header">
          <span className="error-icon">❌</span>
          <div>
            <h3>Inference Failed</h3>
            <p className="error-text">{result.error || 'An unexpected error occurred during processing.'}</p>
          </div>
        </div>
      </div>
    )
  }

  if (!result.data) {
    return null
  }

  const {
    project,
    routeId,
    visitDate,
    imageSize,
    detectedSKU,
    detections,
    originalImageUrl,
    processedImageUrl,
  } = result.data

  const skuRows = Object.entries(detectedSKU || {}).map(([sku, info]) => ({
    sku,
    detected: info.detected,
    count: info.count || 0,
  }))

  const handleDownload = () => {
    if (!processedImageUrl) return
    const filename = processedImageUrl.split('/').pop() || 'processed.jpg'
    const link = document.createElement('a')
    link.href = getDownloadUrl(filename)
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="results success-result">
      <div className="result-header">
        <div>
          <h3>✅ Detection Analysis Complete</h3>
          <p className="result-subtitle">
            Identified <strong>{detections.length}</strong> object{detections.length === 1 ? '' : 's'} on Route{' '}
            <code>{routeId}</code>
          </p>
        </div>
        <button type="button" className="btn action-btn download-btn" onClick={handleDownload}>
          📥 Download Annotated Image
        </button>
      </div>

      <div className="result-summary">
        <div className="summary-item">
          <strong>Project Profile</strong>
          <span>{project}</span>
        </div>
        <div className="summary-item">
          <strong>Route / Store ID</strong>
          <span>{routeId}</span>
        </div>
        <div className="summary-item">
          <strong>Audit Date</strong>
          <span>{visitDate}</span>
        </div>
        <div className="summary-item">
          <strong>Resolution</strong>
          <span>
            {imageSize && imageSize.length >= 2 ? `${imageSize[0]} × ${imageSize[1]} px` : 'N/A'}
          </span>
        </div>
      </div>

      <div className="image-row">
        {originalImageUrl && (
          <div className="image-card">
            <h4>Raw Input Image</h4>
            <div className="img-container">
              <img src={originalImageUrl} alt="Original uploaded or referenced asset" />
            </div>
            <a
              href={originalImageUrl}
              target="_blank"
              rel="noreferrer"
              className="view-link"
            >
              🔍 Open Full Resolution
            </a>
          </div>
        )}

        <div className="image-card highlighted">
          <h4>YOLOv8 Annotated Output</h4>
          <div className="img-container">
            <img src={processedImageUrl} alt="Annotated detection output" />
          </div>
          <div className="card-actions">
            <a
              href={processedImageUrl}
              target="_blank"
              rel="noreferrer"
              className="view-link"
            >
              🔍 Open Full Resolution
            </a>
            <button type="button" className="btn small secondary" onClick={handleDownload}>
              Save File
            </button>
          </div>
        </div>
      </div>

      {/* Detections Breakdown */}
      {detections && detections.length > 0 ? (
        <div className="detections-section">
          <h4>Detected Bounding Boxes ({detections.length})</h4>
          <div className="detections-grid">
            {detections.map((det, idx) => (
              <div key={idx} className="detection-pill-card">
                <div className="pill-header">
                  <span className="det-class-name">{det.class_name}</span>
                  <span className="confidence-badge">
                    {Math.round(det.confidence * 100)}%
                  </span>
                </div>
                <div className="pill-coords">
                  Box: [{det.coordinates.x}, {det.coordinates.y}, {det.coordinates.w}w × {det.coordinates.h}h]
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="zero-detection-banner">
          <span className="info-icon">ℹ️</span>
          <div>
            <strong>Zero Objects Detected</strong>
            <p>
              No target objects identified at the current confidence threshold. If this was unexpected,
              verify that you uploaded a raw un-annotated image, or try reducing the confidence threshold slider.
            </p>
          </div>
        </div>
      )}

      {/* SKU Summary Table */}
      <div className="sku-table">
        <h4>SKU Compliance Summary</h4>
        <table>
          <thead>
            <tr>
              <th>Mapped SKU Classification</th>
              <th>Compliance / Detected</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            {skuRows.map((row) => (
              <tr key={row.sku}>
                <td>
                  <code>{row.sku}</code>
                </td>
                <td>
                  <span className={`status-badge ${row.detected ? 'status-yes' : 'status-no'}`}>
                    {row.detected ? '✓ Detected' : '— None'}
                  </span>
                </td>
                <td>
                  <strong>{row.count}</strong>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
