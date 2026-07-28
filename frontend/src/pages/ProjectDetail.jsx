import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router';
import { api } from '../api/client';
import RagBadge from '../components/RagBadge';
import RiskScoreBadge from '../components/RiskScoreBadge';
import Modal from '../components/Modal';
import ProjectForm from '../components/ProjectForm';
import RiskForm from '../components/RiskForm';
import MilestoneList from '../components/MilestoneList';

export default function ProjectDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showEditForm, setShowEditForm] = useState(false);
  const [riskModal, setRiskModal] = useState(null); // null | 'new' | risk object
  const [newAlloc, setNewAlloc] = useState({ resource_id: '', allocation_pct: 50, start_date: '', end_date: '' });

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const [proj, res] = await Promise.all([api.getProject(id), api.listResources()]);
      setProject(proj);
      setResources(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  if (loading) return <p className="muted">Loading…</p>;
  if (error) return <p style={{ color: 'var(--color-danger)' }}>{error}</p>;
  if (!project) return null;

  async function handleUpdate(data) {
    await api.updateProject(id, data);
    setShowEditForm(false);
    load();
  }

  async function handleDelete() {
    if (!window.confirm(`Delete project "${project.name}"? This also removes its milestones, risks, and allocations.`)) return;
    await api.deleteProject(id);
    navigate('/projects');
  }

  async function handleRagChange(newRag) {
    await api.updateProject(id, { rag_status: newRag });
    load();
  }

  async function handleAddMilestone(data) {
    await api.createMilestone(id, data);
    load();
  }
  async function handleUpdateMilestone(milestoneId, data) {
    await api.updateMilestone(milestoneId, data);
    load();
  }
  async function handleDeleteMilestone(milestoneId) {
    await api.deleteMilestone(milestoneId);
    load();
  }

  async function handleSaveRisk(data) {
    if (riskModal && riskModal !== 'new') {
      await api.updateRisk(riskModal.id, data);
    } else {
      await api.createRisk(data);
    }
    setRiskModal(null);
    load();
  }
  async function handleDeleteRisk(riskId) {
    if (!window.confirm('Delete this risk?')) return;
    await api.deleteRisk(riskId);
    load();
  }

  async function handleAddAllocation(e) {
    e.preventDefault();
    if (!newAlloc.resource_id) return;
    await api.createAllocation({
      resource_id: Number(newAlloc.resource_id),
      project_id: Number(id),
      allocation_pct: Number(newAlloc.allocation_pct),
      start_date: newAlloc.start_date || null,
      end_date: newAlloc.end_date || null,
    });
    setNewAlloc({ resource_id: '', allocation_pct: 50, start_date: '', end_date: '' });
    load();
  }
  async function handleDeleteAllocation(allocId) {
    await api.deleteAllocation(allocId);
    load();
  }

  const availableResources = resources.filter(
    (r) => !project.allocations.some((a) => a.resource_id === r.id)
  );

  return (
    <div>
      <div className="page-header">
        <div>
          <div className="flex-row">
            <h1>{project.name}</h1>
            <span className="muted">{project.code}</span>
          </div>
          <p>{project.description || 'No description yet.'}</p>
        </div>
        <div className="flex-row">
          <button className="btn btn-outline" onClick={() => setShowEditForm(true)} type="button">Edit</button>
          <button className="btn btn-danger" onClick={handleDelete} type="button">Delete</button>
        </div>
      </div>

      <div className="stat-row">
        <div className="stat-card">
          <div className="stat-label">RAG status</div>
          <select
            value={project.rag_status}
            onChange={(e) => handleRagChange(e.target.value)}
            style={{ marginTop: 6, padding: '6px 10px', borderRadius: 8 }}
          >
            <option value="green">Green</option>
            <option value="amber">Amber</option>
            <option value="red">Red</option>
          </select>
        </div>
        <div className="stat-card">
          <div className="stat-label">Owner</div>
          <div className="stat-value" style={{ fontSize: '1.1rem' }}>{project.owner_name || '—'}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Dates</div>
          <div className="stat-value" style={{ fontSize: '1rem' }}>{project.start_date || '?'} → {project.end_date || '?'}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Budget vs Actual</div>
          <div className="stat-value" style={{ fontSize: '1rem' }}>
            ${Number(project.actual_spend).toLocaleString()} / {project.budget != null ? `$${Number(project.budget).toLocaleString()}` : '—'}
          </div>
        </div>
      </div>

      <div className="card section-gap">
        <h2 className="section-gap">Milestones</h2>
        <MilestoneList
          milestones={project.milestones}
          onCreate={handleAddMilestone}
          onUpdate={handleUpdateMilestone}
          onDelete={handleDeleteMilestone}
        />
      </div>

      <div className="card section-gap">
        <div className="page-header">
          <h2>Risks</h2>
          <button className="btn btn-accent btn-sm" onClick={() => setRiskModal('new')} type="button">+ New Risk</button>
        </div>
        {project.risks.length === 0 ? (
          <div className="data-table-empty">No risks logged yet.</div>
        ) : (
          <div className="data-table-wrap">
            <table className="data-table">
              <thead>
                <tr><th>Title</th><th>Score</th><th>Status</th><th>Owner</th><th></th></tr>
              </thead>
              <tbody>
                {project.risks.map((r) => (
                  <tr key={r.id}>
                    <td>{r.title}</td>
                    <td><RiskScoreBadge score={r.score} /></td>
                    <td>{r.status}</td>
                    <td>{r.owner_name || '—'}</td>
                    <td className="flex-row">
                      <button className="btn btn-outline btn-sm" onClick={() => setRiskModal(r)} type="button">Edit</button>
                      <button className="btn btn-outline btn-sm" onClick={() => handleDeleteRisk(r.id)} type="button">Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="card section-gap">
        <h2 className="section-gap">Resource Allocations</h2>
        {project.allocations.length === 0 ? (
          <div className="data-table-empty section-gap">No resources allocated yet.</div>
        ) : (
          <div className="data-table-wrap section-gap">
            <table className="data-table">
              <thead><tr><th>Resource</th><th>Allocation %</th><th>Start</th><th>End</th><th></th></tr></thead>
              <tbody>
                {project.allocations.map((a) => (
                  <tr key={a.id}>
                    <td>{a.resource_name}</td>
                    <td>{a.allocation_pct}%</td>
                    <td>{a.start_date || '—'}</td>
                    <td>{a.end_date || '—'}</td>
                    <td>
                      <button className="btn btn-outline btn-sm" onClick={() => handleDeleteAllocation(a.id)} type="button">Remove</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {availableResources.length > 0 && (
          <form onSubmit={handleAddAllocation} className="flex-row">
            <select
              value={newAlloc.resource_id}
              onChange={(e) => setNewAlloc((a) => ({ ...a, resource_id: e.target.value }))}
              required
            >
              <option value="">Select resource…</option>
              {availableResources.map((r) => (
                <option key={r.id} value={r.id}>{r.name}</option>
              ))}
            </select>
            <input
              type="number"
              min={0}
              max={200}
              value={newAlloc.allocation_pct}
              onChange={(e) => setNewAlloc((a) => ({ ...a, allocation_pct: e.target.value }))}
              style={{ width: 80, padding: '9px 10px', borderRadius: 8, border: '1.5px solid rgba(45,52,54,0.15)' }}
            />
            <span className="muted">%</span>
            <button className="btn btn-accent btn-sm" type="submit">Add Allocation</button>
          </form>
        )}
      </div>

      {showEditForm && (
        <Modal title="Edit Project" onClose={() => setShowEditForm(false)}>
          <ProjectForm initial={project} resources={resources} onSubmit={handleUpdate} onCancel={() => setShowEditForm(false)} />
        </Modal>
      )}

      {riskModal && (
        <Modal title={riskModal === 'new' ? 'New Risk' : 'Edit Risk'} onClose={() => setRiskModal(null)}>
          <RiskForm
            initial={riskModal === 'new' ? null : riskModal}
            resources={resources}
            fixedProjectId={Number(id)}
            onSubmit={handleSaveRisk}
            onCancel={() => setRiskModal(null)}
          />
        </Modal>
      )}
    </div>
  );
}
