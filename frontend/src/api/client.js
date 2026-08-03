// API lives under the app's base path so it survives being served behind the
// shared front door: '/api' at the root, '/pmo/api' when built with APP_BASE.
const BASE = import.meta.env.BASE_URL.replace(/\/$/, '') + '/api';

// Single fetch wrapper behind every API call below. Sends JSON, and turns any
// non-2xx response into a thrown Error carrying the method, path, status and body
// so callers can surface a real message instead of a silent failure. A 204 (No
// Content, e.g. a successful delete) returns null rather than parsing an empty body.
async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`${options.method || 'GET'} ${path} failed (${res.status}): ${body}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

const get = (path) => request(path);
const post = (path, data) => request(path, { method: 'POST', body: JSON.stringify(data) });
const put = (path, data) => request(path, { method: 'PUT', body: JSON.stringify(data) });
const del = (path) => request(path, { method: 'DELETE' });

export const api = {
  // Projects
  listProjects: (params = {}) => get(`/projects${qs(params)}`),
  getProject: (id) => get(`/projects/${id}`),
  createProject: (data) => post('/projects', data),
  updateProject: (id, data) => put(`/projects/${id}`, data),
  deleteProject: (id) => del(`/projects/${id}`),

  // Milestones
  listMilestones: (projectId) => get(`/projects/${projectId}/milestones`),
  createMilestone: (projectId, data) => post(`/projects/${projectId}/milestones`, data),
  updateMilestone: (id, data) => put(`/milestones/${id}`, data),
  deleteMilestone: (id) => del(`/milestones/${id}`),

  // Resources
  listResources: (params = {}) => get(`/resources${qs(params)}`),
  getResource: (id) => get(`/resources/${id}`),
  createResource: (data) => post('/resources', data),
  updateResource: (id, data) => put(`/resources/${id}`, data),
  deleteResource: (id) => del(`/resources/${id}`),

  // Allocations
  listAllocations: (params = {}) => get(`/allocations${qs(params)}`),
  createAllocation: (data) => post('/allocations', data),
  updateAllocation: (id, data) => put(`/allocations/${id}`, data),
  deleteAllocation: (id) => del(`/allocations/${id}`),

  // Risks
  listRisks: (params = {}) => get(`/risks${qs(params)}`),
  createRisk: (data) => post('/risks', data),
  updateRisk: (id, data) => put(`/risks/${id}`, data),
  deleteRisk: (id) => del(`/risks/${id}`),

  // Dashboard & reports
  getDashboardSummary: () => get('/dashboard/summary'),
  getPortfolioReport: () => get('/reports/portfolio'),
  getProjectReport: (id) => get(`/reports/project/${id}`),
};

// Build a query string from a params object, dropping empty/null/undefined values
// so the URL only carries parameters that are actually set. Returns '' when none.
function qs(params) {
  const entries = Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== '');
  if (!entries.length) return '';
  return `?${new URLSearchParams(entries).toString()}`;
}
