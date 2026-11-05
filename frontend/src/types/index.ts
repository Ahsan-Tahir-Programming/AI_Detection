export interface DetectionCoordinates {
  x: number
  y: number
  w: number
  h: number
}

export interface DetectedItem {
  class_id: number
  class_name: string
  confidence: number
  bbox: number[]
  coordinates: DetectionCoordinates
}

export interface SKUInfo {
  detected: boolean
  count?: number
  coordinates?: DetectionCoordinates[]
}

export interface DetectionData {
  id?: number
  requestId: string
  project: string
  routeId: string
  imageKey: string[]
  imageSize: number[]
  visitDate: string
  originalImageUrl: string
  processedImageUrl: string
  detectedSKU: Record<string, SKUInfo>
  detections: DetectedItem[]
  createdAt?: string
}

export interface DetectionResult {
  success: boolean
  data?: DetectionData
  error?: string
}

export interface DetectionFormData {
  modelname: string
  project: string
  imageKey: string
  imageUrl?: string
  imageFile?: File | null
  categoryName: string
  routeId: string
  visitDate: string
  confidence?: number
  iou?: number
}

export interface ModelDetail {
  name: string
  filename: string
  size_mb: number
  loaded: boolean
}

export interface ModelsResponse {
  models: string[]
  details: ModelDetail[]
}

export interface GalleryItem {
  id?: number
  requestId: string
  processedImageUrl: string
  originalImageUrl: string
  project?: string
  routeId?: string
  imageKey?: string[]
  visitDate?: string
  detections?: DetectedItem[]
  createdAt?: string
}

export interface PaginatedGalleryResponse {
  success: boolean
  data: {
    items: GalleryItem[]
    total: number
  }
}

export interface AnalyticsData {
  total_audits: number
  total_objects_detected: number
  total_defects: number
  clean_audits: number
  compliance_rate: number
  avg_confidence: number
  defect_breakdown: Record<string, number>
  project_breakdown: Record<string, number>
}

export interface AnalyticsResponse {
  success: boolean
  data: AnalyticsData
}

export type ActiveTab = 'studio' | 'analytics' | 'history' | 'models' | 'api'

