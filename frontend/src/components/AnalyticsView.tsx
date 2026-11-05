import { useEffect, useState } from 'react'
import type { AnalyticsData } from '../types'
import { fetchAnalytics } from '../api/client'

export default function AnalyticsView() {
  const [data, setData] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  const loadStats = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetchAnalytics()
      if (res.success) {
        setData(res.data)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch analytics')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadStats()
  }, [])

  if (loading) {
    return (
      <div className="view-loading-card">
        <div className="spinner"></div>
        <p>Aggregating historical detection analytics...</p>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="view-error-card">
        <p>❌ {error || 'No analytics data available.'}</p>
        <button type="button" className="btn small" onClick={loadStats}>
          Retry
        </button>
      </div>
    )
  }

  const defectEntries = Object.entries(data.defect_breakdown).sort((a, b) => b[1] - a[1])
  const maxDefectCount = defectEntries.length > 0 ? defectEntries[0][1] : 1
  const projectEntries = Object.entries(data.project_breakdown).sort((a, b) => b[1] - a[1])

  return (
    <div className="analytics-view">
      <div className="analytics-top-bar">
        <div>
          <h3>Audit Executive Summary</h3>
          <p className="section-note">
            Real-time compliance monitoring across field audits and retail chiller units
          </p>
        </div>
        <button type="button" className="btn small secondary" onClick={loadStats}>
          🔄 Refresh Metrics
        </button>
      </div>

      {/* KPI Cards Grid */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-icon-wrap icon-blue">📋</div>
          <div className="kpi-info">
            <span className="kpi-label">Total Audits</span>
            <span className="kpi-value">{data.total_audits}</span>
            <span className="kpi-hint">Processed and logged</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon-wrap icon-green">✅</div>
          <div className="kpi-info">
            <span className="kpi-label">Compliance Rate</span>
            <span className="kpi-value">{data.compliance_rate}%</span>
            <span className="kpi-hint">{data.clean_audits} of {data.total_audits} defect-free</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon-wrap icon-red">⚠️</div>
          <div className="kpi-info">
            <span className="kpi-label">Defects Flagged</span>
            <span className="kpi-value">{data.total_defects}</span>
            <span className="kpi-hint">Across all retail displays</span>
          </div>
        </div>

        <div className="kpi-card">
          <div className="kpi-icon-wrap icon-purple">🎯</div>
          <div className="kpi-info">
            <span className="kpi-label">Objects Identified</span>
            <span className="kpi-value">{data.total_objects_detected}</span>
            <span className="kpi-hint">Average confidence: {Math.round(data.avg_confidence * 100)}%</span>
          </div>
        </div>
      </div>

      {/* Analytics Breakdown Grid */}
      <div className="analytics-details-grid">
        {/* Defect Frequency Card */}
        <div className="analytics-card">
          <h4>Frequent Defect Classifications</h4>
          <p className="card-desc">
            Visual inspection failures classified by YOLOv8 model inference
          </p>

          {defectEntries.length === 0 ? (
            <div className="empty-substate">
              <p>No defects recorded yet in the database.</p>
            </div>
          ) : (
            <div className="chart-bar-list">
              {defectEntries.map(([name, count]) => {
                const percentage = Math.round((count / maxDefectCount) * 100)
                return (
                  <div key={name} className="chart-bar-row">
                    <div className="bar-labels">
                      <span className="bar-title">{name}</span>
                      <span className="bar-value">
                        {count} occurrence{count === 1 ? '' : 's'}
                      </span>
                    </div>
                    <div className="bar-track">
                      <div
                        className="bar-fill fill-danger"
                        style={{ width: `${Math.max(8, percentage)}%` }}
                      ></div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        {/* Audit Projects Card */}
        <div className="analytics-card">
          <h4>Audits by Inspection Profile</h4>
          <p className="card-desc">Volume of images analyzed per client initiative</p>

          {projectEntries.length === 0 ? (
            <div className="empty-substate">
              <p>No profile activity recorded.</p>
            </div>
          ) : (
            <div className="chart-bar-list">
              {projectEntries.map(([proj, count]) => {
                const pct = Math.round((count / data.total_audits) * 100)
                return (
                  <div key={proj} className="chart-bar-row">
                    <div className="bar-labels">
                      <span className="bar-title uppercase-tag">{proj}</span>
                      <span className="bar-value">{count} ({pct}%)</span>
                    </div>
                    <div className="bar-track">
                      <div
                        className="bar-fill fill-primary"
                        style={{ width: `${Math.max(8, pct)}%` }}
                      ></div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

