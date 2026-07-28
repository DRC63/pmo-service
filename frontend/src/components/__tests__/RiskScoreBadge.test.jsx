import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import RiskScoreBadge from '../RiskScoreBadge';

describe('RiskScoreBadge', () => {
  it('shows red for high scores (>=15)', () => {
    render(<RiskScoreBadge score={20} />);
    expect(screen.getByText('20')).toHaveClass('badge-red');
  });

  it('treats 15 as the red boundary', () => {
    render(<RiskScoreBadge score={15} />);
    expect(screen.getByText('15')).toHaveClass('badge-red');
  });

  it('shows amber for medium scores (8-14)', () => {
    render(<RiskScoreBadge score={10} />);
    expect(screen.getByText('10')).toHaveClass('badge-amber');
  });

  it('treats 8 as the amber boundary', () => {
    render(<RiskScoreBadge score={8} />);
    expect(screen.getByText('8')).toHaveClass('badge-amber');
  });

  it('shows green for low scores (<8)', () => {
    render(<RiskScoreBadge score={4} />);
    expect(screen.getByText('4')).toHaveClass('badge-green');
  });
});
