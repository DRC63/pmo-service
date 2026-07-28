function tier(score) {
  if (score >= 15) return 'red';
  if (score >= 8) return 'amber';
  return 'green';
}

export default function RiskScoreBadge({ score }) {
  return <span className={`badge badge-${tier(score)}`}>{score}</span>;
}
