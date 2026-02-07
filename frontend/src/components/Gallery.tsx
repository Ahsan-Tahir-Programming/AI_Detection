interface GalleryItem {
  requestId: string
  processedImageUrl: string
  originalImageUrl: string
  project?: string
  routeId?: string
  imageKey?: string
  visitDate?: string
}

interface GalleryProps {
  items: GalleryItem[]
  onRemove: (requestId: string) => void
  page?: number
  total?: number
  pageSize?: number
  onPageChange?: (page: number) => void
}

export default function Gallery({
  items,
  onRemove,
  page = 1,
  total = 0,
  pageSize = 12,
  onPageChange,
}: GalleryProps) {
  if (!items.length) return null

  const totalPages = Math.max(1, Math.ceil((total || items.length) / pageSize))

  // API base URL - uses environment variable or falls back to localhost
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const handleViewImage = (imageUrl: string) => {
    window.open(imageUrl, '_blank')
  }

  const handleDownloadImage = (imageUrl: string) => {
    // Extract filename from URL
    const url = new URL(imageUrl)
    const filename = url.pathname.split('/').pop()
    
    if (!filename) {
      alert('Failed to extract filename')
      return
    }

    // Call the download endpoint with proper Content-Disposition header
    const downloadUrl = `${API_URL}/download-image/${filename}`
    
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = filename
    
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="gallery">
      <h3 style={{ color: '#fff' }}>Saved Detections</h3>

      <div className="gallery-grid">
        {items.map((it) => (
          <div key={it.requestId} className="gallery-card">
            <div className="img-wrap">
              <img src={it.processedImageUrl} alt={it.requestId} />
            </div>
            <div className="meta">
              <div>
                <strong>Route:</strong> {it.routeId}
              </div>
              <div>
                <strong>Project:</strong> {it.project}
              </div>
              <div>
                <strong>Date:</strong> {it.visitDate}
              </div>
            </div>
            <div className="actions">
              <button className="btn small" onClick={() => handleViewImage(it.processedImageUrl)}>
                View
              </button>
              <button 
                className="btn small" 
                onClick={() => handleDownloadImage(it.processedImageUrl)}
              >
                Download
              </button>
              <button className="btn small danger" onClick={() => onRemove(it.requestId)}>
                Remove
              </button>
            </div>
          </div>
        ))}
      </div>

      <div
        className="pagination"
        style={{ marginTop: 12, display: 'flex', justifyContent: 'center', gap: 8 }}
      >
        <button
          className="btn small"
          onClick={() => onPageChange && onPageChange(Math.max(1, page - 1))}
        >
          Prev
        </button>
        <div style={{ padding: '0.4rem 0.8rem', background: '#fff', borderRadius: 6, color: '#1a1a1a', fontWeight: 'bold' }}>
          Page {page} / {totalPages}
        </div>
        <button
          className="btn small"
          onClick={() => onPageChange && onPageChange(Math.min(totalPages, page + 1))}
        >
          Next
        </button>
      </div>
    </div>
  )
}
