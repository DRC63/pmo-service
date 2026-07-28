import { NavLink } from 'react-router';
import logo from '../assets/logo-triangle-white.svg';

const LINKS = [
  { to: '/', label: 'Dashboard', end: true },
  { to: '/projects', label: 'Projects' },
  { to: '/resources', label: 'Resources' },
  { to: '/risks', label: 'Risks' },
  { to: '/reports', label: 'Reports' },
  { to: '/settings', label: 'Settings' },
];

// Points at the local static-site server while working on localhost; swaps
// to the real domain automatically once this app is served from
// app.p3mai.com, so there's nothing to remember to change at deploy time.
const isLocal = /^(localhost|127\.0\.0\.1)$/.test(window.location.hostname);
const WEBSITE_URL = isLocal
  ? 'http://localhost:4173/services.html'
  : 'https://p3mai.com/services.html';

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <img src={logo} alt="P3MAI" />
        <span>PMO Service</span>
      </div>
      <nav className="sidebar-nav">
        {LINKS.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.end}
            className={({ isActive }) => (isActive ? 'active' : undefined)}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
      <a className="sidebar-back" href={WEBSITE_URL}>
        <span aria-hidden="true">&larr;</span> Back to Website
      </a>
    </aside>
  );
}
