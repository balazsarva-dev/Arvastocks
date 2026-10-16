import { NavLink, Outlet, useLocation } from 'react-router-dom';

const links = [
  { to: '/', label: 'Markets', keepSymbol: true },
  { to: '/news', label: 'News', keepSymbol: true },
  { to: '/about', label: 'About' },
  { to: '/donation', label: 'Donate' },
];

export default function Layout() {
  const { search } = useLocation();

  return (
    <>
      <header className="topbar">
        <NavLink to="/" className="brand">
          <img src="/favicon.svg" alt="" width="24" height="24" />
          Arvastocks
        </NavLink>
        <nav>
          {links.map(({ to, label, keepSymbol }) => (
            <NavLink key={to} to={keepSymbol ? to + search : to} end>
              {label}
            </NavLink>
          ))}
        </nav>
      </header>
      <main className="container">
        <Outlet />
      </main>
      <footer className="footer">
        © {new Date().getFullYear()} Arvastocks · Data from Yahoo Finance · Not investment advice
      </footer>
    </>
  );
}
