import { useState } from 'react';

const STATUS_OPTIONS = ['open', 'mitigating', 'closed'];

export default function RiskForm({ initial, projects, resources, fixedProjectId, onSubmit, onCancel }) {
  const [form, setForm] = useState({
    project_id: initial?.project_id ?? fixedProjectId ?? (projects?.[0]?.id || ''),
    title: initial?.title || '',
    description: initial?.description || '',
    likelihood: initial?.likelihood ?? 3,
    impact: initial?.impact ?? 3,
    status: initial?.status || 'open',
    mitigation_plan: initial?.mitigation_plan || '',
    owner_resource_id: initial?.owner_resource_id ?? '',
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await onSubmit({
        ...form,
        project_id: Number(form.project_id),
        likelihood: Number(form.likelihood),
        impact: Number(form.impact),
        owner_resource_id: form.owner_resource_id === '' ? null : Number(form.owner_resource_id),
      });
    } catch (err) {
      setError(err.message);
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <p style={{ color: 'var(--color-danger)' }}>{error}</p>}
      {!fixedProjectId && (
        <div className="form-field">
          <label>Project</label>
          <select required value={form.project_id} onChange={(e) => update('project_id', e.target.value)}>
            {projects.map((p) => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>
      )}
      <div className="form-field">
        <label>Title</label>
        <input required value={form.title} onChange={(e) => update('title', e.target.value)} />
      </div>
      <div className="form-field">
        <label>Description</label>
        <textarea rows={2} value={form.description} onChange={(e) => update('description', e.target.value)} />
      </div>
      <div className="form-grid">
        <div className="form-field">
          <label>Likelihood (1–5)</label>
          <input type="number" min={1} max={5} required value={form.likelihood} onChange={(e) => update('likelihood', e.target.value)} />
        </div>
        <div className="form-field">
          <label>Impact (1–5)</label>
          <input type="number" min={1} max={5} required value={form.impact} onChange={(e) => update('impact', e.target.value)} />
        </div>
        <div className="form-field">
          <label>Status</label>
          <select value={form.status} onChange={(e) => update('status', e.target.value)}>
            {STATUS_OPTIONS.map((s) => (
              <option key={s} value={s}>{s[0].toUpperCase() + s.slice(1)}</option>
            ))}
          </select>
        </div>
        <div className="form-field">
          <label>Owner</label>
          <select value={form.owner_resource_id} onChange={(e) => update('owner_resource_id', e.target.value)}>
            <option value="">— None —</option>
            {resources.map((r) => (
              <option key={r.id} value={r.id}>{r.name}</option>
            ))}
          </select>
        </div>
      </div>
      <div className="form-field">
        <label>Mitigation plan</label>
        <textarea rows={2} value={form.mitigation_plan} onChange={(e) => update('mitigation_plan', e.target.value)} />
      </div>
      <div className="form-actions">
        <button type="button" className="btn btn-outline" onClick={onCancel}>Cancel</button>
        <button type="submit" className="btn btn-primary" disabled={saving}>
          {saving ? 'Saving…' : 'Save Risk'}
        </button>
      </div>
    </form>
  );
}
