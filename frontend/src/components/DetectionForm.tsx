import { useState, useRef } from 'react'
import type { DetectionFormData } from '../types'

interface DetectionFormProps {
  onSubmit: (formData: DetectionFormData) => Promise<void>
  loading: boolean
  availableModels: string[]
}

type InputMode = 'upload' | 'url'

export default function DetectionForm({
  onSubmit,
  loading,
  availableModels,
}: DetectionFormProps) {
  const [inputMode, setInputMode] = useState<InputMode>('upload')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [filePreview, setFilePreview] = useState<string | null>(null)
  const [showAdvanced, setShowAdvanced] = useState<boolean>(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const [formData, setFormData] = useState<DetectionFormData>({
    modelname: availableModels.length > 0 ? availableModels[0] : 'zyn',
    project: 'retail_audit',
    routeId: 'ROUTE-001',
    imageKey: 'IMG-001',
    imageUrl: 'https://s3.us-east-1.wasabisys.com/ir-nestle-models/original%20image%20urls%20for%20test%20request/BWU%20Damage24.jpg',
    categoryName: 'BWU',
    visitDate: new Date().toISOString().split('T')[0],
    confidence: 0.5,
    iou: 0.7,
  })

  // Derived effective model to avoid cascading renders
  const effectiveModel = availableModels.includes(formData.modelname)
    ? formData.modelname
    : availableModels[0] || 'zyn'

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target
    if (type === 'range') {
      setFormData((prev) => ({ ...prev, [name]: parseFloat(value) }))
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }))
    }
  }

  const handleFileSelect = (file: File) => {
    setSelectedFile(file)
    const previewUrl = URL.createObjectURL(file)
    setFilePreview(previewUrl)
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    if (loading) return
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0]
      if (file.type.startsWith('image/')) {
        handleFileSelect(file)
      }
    }
  }

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
  }

  const handleClearFile = () => {
    setSelectedFile(null)
    if (filePreview) {
      URL.revokeObjectURL(filePreview)
      setFilePreview(null)
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputMode === 'upload' && !selectedFile) {
      alert('Please select an image file to upload')
      return
    }
    if (inputMode === 'url' && !formData.imageUrl?.trim()) {
      alert('Please provide a valid image URL')
      return
    }

    const submissionData: DetectionFormData = {
      ...formData,
      modelname: effectiveModel,
      imageFile: inputMode === 'upload' ? selectedFile : null,
      imageUrl: inputMode === 'url' ? formData.imageUrl : undefined,
    }
    onSubmit(submissionData)
  }

  return (
    <form className="detection-form" onSubmit={handleSubmit}>
      <div className="form-header-row">
        <div>
          <h2>Inference Configuration</h2>
          <p className="form-desc">Select model weights, tuning thresholds, and input source</p>
        </div>

        <div className="mode-toggle-group">
          <button
            type="button"
            className={`mode-toggle-btn ${inputMode === 'upload' ? 'active' : ''}`}
            onClick={() => setInputMode('upload')}
            disabled={loading}
          >
            📁 Upload Local Image
          </button>
          <button
            type="button"
            className={`mode-toggle-btn ${inputMode === 'url' ? 'active' : ''}`}
            onClick={() => setInputMode('url')}
            disabled={loading}
          >
            🔗 Remote Image URL
          </button>
        </div>
      </div>

      {/* Model Selection & Confidence Slider */}
      <div className="form-row">
        <div className="form-group">
          <label htmlFor="modelname">AI Vision Model *</label>
          <select
            id="modelname"
            name="modelname"
            value={effectiveModel}
            onChange={handleInputChange}
            disabled={loading}
          >
            {availableModels.length > 0 ? (
              availableModels.map((m) => (
                <option key={m} value={m}>
                  {m.toUpperCase()} (YOLOv8 Weights)
                </option>
              ))
            ) : (
              <option value="zyn">ZYN (YOLOv8 Weights)</option>
            )}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="confidence">
            Confidence Threshold: <strong>{Math.round((formData.confidence || 0.5) * 100)}%</strong>
          </label>
          <input
            id="confidence"
            type="range"
            name="confidence"
            min="0.1"
            max="0.95"
            step="0.05"
            value={formData.confidence || 0.5}
            onChange={handleInputChange}
            disabled={loading}
            className="slider-input"
          />
        </div>
      </div>

      {/* Input Mode Selector Area */}
      {inputMode === 'upload' ? (
        <div className="form-group">
          <label>Image File *</label>
          <div
            className={`dropzone ${filePreview ? 'has-preview' : ''}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={() => !filePreview && fileInputRef.current?.click()}
          >
            <input
              type="file"
              ref={fileInputRef}
              accept="image/*"
              style={{ display: 'none' }}
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  handleFileSelect(e.target.files[0])
                }
              }}
              disabled={loading}
            />

            {filePreview && selectedFile ? (
              <div className="preview-container">
                <img src={filePreview} alt="Selected preview" className="file-thumbnail" />
                <div className="file-meta">
                  <span className="file-name">{selectedFile.name}</span>
                  <span className="file-size">
                    {(selectedFile.size / 1024).toFixed(1)} KB
                  </span>
                  <button
                    type="button"
                    className="btn-text-danger"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleClearFile()
                    }}
                    disabled={loading}
                  >
                    Remove File
                  </button>
                </div>
              </div>
            ) : (
              <div className="dropzone-prompt">
                <span className="upload-icon">📷</span>
                <p>Drag and drop a raw shelf image here, or <strong>click to browse</strong></p>
                <small>Supports JPG, PNG, WEBP up to 25MB (Upload un-annotated raw images)</small>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="form-group">
          <label htmlFor="imageUrl">Public Image URL *</label>
          <input
            id="imageUrl"
            type="url"
            name="imageUrl"
            value={formData.imageUrl || ''}
            onChange={handleInputChange}
            placeholder="https://example.com/raw-store-image.jpg"
            required={inputMode === 'url'}
            disabled={loading}
          />
        </div>
      )}

      {/* Expandable Advanced Audit Metadata */}
      <div className="accordion-section">
        <button
          type="button"
          className="accordion-toggle"
          onClick={() => setShowAdvanced(!showAdvanced)}
        >
          <span>{showAdvanced ? '▼' : '▶'} Enterprise Audit Parameters</span>
          <span className="accordion-badge">
            {showAdvanced ? 'Click to minimize' : 'Optional (pre-populated)'}
          </span>
        </button>

        {showAdvanced && (
          <div className="accordion-body">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="project">Project / Initiative</label>
                <input
                  id="project"
                  type="text"
                  name="project"
                  value={formData.project}
                  onChange={handleInputChange}
                  placeholder="retail_audit"
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="routeId">Route / Location ID</label>
                <input
                  id="routeId"
                  type="text"
                  name="routeId"
                  value={formData.routeId}
                  onChange={handleInputChange}
                  placeholder="ROUTE-001"
                  disabled={loading}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="imageKey">Image Key</label>
                <input
                  id="imageKey"
                  type="text"
                  name="imageKey"
                  value={formData.imageKey}
                  onChange={handleInputChange}
                  placeholder="IMG-001"
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="categoryName">Category Tag</label>
                <input
                  id="categoryName"
                  type="text"
                  name="categoryName"
                  value={formData.categoryName}
                  onChange={handleInputChange}
                  placeholder="BWU"
                  disabled={loading}
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="visitDate">Audit Date</label>
              <input
                id="visitDate"
                type="date"
                name="visitDate"
                value={formData.visitDate}
                onChange={handleInputChange}
                disabled={loading}
              />
            </div>
          </div>
        )}
      </div>

      <button type="submit" disabled={loading} className="submit-btn">
        {loading ? (
          <span className="btn-loading">
            <span className="spinner-sm"></span> Executing YOLO Inference...
          </span>
        ) : (
          '🚀 Run Object Detection'
        )}
      </button>
    </form>
  )
}
