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
      <a
        className="sidebar-back"
        href="http://localhost:4173/services.html"
      >
        <span aria-hidden="true">&larr;</span> Back to Website
      </a>
    </aside>
  );
}
