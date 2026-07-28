import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Projects from '../Projects';
import { api } from '../../api/client';

vi.mock('../../api/client', () => ({
  api: {
    listProjects: vi.fn(),
    listResources: vi.fn(),
  },
}));

function renderProjects() {
  return render(
    <MemoryRouter>
      <Projects />
    </MemoryRouter>
  );
}

describe('Projects page', () => {
  beforeEach(() => {
    api.listResources.mockResolvedValue([]);
  });

  it('renders the project list once loaded', async () => {
    api.listProjects.mockResolvedValue([
      {
        id: 1,
        name: 'Alpha',
        code: 'A1',
        category: 'other',
        owner_name: 'Doug',
        rag_status: 'green',
        end_date: '2026-12-01',
        budget: 1000,
      },
    ]);

    renderProjects();

    await waitFor(() => expect(screen.getByText('Alpha')).toBeInTheDocument());
    // 'Green' also appears as a filter-dropdown option, so scope to the RAG badge span
    expect(screen.getByText('Green', { selector: 'span.badge' })).toBeInTheDocument();
    expect(screen.getByText('$1,000')).toBeInTheDocument();
  });

  it('shows the empty message when no projects match filters', async () => {
    api.listProjects.mockResolvedValue([]);
    renderProjects();
    await waitFor(() =>
      expect(screen.getByText('No projects match these filters.')).toBeInTheDocument()
    );
  });

  it('shows an error message when loading fails', async () => {
    api.listProjects.mockRejectedValue(new Error('boom'));
    renderProjects();
    await waitFor(() => expect(screen.getByText('boom')).toBeInTheDocument());
  });

  it('opens the New Project modal when the button is clicked', async () => {
    api.listProjects.mockResolvedValue([]);
    const { default: userEvent } = await import('@testing-library/user-event');
    const user = userEvent.setup();

    renderProjects();
    await waitFor(() => expect(api.listProjects).toHaveBeenCalled());

    await user.click(screen.getByText('+ New Project'));
    expect(screen.getByText('Save Project')).toBeInTheDocument();
  });
});
