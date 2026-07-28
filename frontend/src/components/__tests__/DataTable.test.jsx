import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import DataTable from '../DataTable';

const columns = [
  { key: 'name', label: 'Name' },
  { key: 'score', label: 'Score', numeric: true },
];

describe('DataTable', () => {
  it('renders the empty message when there are no rows', () => {
    render(<DataTable columns={columns} rows={[]} emptyMessage="Nothing here" />);
    expect(screen.getByText('Nothing here')).toBeInTheDocument();
  });

  it('renders rows and columns', () => {
    render(<DataTable columns={columns} rows={[{ id: 1, name: 'Alpha', score: 10 }]} />);
    expect(screen.getByText('Alpha')).toBeInTheDocument();
    expect(screen.getByText('10')).toBeInTheDocument();
  });

  it('uses a custom render function per column when provided', () => {
    const customColumns = [{ key: 'name', label: 'Name', render: (row) => `Custom: ${row.name}` }];
    render(<DataTable columns={customColumns} rows={[{ id: 1, name: 'Beta' }]} />);
    expect(screen.getByText('Custom: Beta')).toBeInTheDocument();
  });

  it('calls onRowClick with the row when a row is clicked', () => {
    const handleClick = vi.fn();
    const row = { id: 1, name: 'Alpha', score: 10 };
    render(<DataTable columns={columns} rows={[row]} onRowClick={handleClick} />);

    fireEvent.click(screen.getByText('Alpha'));

    expect(handleClick).toHaveBeenCalledWith(row);
  });
});
