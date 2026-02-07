import React, { useState } from 'react'

interface DetectionFormData {
  modelname: string
  project: string
  imageKey: string
  imageUrl: string
  categoryName: string
  routeId: string
  visitDate: string
}

interface DetectionFormProps {
  onSubmit: (formData: DetectionFormData) => Promise<void>
  loading: boolean
}

export default function DetectionForm({ onSubmit, loading }: DetectionFormProps) {
  const [formData, setFormData] = useState({
    modelname: '',
    project: '',
    imageKey: '',
    imageUrl: '',
    categoryName: '',
    routeId: '',
    visitDate: new Date().toISOString().split('T')[0],
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <form className="detection-form" onSubmit={handleSubmit}>
      <h2>Detection Configuration</h2>

      <div className="form-group">
        <label htmlFor="modelname">Model Name *</label>
        <input
          id="modelname"
          type="text"
          name="modelname"
          value={formData.modelname}
          onChange={handleChange}
          placeholder="ir"
          required
          disabled={loading}
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="project">Project *</label>
          <input
            id="project"
            type="text"
            name="project"
            value={formData.project}
            onChange={handleChange}
            placeholder="ai"
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="routeId">Route ID *</label>
          <input
            id="routeId"
            type="text"
            name="routeId"
            value={formData.routeId}
            onChange={handleChange}
            placeholder="23333"
            required
            disabled={loading}
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="imageKey">Image Key *</label>
          <input
            id="imageKey"
            type="text"
            name="imageKey"
            value={formData.imageKey}
            onChange={handleChange}
            placeholder="23348"
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="categoryName">Category *</label>
          <input
            id="categoryName"
            type="text"
            name="categoryName"
            value={formData.categoryName}
            onChange={handleChange}
            placeholder="non-drink"
            required
            disabled={loading}
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="imageUrl">Image URL *</label>
        <input
          id="imageUrl"
          type="url"
          name="imageUrl"
          value={formData.imageUrl}
          onChange={handleChange}
          placeholder="https://example.com/image.jpg"
          required
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="visitDate">Visit Date</label>
        <input
          id="visitDate"
          type="date"
          name="visitDate"
          value={formData.visitDate}
          onChange={handleChange}
          disabled={loading}
        />
      </div>

      <button type="submit" disabled={loading} className="submit-btn">
        {loading ? 'Processing...' : 'Run Detection'}
      </button>
    </form>
  )
}
