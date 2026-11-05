import type { ActiveTab } from '../types'

interface SidebarProps {
  activeTab: ActiveTab
  onTabChange: (tab: ActiveTab) => void
  isCollapsed: boolean
  onToggleCollapse: () => void
  totalHistory: number
  theme: 'light' | 'dark'
  onToggleTheme: () => void
}

export default function Sidebar({
  activeTab,
  onTabChange,
  isCollapsed,
  onToggleCollapse,
  totalHistory,
  theme,
  onToggleTheme,
}: SidebarProps) {
  const navItems: { id: ActiveTab; label: string; icon: string; badge?: number }[] = [
    { id: 'studio', label: 'Detection Studio', icon: '🎯' },
    { id: 'analytics', label: 'Audit Analytics', icon: '📊' },
    { id: 'history', label: 'Audit History', icon: '🗄️', badge: totalHistory },
    { id: 'models', label: 'Model Registry', icon: '🧠' },
    { id: 'api', label: 'API Reference', icon: '⚡' },
  ]

  return (
    <aside className={`app-sidebar ${isCollapsed ? 'collapsed' : ''}`}>
      {/* Brand Header */}
      <div className="sidebar-brand">
        <div className="brand-logo">
          <span className="logo-icon">🤖</span>
        </div>
        {!isCollapsed && (
          <div className="brand-text">
            <h2>ShelfVision AI</h2>
            <span className="brand-subtitle">Retail Intelligence Studio</span>
          </div>
        )}
        <button
          type="button"
          className="collapse-btn"
          onClick={onToggleCollapse}
          title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
          aria-label="Toggle navigation sidebar"
        >
          {isCollapsed ? '→' : '←'}
        </button>
      </div>

      {/* Navigation List */}
      <nav className="sidebar-nav">
        <ul>
          {navItems.map((item) => {
            const isActive = activeTab === item.id
            return (
              <li key={item.id}>
                <button
                  type="button"
                  className={`nav-item-btn ${isActive ? 'active' : ''}`}
                  onClick={() => onTabChange(item.id)}
                  title={isCollapsed ? item.label : undefined}
                >
                  <span className="nav-icon">{item.icon}</span>
                  {!isCollapsed && <span className="nav-label">{item.label}</span>}
                  {!isCollapsed && item.badge !== undefined && item.badge > 0 && (
                    <span className="nav-badge">{item.badge}</span>
                  )}
                </button>
              </li>
            )
          })}
        </ul>
      </nav>

      {/* Sidebar Footer */}
      <div className="sidebar-footer">
        {!isCollapsed && (
          <div className="engine-status-card">
            <div className="status-indicator">
              <span className="status-dot"></span>
              <span className="status-label">Engine Online</span>
            </div>
            <div className="engine-meta">YOLOv8 PyTorch • v1.0.0</div>
          </div>
        )}

        <div className="footer-controls">
          <button
            type="button"
            className="theme-toggle-btn"
            onClick={onToggleTheme}
            title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} mode`}
          >
            <span className="theme-icon">{theme === 'dark' ? '☀️' : '🌙'}</span>
            {!isCollapsed && (
              <span className="theme-text">
                {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
              </span>
            )}
          </button>
        </div>
      </div>
    </aside>
  )
}

