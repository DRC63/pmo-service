// Unit tests for the API client: verifies it builds the right URLs, throws on a
// non-2xx response, and returns parsed JSON — with fetch mocked so no backend runs.
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { api } from '../client';

describe('api client', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it('builds query strings from params, dropping empty values', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => [{ id: 1, name: 'Project A' }],
    });

    const result = await api.listProjects({ category: 'banking', rag_status: '' });

    expect(global.fetch).toHaveBeenCalledWith(
      '/api/projects?category=banking',
      expect.objectContaining({ headers: { 'Content-Type': 'application/json' } })
    );
    expect(result).toEqual([{ id: 1, name: 'Project A' }]);
  });

  it('omits the query string entirely when there are no params', async () => {
    global.fetch.mockResolvedValue({ ok: true, status: 200, json: async () => [] });
    await api.listProjects();
    expect(global.fetch).toHaveBeenCalledWith('/api/projects', expect.anything());
  });

  it('sends POST requests with a JSON body', async () => {
    global.fetch.mockResolvedValue({ ok: true, status: 201, json: async () => ({ id: 2 }) });

    await api.createProject({ name: 'New', code: 'N1' });

    expect(global.fetch).toHaveBeenCalledWith(
      '/api/projects',
      expect.objectContaining({ method: 'POST', body: JSON.stringify({ name: 'New', code: 'N1' }) })
    );
  });

  it('sends PUT requests to the resource path', async () => {
    global.fetch.mockResolvedValue({ ok: true, status: 200, json: async () => ({ id: 5 }) });
    await api.updateRisk(5, { status: 'closed' });
    expect(global.fetch).toHaveBeenCalledWith(
      '/api/risks/5',
      expect.objectContaining({ method: 'PUT', body: JSON.stringify({ status: 'closed' }) })
    );
  });

  it('returns null for 204 No Content responses without calling .json()', async () => {
    const json = vi.fn();
    global.fetch.mockResolvedValue({ ok: true, status: 204, json });
    const result = await api.deleteProject(1);
    expect(result).toBeNull();
    expect(json).not.toHaveBeenCalled();
  });

  it('throws a descriptive error when the response is not ok', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      status: 404,
      text: async () => 'Project not found',
    });

    await expect(api.getProject(999)).rejects.toThrow(
      'GET /projects/999 failed (404): Project not found'
    );
  });
});
