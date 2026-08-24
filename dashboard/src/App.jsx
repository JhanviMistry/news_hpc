import "./App.css";

function App() {
  return (
    <div className="app">

      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <div className="logo-mark">N</div>
          <span>NewsPulse</span>
        </div>

        <nav>
          <a className="nav-item active">
            <span>◉</span>
            Dashboard
          </a>

          <a className="nav-item">
            <span>▣</span>
            Signals
          </a>

          <a className="nav-item">
            <span>◷</span>
            History
          </a>
        </nav>

        <div className="sidebar-bottom">
          <div className="system-status">
            <span className="status-dot"></span>
            <div>
              <strong>System Online</strong>
              <small>Kafka · Redis · PostgreSQL</small>
            </div>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="main">

        {/* Header */}
        <header className="header">
          <div>
            <h1>Market Intelligence</h1>
            <p>Real-time news signal monitoring</p>
          </div>

          <div className="live-indicator">
            <span className="live-dot"></span>
            LIVE
          </div>
        </header>

        {/* KPI Cards */}
        <section className="stats-grid">

          <div className="stat-card">
            <span className="stat-label">Signals Processed</span>
            <strong className="stat-value">20</strong>
            <span className="stat-change positive">
              ↑ Live
            </span>
          </div>

          <div className="stat-card">
            <span className="stat-label">Average Impact</span>
            <strong className="stat-value">0.14</strong>
            <span className="stat-change positive">
              ↑ 8.4%
            </span>
          </div>

          <div className="stat-card">
            <span className="stat-label">Positive Signals</span>
            <strong className="stat-value">42%</strong>
            <span className="stat-change">
              Current
            </span>
          </div>

          <div className="stat-card">
            <span className="stat-label">Consumer Status</span>
            <strong className="stat-value status-online">
              Online
            </strong>
            <span className="stat-change positive">
              ● Healthy
            </span>
          </div>

        </section>

        {/* Main grid */}
        <section className="content-grid">

          {/* Top Signals */}
          <div className="panel signals-panel">

            <div className="panel-header">
              <div>
                <h2>Top Signals</h2>
                <p>Highest market impact</p>
              </div>

              <button>View all →</button>
            </div>

            <div className="signal-list">

              <div className="signal-row">
                <div className="signal-symbol positive-bg">
                  A
                </div>

                <div className="signal-info">
                  <strong>AAPL</strong>
                  <span>Positive market sentiment</span>
                </div>

                <div className="signal-impact positive">
                  +0.82
                </div>

                <span className="badge high">
                  HIGH
                </span>
              </div>

              <div className="signal-row">
                <div className="signal-symbol negative-bg">
                  N
                </div>

                <div className="signal-info">
                  <strong>NVDA</strong>
                  <span>Negative market sentiment</span>
                </div>

                <div className="signal-impact negative">
                  -0.71
                </div>

                <span className="badge high">
                  HIGH
                </span>
              </div>

              <div className="signal-row">
                <div className="signal-symbol positive-bg">
                  M
                </div>

                <div className="signal-info">
                  <strong>MSFT</strong>
                  <span>Positive market sentiment</span>
                </div>

                <div className="signal-impact positive">
                  +0.63
                </div>

                <span className="badge medium">
                  MEDIUM
                </span>
              </div>

              <div className="signal-row">
                <div className="signal-symbol negative-bg">
                  T
                </div>

                <div className="signal-info">
                  <strong>TSLA</strong>
                  <span>Negative market sentiment</span>
                </div>

                <div className="signal-impact negative">
                  -0.55
                </div>

                <span className="badge medium">
                  MEDIUM
                </span>
              </div>

            </div>
          </div>

          {/* System Overview */}
          <div className="panel">

            <div className="panel-header">
              <div>
                <h2>Pipeline Status</h2>
                <p>Infrastructure health</p>
              </div>
            </div>

            <div className="pipeline">

              <div className="pipeline-item">
                <div className="pipeline-icon">K</div>
                <div>
                  <strong>Kafka</strong>
                  <span>Message streaming</span>
                </div>
                <span className="healthy">Healthy</span>
              </div>

              <div className="pipeline-item">
                <div className="pipeline-icon">R</div>
                <div>
                  <strong>Redis</strong>
                  <span>Hot signal cache</span>
                </div>
                <span className="healthy">Healthy</span>
              </div>

              <div className="pipeline-item">
                <div className="pipeline-icon">P</div>
                <div>
                  <strong>PostgreSQL</strong>
                  <span>Historical storage</span>
                </div>
                <span className="healthy">Healthy</span>
              </div>

              <div className="pipeline-item">
                <div className="pipeline-icon">F</div>
                <div>
                  <strong>FastAPI</strong>
                  <span>API service</span>
                </div>
                <span className="healthy">Healthy</span>
              </div>

            </div>
          </div>

        </section>

        {/* Recent activity */}
        <section className="panel activity-panel">

          <div className="panel-header">
            <div>
              <h2>Recent Activity</h2>
              <p>Latest processed news signals</p>
            </div>

            <span className="activity-live">
              ● Streaming
            </span>
          </div>

          <div className="activity-placeholder">
            <div className="activity-icon">↯</div>
            <strong>Real-time feed coming next</strong>
            <span>
              This panel will connect directly to your Kafka →
              FastAPI pipeline.
            </span>
          </div>

        </section>

      </main>
    </div>
  );
}

export default App;