// Unit test for the Dashboard page: the summary API is mocked, and the test asserts
// the loaded portfolio figures render.
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router';
import { describe, it, expect, vi } from 'vitest';
import Dashboard from '../Dashboard';
import { api } from '../../api/client';

vi.mock('../../api/client', () => ({
  api: { getDashboardSummary: vi.fn() },
}));

function renderDashboard() {
  return render(
    <MemoryRouter>
      <Dashboard />
    </MemoryRouter>
  );
}

describe('Dashboard page', () => {
  it('shows a loading state before data arrives', () => {
    api.getDashboardSummary.mockReturnValue(new Promise(() => {})); // never resolves
    renderDashboard();
    expect(screen.getByText('Loading…')).toBeInTheDocument();
  });

  it('renders summary stats and lists once data loads', async () => {
    api.getDashboardSummary.mockResolvedValue({
      total_projects: 3,
      rag_counts: { green: 2, amber: 1, red: 0 },
      overdue_milestones_count: 1,
      upcoming_milestones: [
        {
          milestone_id: 1,
          project_id: 5,
          project_name: 'Project X',
          name: 'Kickoff',
          due_date: '2026-08-01',
          days_until: 4,
        },
      ],
      high_severity_risks: [
        {
          risk_id: 9,
          project_id: 5,
          project_name: 'Project X',
          title: 'Big Risk',
          status: 'open',
          score: 20,
        },
      ],
    });

    renderDashboard();

    await waitFor(() => expect(screen.getByText('3')).toBeInTheDocument());
    expect(screen.getByText('Kickoff')).toBeInTheDocument();
    expect(screen.getByText('Big Risk')).toBeInTheDocument();
    expect(screen.getByText('20')).toBeInTheDocument();
  });

  it('shows an empty state when there is nothing upcoming or high-severity', async () => {
    api.getDashboardSummary.mockResolvedValue({
      total_projects: 0,
      rag_counts: { green: 0, amber: 0, red: 0 },
      overdue_milestones_count: 0,
      upcoming_milestones: [],
      high_severity_risks: [],
    });

    renderDashboard();

    await waitFor(() =>
      expect(screen.getByText('Nothing due in the next 30 days.')).toBeInTheDocument()
    );
    expect(screen.getByText('No open high-severity risks.')).toBeInTheDocument();
  });

  it('shows an error message when the request fails', async () => {
    api.getDashboardSummary.mockRejectedValue(new Error('Network down'));
    renderDashboard();
    await waitFor(() => expect(screen.getByText('Network down')).toBeInTheDocument());
  });
});
