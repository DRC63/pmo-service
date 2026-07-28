import { useEffect, useState } from 'react';
import { api } from '../api/client';
import DataTable from '../components/DataTable';
import RagBadge from '../components/RagBadge';
import RiskScoreBadge from '../components/RiskScoreBadge';

const CATEGORY_LABELS = {
  ai_infrastructure: 'AI Infrastructure',
  transformation: 'Transformation',
  banking: 'Banking',
  other: 'Other',
};

function PortfolioSummary() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.getPortfolioReport()
      .then(setRows)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="muted">Loading…</p>;
  if (error) return <p style={{ color: 'var(--color-danger)' }}>{error}</p>;

  const columns = [
    { key: 'name', label: 'Project', render: (r) => <strong>{r.name}</strong> },
    { key: 'category', label: 'Category', render: (r) => CATEGORY_LABELS[r.category] || r.category },
    { key: 'rag_status', label: 'RAG', render: (r) => <RagBadge status={r.rag_status} /> },
    { key: 'owner_name', label: 'Owner', render: (r) => r.owner_name || '—' },
    { key: 'pct_milestones_complete', label: '% Milestones Complete', numeric: true, render: (r) => `${r.pct_milestones_complete}%` },
    { key: 'open_risk_count', label: 'Open Risks', numeric: true },
    { key: 'top_risk_score', label: 'Top Risk Score', render: (r) => <RiskScoreBadge score={r.top_risk_score} /> },
    { key: 'budget', label: 'Budget vs Actual', render: (r) => `$${Number(r.actual_spend).toLocaleString()} / ${r.budget != null ? `$${Number(r.budget).toLocaleString()}` : '—'}` },
  ];

  return <DataTable columns={columns} rows={rows} rowKey="project_id" emptyMessage="No projects yet." />;
}

function ProjectDetailReport({ projects }) {
  const [selectedId, setSelectedId] = useState(projects[0]?.id || '');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!selectedId) return;
    setLoading(true);
    setError(null);
    api.getProjectReport(selectedId)
      .then(setReport)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [selectedId]);

  return (
    <div>
      <div className="filter-row">
        <select value={selectedId} onChange={(e) => setSelectedId(e.target.value)}>
          {projects.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
      </div>

      {loading && <p className="muted">Loading…</p>}
      {error && <p style={{ color: 'var(--color-danger)' }}>{error}</p>}

      {report && (
        <div className="card" style={{ maxWidth: 720 }}>
          <div className="page-header">
            <div>
              <h2>{report.project.name}</h2>
              <p className="muted">{report.project.code} — {CATEGORY_LABELS[report.project.category] || report.project.category}</p>
            </div>
            <RagBadge status={report.project.rag_status} />
          </div>

          <div className="stat-row">
            <StatMini label="Owner" value={report.project.owner_name || '—'} />
            <StatMini label="Milestones complete" value={`${report.pct_milestones_complete}%`} />
            <StatMini label="Open risks" value={report.open_risk_count} />
            <StatMini label="Top risk score" value={report.top_risk_score} />
          </div>

          <h3 className="section-gap">Milestones</h3>
          <ul className="section-gap">
            {report.project.milestones.map((m) => (
              <li key={m.id} style={{ padding: '6px 0' }}>
                {m.name} — {m.due_date || 'no date'} — {m.status}
                {m.is_overdue && <span className="badge badge-red" style={{ marginLeft: 8 }}>Overdue</span>}
              </li>
            ))}
          </ul>

          <h3 className="section-gap">Risks</h3>
          <ul className="section-gap">
            {report.project.risks.map((r) => (
              <li key={r.id} style={{ padding: '6px 0' }}>
                {r.title} — score {r.score} — {r.status}
              </li>
            ))}
          </ul>

          <h3 className="section-gap">Allocations</h3>
          <ul>
            {report.project.allocations.map((a) => (
              <li key={a.id} style={{ padding: '6px 0' }}>{a.resource_name} — {a.allocation_pct}%</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function StatMini({ label, value }) {
  return (
    <div className="stat-card">
      <div className="stat-label">{label}</div>
      <div className="stat-value" style={{ fontSize: '1.15rem' }}>{value}</div>
    </div>
  );
}

export default function Reports() {
  const [tab, setTab] = useState('portfolio');
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    api.listProjects().then(setProjects);
  }, []);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Reports</h1>
          <p>Portfolio rollups and per-project status.</p>
        </div>
      </div>

      <div className="filter-row">
        <button className={`btn ${tab === 'portfolio' ? 'btn-primary' : 'btn-outline'}`} onClick={() => setTab('portfolio')} type="button">
          Portfolio Summary
        </button>
        <button className={`btn ${tab === 'project' ? 'btn-primary' : 'btn-outline'}`} onClick={() => setTab('project')} type="button">
          Project Detail
        </button>
      </div>

      {tab === 'portfolio' ? <PortfolioSummary /> : projects.length > 0 ? <ProjectDetailReport projects={projects} /> : <p className="muted">No projects yet.</p>}
    </div>
  );
}
