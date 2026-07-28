import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import AllocationBar from '../AllocationBar';

describe('AllocationBar', () => {
  it('renders the percentage label', () => {
    render(<AllocationBar pct={60} />);
    expect(screen.getByText('60%')).toBeInTheDocument();
  });

  it('marks over-allocation (>100%) with the "over" fill class, clamped visually to 100%', () => {
    const { container } = render(<AllocationBar pct={120} />);
    const fill = container.querySelector('.allocation-bar-fill');
    expect(fill).toHaveClass('over');
    expect(fill.style.width).toBe('100%');
  });

  it('does not mark at-capacity allocation as over', () => {
    const { container } = render(<AllocationBar pct={100} />);
    expect(container.querySelector('.allocation-bar-fill')).not.toHaveClass('over');
  });
});
