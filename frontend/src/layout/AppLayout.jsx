import Sidebar from './Sidebar';
import Topbar from './Topbar';

// Standard page frame for every route: the left sidebar navigation, the top bar
// (page title + brand), and the routed page content in the main area.
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
