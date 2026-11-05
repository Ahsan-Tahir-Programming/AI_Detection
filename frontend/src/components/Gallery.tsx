import { useState } from 'react'
import type { GalleryItem } from '../types'
import { getDownloadUrl } from '../api/client'

interface GalleryProps {
  items: GalleryItem[]
  onRemove: (requestId: string) => Promise<void>
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
  const [searchTerm, setSearchTerm] = useState('')

  if (!items.length) {
    return (
      <div className="gallery-empty">
        <span className="empty-icon">🗄️</span>
        <h4>No Historical Audit Records Found</h4>
        <p>Run your first YOLO inference in the Detection Studio to generate and persist annotated images.</p>
      </div>
    )
  }

  const filteredItems = items.filter((item) => {
    if (!searchTerm.trim()) return true
    const term = searchTerm.toLowerCase()
    return (
      (item.routeId && item.routeId.toLowerCase().includes(term)) ||
      (item.project && item.project.toLowerCase().includes(term)) ||
      (item.visitDate && item.visitDate.toLowerCase().includes(term))
    )
  })

  const totalPages = Math.max(1, Math.ceil((total || items.length) / pageSize))

  const handleDownloadImage = (imageUrl: string) => {
    const filename = imageUrl.split('?')[0].split('/').pop() || 'processed.jpg'
    const downloadUrl = getDownloadUrl(filename)

    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const handleRemoveConfirm = (requestId: string) => {
    if (window.confirm('Are you sure you want to delete this detection record and its processed image?')) {
      onRemove(requestId)
    }
  }

  return (
    <div className="gallery">
      <div className="gallery-header-row">
        <div>
          <h3>Audit Records & Annotated Image Gallery</h3>
          <p className="section-note">
            Persisted YOLO detections with annotated bounding boxes and metadata ({total} total runs)
          </p>
        </div>

        <div className="gallery-filter-wrap">
          <input
            type="text"
            className="search-input"
            placeholder="Filter by Route, Project, or Date..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="gallery-grid">
        {filteredItems.map((item) => (
          <div key={item.requestId} className="gallery-card">
            <div className="img-wrap">
              <img
                src={item.processedImageUrl}
                alt={`Processed result for ${item.routeId || item.requestId}`}
                loading="lazy"
              />
            </div>
            <div className="meta">
              <div className="meta-row">
                <strong>Route:</strong> <span>{item.routeId || 'N/A'}</span>
              </div>
              <div className="meta-row">
                <strong>Profile:</strong> <span className="uppercase-tag">{item.project || 'N/A'}</span>
              </div>
              <div className="meta-row">
                <strong>Date:</strong> <span>{item.visitDate || 'N/A'}</span>
              </div>
              {item.detections && (
                <div className="meta-row">
                  <strong>Objects:</strong>
                  <span className="objects-badge">{item.detections.length} Detected</span>
                </div>
              )}
            </div>
            <div className="actions">
              <a
                href={item.processedImageUrl}
                target="_blank"
                rel="noreferrer"
                className="btn small"
              >
                View
              </a>
              <button
                type="button"
                className="btn small secondary"
                onClick={() => handleDownloadImage(item.processedImageUrl)}
              >
                Download
              </button>
              <button
                type="button"
                className="btn small danger"
                onClick={() => handleRemoveConfirm(item.requestId)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            type="button"
            className="btn small pagination-btn"
            disabled={page <= 1}
            onClick={() => onPageChange && onPageChange(page - 1)}
          >
            ← Previous
          </button>
          <div className="pagination-info">
            Page {page} of {totalPages}
          </div>
          <button
            type="button"
            className="btn small pagination-btn"
            disabled={page >= totalPages}
            onClick={() => onPageChange && onPageChange(page + 1)}
          >
            Next →
          </button>
        </div>
      )}
    </div>
  )
}
