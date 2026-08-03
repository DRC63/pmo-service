// Header bar shown on every page: the current page title on the left and the
// P3MAI wordmark on the right. Presentational only — the title comes from the route.
export default function Topbar({ title }) {
  return (
    <header className="topbar">
      <h1>{title}</h1>
      <span className="topbar-brand">P3M<span className="brand-ai">AI</span></span>
    </header>
  );
}
