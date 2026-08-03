// Horizontal bar showing a resource's allocation percentage. The visible fill is
// capped at 100% width and given an "over" style once allocation exceeds 100%, so
// over-allocation is obvious at a glance; the exact percentage is always shown as
// text alongside the bar.
export default function AllocationBar({ pct }) {
  const clamped = Math.min(pct, 150);
  const over = pct > 100;
  return (
    <div className="flex-row">
      <div className="allocation-bar-track" style={{ maxWidth: 140 }}>
        <div
          className={`allocation-bar-fill${over ? ' over' : ''}`}
          style={{ width: `${Math.min(clamped, 100)}%` }}
        />
      </div>
      <span className="muted">{pct}%</span>
    </div>
  );
}
