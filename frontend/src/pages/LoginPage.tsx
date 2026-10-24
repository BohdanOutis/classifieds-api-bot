import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/useStore';
import { setApiKey } from '../store/authSlice';
import { getAds } from '../api/ads';
import Spinner from '../components/Spinner';

const LoginPage = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const isAuthenticated = useAppSelector((s) => s.auth.isAuthenticated);

  const [key, setKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showKey, setShowKey] = useState(false);

  useEffect(() => {
    if (isAuthenticated) navigate('/dashboard', { replace: true });
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = key.trim();
    if (!trimmed) {
      setError('Будь ласка, введіть API-ключ.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      localStorage.setItem('api_key', trimmed);
      await getAds();
      dispatch(setApiKey(trimmed));
      navigate('/dashboard', { replace: true });
    } catch (err: unknown) {
      localStorage.removeItem('api_key');
      const status = (err as { response?: { status?: number } })?.response?.status;
      if (status === 401 || status === 403) {
        setError('Невірний API-ключ. Перевірте та спробуйте знову.');
      } else if (status === undefined) {
        setError('Не вдалося з\'єднатися з сервером. Перевірте, чи запущений бекенд.');
      } else {
        setError(`Помилка сервера: ${status}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center p-6 overflow-hidden bg-[var(--clr-bg)]">
      {/* ── Background Blobs ───────────────────────────────────────────── */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-150px] left-[-100px] w-[500px] h-[500px] rounded-full bg-[radial-gradient(circle,_#6c63ff99_0%,_transparent_70%)] blur-[80px] opacity-40 animate-[blob-drift_12s_ease-in-out_infinite]" />
        <div className="absolute bottom-[-100px] right-[-80px] w-[400px] h-[400px] rounded-full bg-[radial-gradient(circle,_#8b5cf680_0%,_transparent_70%)] blur-[80px] opacity-40 animate-[blob-drift_12s_ease-in-out_infinite_-4s]" />
        <div className="absolute top-[40%] left-[50%] -translate-x-1/2 w-[300px] h-[300px] rounded-full bg-[radial-gradient(circle,_#c084fc59_0%,_transparent_70%)] blur-[80px] opacity-40 animate-[blob-drift_12s_ease-in-out_infinite_-8s]" />
      </div>

      {/* ── Login Card ─────────────────────────────────────────────────── */}
      <div className="relative z-10 w-full max-w-[440px] bg-[#13161f]/75 backdrop-blur-2xl border border-white/10 rounded-[var(--radius-xl)] p-10 sm:p-11 shadow-[var(--shadow-lg),_0_0_60px_rgba(108,99,255,0.1)] animate-fade-in-up">
        {/* Brand */}
        <div className="text-center mb-9">
          <div className="w-16 h-16 rounded-[var(--radius-md)] bg-gradient-to-br from-[var(--clr-accent)] to-purple-600 inline-flex items-center justify-center text-white mb-4 shadow-[0_8px_32px_var(--clr-accent-glow)] animate-[pulse-glow_3s_ease-in-out_infinite]">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
            </svg>
          </div>
          <h1 className="text-3xl font-black tracking-tight bg-gradient-to-br from-[var(--clr-text)] to-[var(--clr-accent-2)] bg-clip-text text-transparent mb-1.5">
            AdPanel
          </h1>
          <p className="text-sm text-[var(--clr-text-2)]">Адмін-панель дошки оголошень</p>
        </div>

        {/* Form */}
        <form className="flex flex-col gap-6" onSubmit={handleSubmit} noValidate id="login-form">
          <div className="flex flex-col gap-2">
            <label className="text-xs font-semibold uppercase tracking-wider text-[var(--clr-text-2)]" htmlFor="api-key-input">
              API-ключ
            </label>
            <div className="relative flex items-center">
              <span className="absolute left-3.5 text-[var(--clr-text-3)] pointer-events-none flex items-center justify-center">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4" />
                </svg>
              </span>
              <input
                id="api-key-input"
                className={`w-full pl-11 pr-11 py-2.5 bg-[var(--clr-surface-2)] border rounded-[var(--radius-sm)] text-[var(--clr-text)] text-sm outline-none transition-all duration-200 placeholder:text-[var(--clr-text-3)] focus:bg-[var(--clr-surface-3)] focus:ring-3 ${
                  error
                    ? 'border-red-500/80 focus:border-red-500 focus:ring-red-500/20'
                    : 'border-[var(--clr-border)] focus:border-[var(--clr-accent)] focus:ring-[rgba(108,99,255,0.15)]'
                }`}
                type={showKey ? 'text' : 'password'}
                value={key}
                onChange={(e) => {
                  setKey(e.target.value);
                  setError('');
                }}
                placeholder="Введіть ваш API Key..."
                autoComplete="current-password"
                disabled={loading}
                autoFocus
              />
              <button
                type="button"
                className="absolute right-3.5 text-[var(--clr-text-3)] hover:text-[var(--clr-text)] transition-colors duration-150 cursor-pointer flex items-center justify-center p-1"
                onClick={() => setShowKey((v) => !v)}
                aria-label={showKey ? 'Приховати ключ' : 'Показати ключ'}
              >
                {showKey ? (
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                    <line x1="1" y1="1" x2="23" y2="23" />
                  </svg>
                ) : (
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                )}
              </button>
            </div>

            {error && (
              <p className="inline-flex items-center gap-1.5 text-xs text-red-400 font-medium mt-1 animate-fade-in-up" role="alert" id="login-error">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" className="shrink-0">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" />
                </svg>
                <span>{error}</span>
              </p>
            )}
          </div>

          <button
            type="submit"
            className="w-full inline-flex items-center justify-center gap-2 px-5 py-3 rounded-[var(--radius-sm)] text-sm font-semibold text-white bg-gradient-to-br from-[var(--clr-accent)] to-purple-600 shadow-[0_4px_14px_var(--clr-accent-glow)] transition-all duration-200 cursor-pointer hover:enabled:from-[var(--clr-accent-hover)] hover:enabled:to-purple-500 hover:enabled:shadow-[0_6px_20px_var(--clr-accent-glow)] hover:enabled:-translate-y-0.5 active:enabled:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={loading || !key.trim()}
            id="login-submit-btn"
          >
            {loading ? (
              <>
                <Spinner size={18} />
                <span>Перевірка...</span>
              </>
            ) : (
              <>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
                  <polyline points="10 17 15 12 10 7" />
                  <line x1="15" y1="12" x2="3" y2="12" />
                </svg>
                <span>Увійти</span>
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;