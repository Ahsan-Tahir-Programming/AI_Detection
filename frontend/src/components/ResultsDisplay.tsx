interface DetectionResultProps {
  result: {
    success: boolean
    data?: {
      project?: string
      routeId?: string
      imageKey?: string[]
      imageSize?: number[]
      requestId?: string
      visitDate?: string
      detectedSKU?: Record<string, any>
      originalImageUrl?: string
      processedImageUrl?: string
    }
    error?: string
  }
}

export default function ResultsDisplay({ result }: DetectionResultProps) {
  if (!result.success) {
    return (
      <div className="results error-result">
        <h3>❌ Detection Failed</h3>
        <p className="error-text">{result.error || 'Unknown error'}</p>
      </div>
    )
  }

  if (!result.data) {
    return null
  }

  const { project, routeId, detectedSKU, originalImageUrl, processedImageUrl } = result.data

  const skuRows = Object.entries(detectedSKU || {}).map(([sku, info]) => ({ sku, ...info }))

  return (
    <div className="results success-result">
      <h3>✅ Detection Successful</h3>

      <div className="result-summary">
        <div className="summary-item">
          <strong>Project:</strong>
          <span>{project}</span>
        </div>
        <div className="summary-item">
          <strong>Route:</strong>
          <span>{routeId}</span>
        </div>
      </div>

      <div className="image-row">
        <div className="image-card">
          <h4>Original</h4>
          <img src={originalImageUrl} alt="original" />
        </div>
        <div className="image-card">
          <h4>Processed</h4>
          <img src={processedImageUrl} alt="processed" />
        </div>
      </div>

      <div className="sku-table">
        <h4>SKU Summary</h4>
        <table>
          <thead>
            <tr>
              <th>SKU</th>
              <th>Detected</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            {skuRows.map((row) => (
              <tr key={row.sku}>
                <td>{row.sku}</td>
                <td>{row.detected ? 'Yes' : 'No'}</td>
                <td>{row.count || 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
