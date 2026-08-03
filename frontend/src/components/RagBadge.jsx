// Coloured status pill for a project's RAG (Red / Amber / Green) status. Falls back
// to a neutral grey style and the raw value if the status isn't one of the three.
const LABELS = { green: 'Green', amber: 'Amber', red: 'Red' };

export default function RagBadge({ status }) {
  const cls = `badge badge-${status || 'grey'}`;
  return <span className={cls}>{LABELS[status] || status}</span>;
}
