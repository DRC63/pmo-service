import { Link } from 'react-router';

const CATEGORIES = [
  { value: 'ai_infrastructure', label: 'AI Infrastructure' },
  { value: 'transformation', label: 'Transformation' },
  { value: 'banking', label: 'Banking' },
  { value: 'other', label: 'Other' },
];

export default function Settings() {
  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Settings</h1>
          <p>Reference data and application configuration.</p>
        </div>
      </div>

      <div className="card section-gap" style={{ borderLeft: '4px solid var(--color-accent)' }}>
        <h2 className="section-gap">No Authentication (v1)</h2>
        <p>
          This is a single-user, localhost-only internal tool. There is no login and no per-user
          permissions in this version — anyone with access to this machine can view and edit all data.
          Add authentication before exposing this app beyond your own machine.
        </p>
      </div>

      <div className="card section-gap">
        <h2 className="section-gap">Resources</h2>
        <p className="section-gap">Manage the people/roles used across projects, allocations, and risk ownership.</p>
        <Link to="/resources" className="btn btn-primary">Manage Resources</Link>
      </div>

      <div className="card">
        <h2 className="section-gap">Project Categories</h2>
        <p className="section-gap">
          Categories are a fixed list in v1 — editable category management can be added later if needed.
        </p>
        <ul>
          {CATEGORIES.map((c) => (
            <li key={c.value} style={{ padding: '6px 0' }}>{c.label}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
