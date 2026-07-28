import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import RagBadge from '../RagBadge';

describe('RagBadge', () => {
  it('renders the correct label and class for green', () => {
    render(<RagBadge status="green" />);
    expect(screen.getByText('Green')).toHaveClass('badge-green');
  });

  it('renders amber and red statuses', () => {
    const { rerender } = render(<RagBadge status="amber" />);
    expect(screen.getByText('Amber')).toHaveClass('badge-amber');

    rerender(<RagBadge status="red" />);
    expect(screen.getByText('Red')).toHaveClass('badge-red');
  });

  it('falls back to the raw value for unknown statuses', () => {
    render(<RagBadge status="unknown" />);
    expect(screen.getByText('unknown')).toHaveClass('badge-unknown');
  });

  it('falls back to a grey badge when status is missing', () => {
    const { container } = render(<RagBadge />);
    expect(container.querySelector('.badge')).toHaveClass('badge-grey');
  });
});
