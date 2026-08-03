import { useState } from 'react';

// The milestone table on a project's detail page: lists milestones (flagging any
// overdue), lets the status be changed inline, delete a row, and add a new one via
// the form at the bottom. It holds only the new-milestone form fields; every change
// is reported to the parent through onCreate/onUpdate/onDelete, which own the API
// calls and the reload.
const STATUS_OPTIONS = ['not_started', 'in_progress', 'complete', 'late'];

export default function MilestoneList({ milestones, onCreate, onUpdate, onDelete }) {
  const [newName, setNewName] = useState('');
  const [newDue, setNewDue] = useState('');
  const [adding, setAdding] = useState(false);

  // Add a milestone from the inline form. New milestones start "not started"; the
  // due date is optional. `adding` disables the button so a slow save can't be
  // double-submitted.
  async function handleAdd(e) {
    e.preventDefault();
    if (!newName) return;
    setAdding(true);
    try {
      await onCreate({ name: newName, due_date: newDue || null, status: 'not_started' });
      setNewName('');
      setNewDue('');
    } finally {
      setAdding(false);
    }
  }

  return (
    <div>
      <div className="data-table-wrap section-gap">
        {milestones.length === 0 ? (
          <div className="data-table-empty">No milestones yet.</div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Due date</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {milestones.map((m) => (
                <tr key={m.id}>
                  <td>
                    {m.name}
                    {m.is_overdue && <span className="badge badge-red" style={{ marginLeft: 8 }}>Overdue</span>}
                  </td>
                  <td>{m.due_date || '—'}</td>
                  <td>
                    <select
                      value={m.status}
                      onChange={(e) => onUpdate(m.id, { status: e.target.value })}
                    >
                      {STATUS_OPTIONS.map((s) => (
                        <option key={s} value={s}>{s.replace('_', ' ')}</option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <button className="btn btn-outline btn-sm" onClick={() => onDelete(m.id)} type="button">
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
      <form onSubmit={handleAdd} className="flex-row">
        <input
          placeholder="New milestone name"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          style={{ flexGrow: 1, padding: '9px 14px', borderRadius: 8, border: '1.5px solid rgba(45,52,54,0.15)' }}
        />
        <input
          type="date"
          value={newDue}
          onChange={(e) => setNewDue(e.target.value)}
          style={{ padding: '9px 14px', borderRadius: 8, border: '1.5px solid rgba(45,52,54,0.15)' }}
        />
        <button className="btn btn-accent btn-sm" type="submit" disabled={adding}>Add</button>
      </form>
    </div>
  );
}
