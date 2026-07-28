import Sidebar from './Sidebar';
import Topbar from './Topbar';

export default function AppLayout({ title, children }) {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="content-area">
        <Topbar title={title} />
        <main className="page-content">{children}</main>
      </div>
    </div>
  );
}
