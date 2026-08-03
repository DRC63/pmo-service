// Create/edit form for a resource (a person): name, role, email, weekly capacity
// hours and the active flag. `initial` is null in create mode. onSubmit receives
// the payload; the parent performs the API call.
import { useState } from 'react';

export default function ResourceForm({ initial, onSubmit, onCancel }) {
  const [form, setForm] = useState({
    name: initial?.name || '',
    role: initial?.role || '',
    email: initial?.email || '',
    weekly_capacity_hours: initial?.weekly_capacity_hours ?? 40,
    active: initial?.active ?? true,
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  // Coerce capacity to a number (form inputs yield strings) and hand off to the
  // parent's onSubmit, which owns the create/update call. On error, surface the
  // message and re-enable the form so the user can retry.
  async function handleSubmit(e) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await onSubmit({ ...form, weekly_capacity_hours: Number(form.weekly_capacity_hours) });
    } catch (err) {
      setError(err.message);
      setSaving(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {error && <p style={{ color: 'var(--color-danger)' }}>{error}</p>}
      <div className="form-field">
        <label>Name</label>
        <input required value={form.name} onChange={(e) => update('name', e.target.value)} />
      </div>
      <div className="form-grid">
        <div className="form-field">
          <label>Role</label>
          <input value={form.role} onChange={(e) => update('role', e.target.value)} />
        </div>
        <div className="form-field">
          <label>Email</label>
          <input type="email" value={form.email} onChange={(e) => update('email', e.target.value)} />
        </div>
        <div className="form-field">
          <label>Weekly capacity (hours)</label>
          <input type="number" step="0.5" value={form.weekly_capacity_hours} onChange={(e) => update('weekly_capacity_hours', e.target.value)} />
        </div>
        <div className="form-field">
          <label>Active</label>
          <select value={form.active ? 'true' : 'false'} onChange={(e) => update('active', e.target.value === 'true')}>
            <option value="true">Active</option>
            <option value="false">Inactive</option>
          </select>
        </div>
      </div>
      <div className="form-actions">
        <button type="button" className="btn btn-outline" onClick={onCancel}>Cancel</button>
        <button type="submit" className="btn btn-primary" disabled={saving}>
          {saving ? 'Saving…' : 'Save Resource'}
        </button>
      </div>
    </form>
  );
}
