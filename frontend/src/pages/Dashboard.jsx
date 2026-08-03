// Dashboard page: the portfolio at a glance. Loads the aggregate summary from the
// backend (project and RAG counts, upcoming milestones, high-severity risks) and
// lays it out as stat cards and short lists. Read-only — no editing here.
import { useEffect, useState } from 'react';
import { Link } from 'react-router';
import { api } from '../api/client';
import StatCard from '../components/StatCard';
import RiskScoreBadge from '../components/RiskScoreBadge';

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.getDashboardSummary()
      .then(setSummary)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  // Guard clauses keep the render simple: the layout below can assume `summary` is
  // present, so it doesn't need per-field null checks.
  if (loading) return <p className="muted">Loading…</p>;
  if (error) return <p style={{ color: 'var(--color-danger)' }}>{error}</p>;
  if (!summary) return null;

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p>Portfolio health at a glance.</p>
        </div>
      </div>

      {/* Headline counts: total projects, the RAG breakdown, and overdue milestones. */}
      <div className="stat-row">
        <StatCard label="Total Projects" value={summary.total_projects} />
        <StatCard label="Green" value={summary.rag_counts.green ?? 0} />
        <StatCard label="Amber" value={summary.rag_counts.amber ?? 0} />
        <StatCard label="Red" value={summary.rag_counts.red ?? 0} />
        <StatCard label="Overdue Milestones" value={summary.overdue_milestones_count} />
      </div>

      <div className="form-grid">
        <div className="card">
          <h2 className="section-gap">Upcoming Milestones (next 30 days)</h2>
          {summary.upcoming_milestones.length === 0 ? (
            <p className="muted">Nothing due in the next 30 days.</p>
          ) : (
            <ul>
              {summary.upcoming_milestones.map((m) => (
                <li key={m.milestone_id} style={{ padding: '10px 0', borderBottom: '1px solid var(--color-bg-alt)' }}>
                  <Link to={`/projects/${m.project_id}`}><strong>{m.name}</strong></Link>
                  <div className="muted">{m.project_name} — due {m.due_date} ({m.days_until}d)</div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="card">
          <h2 className="section-gap">High-Severity Risks</h2>
          {summary.high_severity_risks.length === 0 ? (
            <p className="muted">No open high-severity risks.</p>
          ) : (
            <ul>
              {summary.high_severity_risks.map((r) => (
                <li key={r.risk_id} className="flex-row" style={{ padding: '10px 0', borderBottom: '1px solid var(--color-bg-alt)', justifyContent: 'space-between' }}>
                  <div>
                    <Link to={`/projects/${r.project_id}`}><strong>{r.title}</strong></Link>
                    <div className="muted">{r.project_name} — {r.status}</div>
                  </div>
                  <RiskScoreBadge score={r.score} />
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
