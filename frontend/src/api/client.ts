import type {
  DetectionFormData,
  DetectionData,
  ModelsResponse,
  PaginatedGalleryResponse,
  AnalyticsResponse,
} from '../types'

export const API_BASE = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

/**
 * Fetch list of discovered and loaded YOLO models from backend.
 */
export async function fetchModels(): Promise<ModelsResponse> {
  const res = await fetch(`${API_BASE}/models`)
  if (!res.ok) {
    throw new Error(`Failed to fetch models: HTTP ${res.status}`)
  }
  return res.json()
} 

/**
 * Run object detection via image URL.
 */
export async function detectViaUrl(data: DetectionFormData): Promise<DetectionData> {
  const payload = {
    modelname: data.modelname,
    project: data.project,
    routeId: data.routeId,
    imageKey: data.imageKey,
    imageUrl: data.imageUrl,
    categoryName: data.categoryName,
    visitDate: data.visitDate,
    confidence: data.confidence,
    iou: data.iou,
  }

  const res = await fetch(`${API_BASE}/detect/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  const json = await res.json()
  if (!res.ok) {
    const errorMsg = json.detail || json.error || `Detection failed: HTTP ${res.status}`
    throw new Error(errorMsg)
  }
  return json
}

/**
 * Run object detection via direct file upload.
 */
export async function detectViaUpload(
  file: File,
  data: DetectionFormData
): Promise<DetectionData> {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('modelname', data.modelname)
  formData.append('project', data.project)
  formData.append('routeId', data.routeId)
  formData.append('imageKey', data.imageKey)
  formData.append('categoryName', data.categoryName)
  if (data.visitDate) {
    formData.append('visitDate', data.visitDate)
  }
  if (data.confidence !== undefined) {
    formData.append('confidence', data.confidence.toString())
  }
  if (data.iou !== undefined) {
    formData.append('iou', data.iou.toString())
  }

  const res = await fetch(`${API_BASE}/detect/upload`, {
    method: 'POST',
    body: formData,
  })

  const json = await res.json()
  if (!res.ok) {
    const errorMsg = json.detail || json.error || `Upload detection failed: HTTP ${res.status}`
    throw new Error(errorMsg)
  }
  return json
}

/**
 * Fetch paginated saved detections.
 */
export async function fetchDetections(
  page: number = 1,
  pageSize: number = 12
): Promise<PaginatedGalleryResponse> {
  const res = await fetch(`${API_BASE}/detections/?page=${page}&page_size=${pageSize}`)
  if (!res.ok) {
    throw new Error(`Failed to load gallery: HTTP ${res.status}`)
  }
  return res.json()
}

/**
 * Delete a detection record by requestId.
 */
export async function deleteDetection(requestId: string): Promise<boolean> {
  const res = await fetch(`${API_BASE}/detections/${encodeURIComponent(requestId)}`, {
    method: 'DELETE',
  })
  if (!res.ok) {
    throw new Error(`Failed to delete record: HTTP ${res.status}`)
  }
  return true
}

/**
 * Fetch high-level analytics over all historical audits.
 */
export async function fetchAnalytics(): Promise<AnalyticsResponse> {
  const res = await fetch(`${API_BASE}/analytics/stats`)
  if (!res.ok) {
    throw new Error(`Failed to load analytics: HTTP ${res.status}`)
  }
  return res.json()
}

/**
 * Generate secure download URL for an image filename.
 */
export function getDownloadUrl(filename: string): string {
  return `${API_BASE}/download-image/${encodeURIComponent(filename)}`
}
