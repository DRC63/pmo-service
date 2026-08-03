// Coloured pill for a risk score (likelihood × impact, so 1–25). The colour tiers
// match the severity thresholds used elsewhere — 15+ is high (red), 8–14 medium
// (amber), below is low (green) — so a score reads at a glance without the viewer
// doing the maths.
function tier(score) {
  if (score >= 15) return 'red';
  if (score >= 8) return 'amber';
  return 'green';
}

export default function RiskScoreBadge({ score }) {
  return <span className={`badge badge-${tier(score)}`}>{score}</span>;
}
