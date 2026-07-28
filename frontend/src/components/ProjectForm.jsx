import { useState } from 'react';

const CATEGORIES = [
  { value: 'ai_infrastructure', label: 'AI Infrastructure' },
  { value: 'transformation', label: 'Transformation' },
  { value: 'banking', label: 'Banking' },
  { value: 'other', label: 'Other' },
];

const RAG_OPTIONS = ['green', 'amber', 'red'];

export default function ProjectForm({ initial, resources, onSubmit, onCancel }) {
  const [form, setForm] = useState({
    name: initial?.name || '',
    code: initial?.code || '',
    category: initial?.category || 'other',
    owner_resource_id: initial?.owner_resource_id ?? '',
    start_date: initial?.start_date || '',
    end_date: initial?.end_date || '',
    budget: initial?.budget ?? '',
    actual_spend: initial?.actual_spend ?? 0,
    rag_status: initial?.rag_status || 'green',
    description: initial?.description || '',
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
        owner_resource_id: form.owner_resource_id === '' ? null : Number(form.owner_resource_id),
        start_date: form.start_date || null,
        end_date: form.end_date || null,
        budget: form.budget === '' ? null : Number(form.budget),
        actual_spend: Number(form.actual_spend || 0),
      });
    } catch (err) {
      setError(err.message);
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <p style={{ color: 'var(--color-danger)' }}>{error}</p>}
      <div className="form-grid">
        <div className="form-field">
          <label>Name</label>
          <input required value={form.name} onChange={(e) => update('name', e.target.value)} />
        </div>
        <div className="form-field">
          <label>Code</label>
          <input required value={form.code} onChange={(e) => update('code', e.target.value)} />
        </div>
        <div className="form-field">
          <label>Category</label>
          <select value={form.category} onChange={(e) => update('category', e.target.value)}>
            {CATEGORIES.map((c) => (
              <option key={c.value} value={c.value}>{c.label}</option>
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
        <div className="form-field">
          <label>RAG status</label>
          <select value={form.rag_status} onChange={(e) => update('rag_status', e.target.value)}>
            {RAG_OPTIONS.map((s) => (
              <option key={s} value={s}>{s[0].toUpperCase() + s.slice(1)}</option>
            ))}
          </select>
        </div>
        <div className="form-field">
          <label>Start date</label>
          <input type="date" value={form.start_date} onChange={(e) => update('start_date', e.target.value)} />
        </div>
        <div className="form-field">
          <label>End date</label>
          <input type="date" value={form.end_date} onChange={(e) => update('end_date', e.target.value)} />
        </div>
        <div className="form-field">
          <label>Budget</label>
          <input type="number" step="0.01" value={form.budget} onChange={(e) => update('budget', e.target.value)} />
        </div>
        <div className="form-field">
          <label>Actual spend</label>
          <input type="number" step="0.01" value={form.actual_spend} onChange={(e) => update('actual_spend', e.target.value)} />
        </div>
      </div>
      <div className="form-field">
        <label>Description</label>
        <textarea rows={3} value={form.description} onChange={(e) => update('description', e.target.value)} />
      </div>
      <div className="form-actions">
        <button type="button" className="btn btn-outline" onClick={onCancel}>Cancel</button>
        <button type="submit" className="btn btn-primary" disabled={saving}>
          {saving ? 'Saving…' : 'Save Project'}
        </button>
      </div>
    </form>
  );
}
