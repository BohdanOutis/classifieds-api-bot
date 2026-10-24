import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/useStore';
import { logout } from '../store/authSlice';

interface LayoutProps {
  children: React.ReactNode;
}

const navItems = [
  {
    to: '/dashboard',
    label: 'Оголошення',
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="7" height="7" rx="1"/>
        <rect x="14" y="3" width="7" height="7" rx="1"/>
        <rect x="3" y="14" width="7" height="7" rx="1"/>
        <rect x="14" y="14" width="7" height="7" rx="1"/>
      </svg>
    ),
  },
  {
    to: '/create-ad',
    label: 'Нове оголошення',
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="16"/>
        <line x1="8" y1="12" x2="16" y2="12"/>
      </svg>
    ),
  },
  {
    to: '/stats',
    label: 'Статистика бота',
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="16"/>
        <line x1="8" y1="12" x2="16" y2="12"/>
      </svg>
    ),
  },
];

const Layout = ({ children }: LayoutProps) => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const apiKey = useAppSelector((s) => s.auth.apiKey);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login', { replace: true });
  };

  const maskedKey = apiKey
    ? `${apiKey.slice(0, 6)}${'•'.repeat(Math.min(12, Math.max(0, apiKey.length - 6)))}`
    : '';

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="fixed top-0 left-0 bottom-0 z-100 flex flex-col w-[var(--sidebar-w)] bg-[var(--clr-surface)] border-r border-[var(--clr-border)] animate-fade-in-right">
        
        {/* Brand Header */}
        <div className="flex items-center gap-3 p-6 pb-5 border-b border-[var(--clr-border)]">
          <div className="flex shrink-0 items-center justify-center w-10 h-10 rounded-[var(--radius-sm)] bg-gradient-to-br from-[var(--clr-accent)] to-purple-600 text-white shadow-[var(--shadow-glow)]">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
          <span className="text-[1.2rem] font-extrabold tracking-tight bg-gradient-to-br from-[var(--clr-accent-2)] to-purple-400 bg-clip-text text-transparent">
            AdPanel
          </span>
        </div>

        {/* Navigation */}
        <nav className="flex-1 flex flex-col gap-1 px-3 py-4 overflow-y-auto" aria-label="Main navigation">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-3 rounded-[var(--radius-sm)] text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-br from-[rgba(108,99,255,0.2)] to-[rgba(139,92,246,0.1)] text-[var(--clr-accent-2)] border border-[rgba(108,99,255,0.2)]'
                    : 'text-[var(--clr-text-2)] hover:bg-[var(--clr-surface-2)] hover:text-[var(--clr-text)]'
                }`
              }
            >
              <span className="flex shrink-0 items-center">{item.icon}</span>
              <span className="truncate whitespace-nowrap">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        <div className="flex flex-col gap-2.5 p-3 border-t border-[var(--clr-border)]">
          <div className="flex items-center gap-2 px-3 py-2.5 bg-[var(--clr-surface-2)] rounded-[var(--radius-sm)] text-xs text-[var(--clr-text-3)] border border-[var(--clr-border)] overflow-hidden" title={apiKey ?? ''}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="shrink-0">
              <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>
            </svg>
            <span className="font-mono truncate flex-1">{maskedKey}</span>
          </div>

          <button
            className="flex items-center gap-2.5 w-full px-3.5 py-2.5 rounded-[var(--radius-sm)] bg-transparent border border-[var(--clr-border)] text-[var(--clr-text-2)] text-sm font-medium transition-all duration-200 cursor-pointer hover:bg-red-500/10 hover:border-red-500/30 hover:text-red-400"
            onClick={handleLogout}
            id="logout-btn"
            aria-label="Вийти"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="shrink-0">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            <span>Вийти</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-[var(--sidebar-w)] min-h-screen bg-[var(--clr-bg)] overflow-x-hidden">
        {children}
      </main>
    </div>
  );
};

export default Layout;