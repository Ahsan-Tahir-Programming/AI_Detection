import type { ModelDetail } from '../types'

interface ModelRegistryViewProps {
  modelsDetails: ModelDetail[]
  activeModel: string
  onSelectModel: (name: string) => void
}

const SUPPORTED_ZYN_CLASSES = [
  { name: 'Backlit Not Functional', color: '#ff0000', mapped: 'backlit_not_functional' },
  { name: 'Backlit Functional', color: '#00ff00', mapped: 'backlit_functional' },
  { name: 'BWU Damage', color: '#ffa500', mapped: 'sheet_damaged' },
  { name: 'Compartment', color: '#0000ff', mapped: 'compartment' },
  { name: 'CAN Compartment Damage', color: '#ff00ff', mapped: 'compartment_damage' },
  { name: 'Paint Fade Off', color: '#ffff00', mapped: 'paint_fade_off' },
  { name: 'Visibility Hidden With Others Items', color: '#800080', mapped: 'Visibility_hidden_other_items' },
  { name: 'ZYN Logo Damage', color: '#ff1493', mapped: 'logo_damage' },
  { name: 'Asset Available Not Deployed', color: '#00ffff', mapped: 'non_compliant' },
]

export default function ModelRegistryView({
  modelsDetails,
  activeModel,
  onSelectModel,
}: ModelRegistryViewProps) {
  return (
    <div className="models-view">
      <div className="section-header-row">
        <div>
          <h3>Registered Computer Vision Models</h3>
          <p className="section-note">
            Pretrained YOLO weights discovered on disk and available for real-time inference
          </p>
        </div>
      </div>

      <div className="models-grid">
        {modelsDetails.map((model) => {
          const isSelected = activeModel.toLowerCase() === model.name.toLowerCase()
          return (
            <div
              key={model.name}
              className={`model-card ${isSelected ? 'model-card-active' : ''}`}
            >
              <div className="model-card-header">
                <div>
                  <h4 className="model-title">{model.name.toUpperCase()} (YOLOv8)</h4>
                  <span className="model-filename"><code>{model.filename}</code></span>
                </div>
                <span className={`model-badge ${model.loaded ? 'badge-loaded' : 'badge-standby'}`}>
                  {model.loaded ? '● In-Memory' : '○ Standby'}
                </span>
              </div>

              <div className="model-metrics-grid">
                <div className="model-metric">
                  <span className="m-label">File Size</span>
                  <span className="m-val">{model.size_mb} MB</span>
                </div>
                <div className="model-metric">
                  <span className="m-label">Task</span>
                  <span className="m-val">Object Detection</span>
                </div>
                <div className="model-metric">
                  <span className="m-label">Base Image Size</span>
                  <span className="m-val">640 × 640 px</span>
                </div>
                <div className="model-metric">
                  <span className="m-label">Inference Device</span>
                  <span className="m-val">CPU / ThreadPool</span>
                </div>
              </div>

              <div className="model-classes-section">
                <h5>Detectable Class Labels ({SUPPORTED_ZYN_CLASSES.length})</h5>
                <div className="class-tags-cloud">
                  {SUPPORTED_ZYN_CLASSES.map((cls) => (
                    <span
                      key={cls.name}
                      className="class-chip"
                      style={{ borderLeftColor: cls.color }}
                      title={`Mapped to: ${cls.mapped}`}
                    >
                      <span className="chip-indicator" style={{ background: cls.color }}></span>
                      <span className="chip-label">{cls.name}</span>
                    </span>
                  ))}
                </div>
              </div>

              <div className="model-card-footer">
                {isSelected ? (
                  <span className="active-pill">✓ Currently Active in Studio</span>
                ) : (
                  <button
                    type="button"
                    className="btn small secondary"
                    onClick={() => onSelectModel(model.name)}
                  >
                    Activate in Studio
                  </button>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

