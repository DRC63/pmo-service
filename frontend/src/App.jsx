import { BrowserRouter, Route, Routes } from 'react-router';
import AppLayout from './layout/AppLayout';
import Dashboard from './pages/Dashboard';
import Projects from './pages/Projects';
import ProjectDetail from './pages/ProjectDetail';
import Resources from './pages/Resources';
import Risks from './pages/Risks';
import Reports from './pages/Reports';
import Settings from './pages/Settings';

function Page({ title, children }) {
  return <AppLayout title={title}>{children}</AppLayout>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Page title="Dashboard"><Dashboard /></Page>} />
        <Route path="/projects" element={<Page title="Projects"><Projects /></Page>} />
        <Route path="/projects/:id" element={<Page title="Project Detail"><ProjectDetail /></Page>} />
        <Route path="/resources" element={<Page title="Resources"><Resources /></Page>} />
        <Route path="/risks" element={<Page title="Risk Register"><Risks /></Page>} />
        <Route path="/reports" element={<Page title="Reports"><Reports /></Page>} />
        <Route path="/settings" element={<Page title="Settings"><Settings /></Page>} />
      </Routes>
    </BrowserRouter>
  );
}
