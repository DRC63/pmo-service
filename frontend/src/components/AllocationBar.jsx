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
