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
    <div className="login-page">
      <div className="login-page__bg">
        <div className="login-page__bg-blob login-page__bg-blob--1" />
        <div className="login-page__bg-blob login-page__bg-blob--2" />
        <div className="login-page__bg-blob login-page__bg-blob--3" />
      </div>

      <div className="login-card">
        <div className="login-card__brand">
          <div className="login-card__logo">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
          <h1 className="login-card__title">AdPanel</h1>
          <p className="login-card__subtitle">Адмін-панель дошки оголошень</p>
        </div>

        <form className="login-card__form" onSubmit={handleSubmit} noValidate id="login-form">
          <div className="form-group">
            <label className="form-label" htmlFor="api-key-input">
              API-ключ
            </label>
            <div className="form-input-wrapper">
              <span className="form-input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>
                </svg>
              </span>
              <input
                id="api-key-input"
                className={`form-input ${error ? 'form-input--error' : ''}`}
                type={showKey ? 'text' : 'password'}
                value={key}
                onChange={(e) => { setKey(e.target.value); setError(''); }}
                placeholder="Введіть ваш API Key..."
                autoComplete="current-password"
                disabled={loading}
                autoFocus
              />
              <button
                type="button"
                className="form-input-toggle"
                onClick={() => setShowKey((v) => !v)}
                aria-label={showKey ? 'Приховати ключ' : 'Показати ключ'}
              >
                {showKey ? (
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                ) : (
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                )}
              </button>
            </div>

            {error && (
              <p className="form-error" role="alert" id="login-error">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                </svg>
                {error}
              </p>
            )}
          </div>

          <button
            type="submit"
            className="btn btn--primary btn--full"
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
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
                  <polyline points="10 17 15 12 10 7"/>
                  <line x1="15" y1="12" x2="3" y2="12"/>
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