import { useEffect, useState } from 'react';
import { api } from '../api/client';
import DataTable from '../components/DataTable';
import RiskScoreBadge from '../components/RiskScoreBadge';
import Modal from '../components/Modal';
import RiskForm from '../components/RiskForm';

export default function Risks() {
  const [risks, setRisks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ project_id: '', status: '', min_score: '' });
  const [modal, setModal] = useState(null); // null | 'new' | risk object

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const [riskList, projectList, resourceList] = await Promise.all([
        api.listRisks(filters),
        api.listProjects(),
        api.listResources(),
      ]);
      setRisks(riskList);
      setProjects(projectList);
      setResources(resourceList);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters.project_id, filters.status, filters.min_score]);

  async function handleSave(data) {
    if (modal && modal !== 'new') {
      await api.updateRisk(modal.id, data);
    } else {
      await api.createRisk(data);
    }
    setModal(null);
    load();
  }

  async function handleDelete(risk) {
    if (!window.confirm(`Delete risk "${risk.title}"?`)) return;
    await api.deleteRisk(risk.id);
    load();
  }

  const columns = [
    { key: 'project_name', label: 'Project' },
    { key: 'title', label: 'Title' },
    { key: 'likelihood', label: 'L', numeric: true },
    { key: 'impact', label: 'I', numeric: true },
    { key: 'score', label: 'Score', render: (r) => <RiskScoreBadge score={r.score} /> },
    { key: 'status', label: 'Status' },
    { key: 'owner_name', label: 'Owner', render: (r) => r.owner_name || '—' },
    {
      key: 'actions',
      label: '',
      render: (r) => (
        <div className="flex-row">
          <button className="btn btn-outline btn-sm" onClick={(e) => { e.stopPropagation(); setModal(r); }} type="button">Edit</button>
          <button className="btn btn-outline btn-sm" onClick={(e) => { e.stopPropagation(); handleDelete(r); }} type="button">Delete</button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Risk Register</h1>
          <p>All risks across the portfolio, ranked by severity.</p>
        </div>
        <button className="btn btn-accent" onClick={() => setModal('new')} type="button">+ New Risk</button>
      </div>

      <div className="filter-row">
        <select value={filters.project_id} onChange={(e) => setFilters((f) => ({ ...f, project_id: e.target.value }))}>
          <option value="">All projects</option>
          {projects.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        <select value={filters.status} onChange={(e) => setFilters((f) => ({ ...f, status: e.target.value }))}>
          <option value="">All statuses</option>
          <option value="open">Open</option>
          <option value="mitigating">Mitigating</option>
          <option value="closed">Closed</option>
        </select>
        <select value={filters.min_score} onChange={(e) => setFilters((f) => ({ ...f, min_score: e.target.value }))}>
          <option value="">All scores</option>
          <option value="15">High severity (≥15)</option>
          <option value="8">Medium+ (≥8)</option>
        </select>
      </div>

      {error && <p style={{ color: 'var(--color-danger)' }}>{error}</p>}
      {loading ? <p className="muted">Loading…</p> : (
        <DataTable columns={columns} rows={risks} emptyMessage="No risks match these filters." />
      )}

      {modal && (
        <Modal title={modal === 'new' ? 'New Risk' : 'Edit Risk'} onClose={() => setModal(null)}>
          <RiskForm
            initial={modal === 'new' ? null : modal}
            projects={projects}
            resources={resources}
            onSubmit={handleSave}
            onCancel={() => setModal(null)}
          />
        </Modal>
      )}
    </div>
  );
}
