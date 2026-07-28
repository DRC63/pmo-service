const LABELS = { green: 'Green', amber: 'Amber', red: 'Red' };

export default function RagBadge({ status }) {
  const cls = `badge badge-${status || 'grey'}`;
  return <span className={cls}>{LABELS[status] || status}</span>;
}
