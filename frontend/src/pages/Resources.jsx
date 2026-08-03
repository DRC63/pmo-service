// Resources page: a table of people with their total allocation (an AllocationBar
// flags over-commitment), create/edit via the ResourceForm modal, and an expandable
// row that reveals a resource's per-project allocations.
import { useEffect, useState } from 'react';
import { api } from '../api/client';
import DataTable from '../components/DataTable';
import AllocationBar from '../components/AllocationBar';
import Modal from '../components/Modal';
import ResourceForm from '../components/ResourceForm';

export default function Resources() {
  const [resources, setResources] = useState([]);
  const [allocations, setAllocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [expandedId, setExpandedId] = useState(null);

  // Load people and their allocations together — the table needs both to show each
  // person's total commitment across projects. Runs on mount and after any change.
  async function load() {
    setLoading(true);
    setError(null);
    try {
      const [resourceList, allocationList] = await Promise.all([
        api.listResources(),
        api.listAllocations(),
      ]);
      setResources(resourceList);
      setAllocations(allocationList);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  // A resource's total commitment = the sum of its allocation percentages across
  // every project. This can exceed 100%, which is exactly the over-allocation the
  // AllocationBar highlights in red.
  function totalAllocationFor(resourceId) {
    return allocations
      .filter((a) => a.resource_id === resourceId)
      .reduce((sum, a) => sum + Number(a.allocation_pct), 0);
  }

  async function handleCreate(data) {
    await api.createResource(data);
    setShowForm(false);
    load();
  }

  async function handleUpdate(data) {
    await api.updateResource(editing.id, data);
    setEditing(null);
    load();
  }

  async function handleDelete(resource) {
    if (!window.confirm(`Delete resource "${resource.name}"?`)) return;
    await api.deleteResource(resource.id);
    load();
  }

  const columns = [
    { key: 'name', label: 'Name', render: (r) => <strong>{r.name}</strong> },
    { key: 'role', label: 'Role', render: (r) => r.role || '—' },
    { key: 'weekly_capacity_hours', label: 'Capacity (hrs/wk)', numeric: true },
    { key: 'allocation', label: 'Total Allocation', render: (r) => <AllocationBar pct={totalAllocationFor(r.id)} /> },
    { key: 'active', label: 'Status', render: (r) => (r.active ? <span className="badge badge-green">Active</span> : <span className="badge badge-grey">Inactive</span>) },
    {
      key: 'actions',
      label: '',
      // stopPropagation so clicking Edit/Delete doesn't also trigger the row's
      // click handler (which toggles the allocation detail open/closed).
      render: (r) => (
        <div className="flex-row">
          <button className="btn btn-outline btn-sm" onClick={(e) => { e.stopPropagation(); setEditing(r); }} type="button">Edit</button>
          <button className="btn btn-outline btn-sm" onClick={(e) => { e.stopPropagation(); handleDelete(r); }} type="button">Delete</button>
        </div>
      ),
    },
  ];

  // Clicking a row expands it to show that person's per-project allocations below
  // the table; clicking the same row again collapses it (expandedId → null).
  const expandedResource = resources.find((r) => r.id === expandedId);
  const expandedAllocations = allocations.filter((a) => a.resource_id === expandedId);

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Resources</h1>
          <p>People and their capacity across active engagements.</p>
        </div>
        <button className="btn btn-accent" onClick={() => setShowForm(true)} type="button">+ New Resource</button>
      </div>

      {error && <p style={{ color: 'var(--color-danger)' }}>{error}</p>}
      {loading ? (
        <p className="muted">Loading…</p>
      ) : (
        <>
          <DataTable
            columns={columns}
            rows={resources}
            onRowClick={(r) => setExpandedId(expandedId === r.id ? null : r.id)}
            emptyMessage="No resources yet."
          />

          {expandedResource && (
            <div className="card section-gap" style={{ marginTop: 20 }}>
              <h2 className="section-gap">{expandedResource.name} — Allocations</h2>
              {expandedAllocations.length === 0 ? (
                <p className="muted">Not currently allocated to any project.</p>
              ) : (
                <ul>
                  {expandedAllocations.map((a) => (
                    <li key={a.id} style={{ padding: '6px 0' }}>
                      {a.project_name} — {a.allocation_pct}%
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </>
      )}

      {showForm && (
        <Modal title="New Resource" onClose={() => setShowForm(false)}>
          <ResourceForm onSubmit={handleCreate} onCancel={() => setShowForm(false)} />
        </Modal>
      )}
      {editing && (
        <Modal title="Edit Resource" onClose={() => setEditing(null)}>
          <ResourceForm initial={editing} onSubmit={handleUpdate} onCancel={() => setEditing(null)} />
        </Modal>
      )}
    </div>
  );
}
