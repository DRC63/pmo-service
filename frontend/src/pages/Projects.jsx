import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { api } from '../api/client';
import DataTable from '../components/DataTable';
import RagBadge from '../components/RagBadge';
import Modal from '../components/Modal';
import ProjectForm from '../components/ProjectForm';

const CATEGORY_LABELS = {
  ai_infrastructure: 'AI Infrastructure',
  transformation: 'Transformation',
  banking: 'Banking',
  other: 'Other',
};

export default function Projects() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ category: '', rag_status: '' });
  const [showForm, setShowForm] = useState(false);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const [projectList, resourceList] = await Promise.all([
        api.listProjects(filters),
        api.listResources(),
      ]);
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
  }, [filters.category, filters.rag_status]);

  async function handleCreate(data) {
    await api.createProject(data);
    setShowForm(false);
    load();
  }

  const columns = [
    { key: 'name', label: 'Name', render: (p) => <strong>{p.name}</strong> },
    { key: 'code', label: 'Code' },
    { key: 'category', label: 'Category', render: (p) => CATEGORY_LABELS[p.category] || p.category },
    { key: 'owner_name', label: 'Owner', render: (p) => p.owner_name || '—' },
    { key: 'rag_status', label: 'RAG', render: (p) => <RagBadge status={p.rag_status} /> },
    { key: 'end_date', label: 'End date', render: (p) => p.end_date || '—' },
    { key: 'budget', label: 'Budget', numeric: true, render: (p) => (p.budget != null ? `$${Number(p.budget).toLocaleString()}` : '—') },
  ];

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Projects</h1>
          <p>Portfolio of active and past engagements.</p>
        </div>
        <button className="btn btn-accent" onClick={() => setShowForm(true)} type="button">
          + New Project
        </button>
      </div>

      <div className="filter-row">
        <select value={filters.category} onChange={(e) => setFilters((f) => ({ ...f, category: e.target.value }))}>
          <option value="">All categories</option>
          {Object.entries(CATEGORY_LABELS).map(([value, label]) => (
            <option key={value} value={value}>{label}</option>
          ))}
        </select>
        <select value={filters.rag_status} onChange={(e) => setFilters((f) => ({ ...f, rag_status: e.target.value }))}>
          <option value="">All RAG statuses</option>
          <option value="green">Green</option>
          <option value="amber">Amber</option>
          <option value="red">Red</option>
        </select>
      </div>

      {error && <p style={{ color: 'var(--color-danger)' }}>{error}</p>}
      {loading ? (
        <p className="muted">Loading…</p>
      ) : (
        <DataTable columns={columns} rows={projects} onRowClick={(p) => navigate(`/projects/${p.id}`)} emptyMessage="No projects match these filters." />
      )}

      {showForm && (
        <Modal title="New Project" onClose={() => setShowForm(false)}>
          <ProjectForm resources={resources} onSubmit={handleCreate} onCancel={() => setShowForm(false)} />
        </Modal>
      )}
    </div>
  );
}
