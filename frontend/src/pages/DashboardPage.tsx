import { useEffect, useState, useMemo } from 'react';

import { Link } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/useStore';
import { fetchAds } from '../store/adsSlice';
import AdCard from '../components/AdCard';
import Spinner from '../components/Spinner';
import type { AdsQueryParams } from '../types/api';

const PAGE_SIZE = 12;

const STATUS_OPTIONS = [
  { value: '', label: 'Всі статуси' },
  { value: 'active', label: 'Активні' },
  { value: 'pending', label: 'На модерації' },
  { value: 'inactive', label: 'Неактивні' },
  { value: 'rejected', label: 'Відхилені' },
];

const DashboardPage = () => {
  const dispatch = useAppDispatch();
  const { ads, loading, error } = useAppSelector((s) => s.ads);

  const [statusFilter, setStatusFilter] = useState('');
  const [tgIdFilter, setTgIdFilter] = useState('');
  const [page, setPage] = useState(1);

  const fetchWithFilters = (params: AdsQueryParams = {}) => {
    dispatch(fetchAds(params));
  };

  useEffect(() => {
    fetchWithFilters();
  }, []);

  const handleApplyFilters = () => {
    const params: AdsQueryParams = {};
    if (statusFilter) params.status = statusFilter;
    if (tgIdFilter) params.tg_id = Number(tgIdFilter);
    setPage(1);
    fetchWithFilters(params);
  };

  const handleReset = () => {
    setStatusFilter('');
    setTgIdFilter('');
    setPage(1);
    fetchWithFilters();
  };

  const totalPages = Math.max(1, Math.ceil(ads.length / PAGE_SIZE));
  const paginated = useMemo(
    () => ads.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE),
    [ads, page],
  );

  const stats = useMemo(
    () => ({
      total: ads.length,
      active: ads.filter((a) => a.status === 'active').length,
      pending: ads.filter((a) => a.status === 'pending').length,
      rejected: ads.filter((a) => a.status === 'rejected').length,
    }),
    [ads],
  );

  return (
    <div className="page dashboard-page">
      {/* ── Header ──────────────────────────────────────────────────────── */}
      <div className="page__header">
        <div>
          <h1 className="page__title">Оголошення</h1>
          <p className="page__subtitle">Управління оголошеннями дошки</p>
        </div>
        <div className="page__actions">
          <button
            className="btn btn--secondary"
            onClick={() => fetchWithFilters()}
            disabled={loading}
            id="refresh-ads-btn"
            aria-label="Оновити список"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={loading ? 'spin' : ''}>
              <polyline points="23 4 23 10 17 10"/>
              <polyline points="1 20 1 14 7 14"/>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
            </svg>
            Оновити
          </button>
          <Link to="/create-ad" className="btn btn--primary" id="create-ad-link">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            Нове оголошення
          </Link>
        </div>
      </div>

      {/* ── Stats ───────────────────────────────────────────────────────── */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-card__icon stat-card__icon--total">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="7" height="7" rx="1"/>
              <rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/>
              <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
          </div>
          <div>
            <p className="stat-card__label">Всього</p>
            <p className="stat-card__value">{stats.total}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-card__icon stat-card__icon--active">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
          </div>
          <div>
            <p className="stat-card__label">Активні</p>
            <p className="stat-card__value stat-card__value--active">{stats.active}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-card__icon stat-card__icon--pending">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
          </div>
          <div>
            <p className="stat-card__label">На модерації</p>
            <p className="stat-card__value stat-card__value--pending">{stats.pending}</p>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-card__icon stat-card__icon--rejected">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="15" y1="9" x2="9" y2="15"/>
              <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
          </div>
          <div>
            <p className="stat-card__label">Відхилені</p>
            <p className="stat-card__value stat-card__value--rejected">{stats.rejected}</p>
          </div>
        </div>
      </div>

      {/* ── Filters ─────────────────────────────────────────────────────── */}
      <div className="filters-bar">
        <div className="filters-bar__group">
          <label htmlFor="status-filter" className="filters-bar__label">Статус</label>
          <select
            id="status-filter"
            className="form-select"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            {STATUS_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
        </div>
        <div className="filters-bar__group">
          <label htmlFor="tg-id-filter" className="filters-bar__label">Telegram ID</label>
          <input
            id="tg-id-filter"
            className="form-input"
            type="text"
            inputMode="numeric"
            pattern="[0-9]*"
            placeholder="Пошук за tg_id..."
            value={tgIdFilter}
            onChange={(e) => setTgIdFilter(e.target.value)}
            min="1"
          />
        </div>
        <div className="filters-bar__actions">
          <button
            className="btn btn--primary"
            onClick={handleApplyFilters}
            id="apply-filters-btn"
            disabled={loading}
          >
            Застосувати
          </button>
          <button
            className="btn btn--ghost"
            onClick={handleReset}
            id="reset-filters-btn"
            disabled={loading}
          >
            Скинути
          </button>
        </div>
      </div>

      {/* ── Content ─────────────────────────────────────────────────────── */}
      {loading ? (
        <div className="state-center">
          <Spinner size={48} />
          <p className="state-center__text">Завантаження оголошень...</p>
        </div>
      ) : error ? (
        <div className="state-center state-center--error">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <p className="state-center__text">{error}</p>
          <button className="btn btn--secondary" onClick={() => fetchWithFilters()}>
            Спробувати знову
          </button>
        </div>
      ) : paginated.length === 0 ? (
        <div className="state-center">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          <p className="state-center__text">Оголошень не знайдено</p>
          <Link to="/create-ad" className="btn btn--primary">Створити перше оголошення</Link>
        </div>
      ) : (
        <>
          <div className="ads-grid" id="ads-grid">
            {paginated.map((ad) => (
              <AdCard key={ad.id} ad={ad} />
            ))}
          </div>

          {/* ── Pagination ────────────────────────────────────────────── */}
          {totalPages > 1 && (
            <div className="pagination" role="navigation" aria-label="Pagination">
              <button
                className="pagination__btn"
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                id="prev-page-btn"
                aria-label="Попередня сторінка"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="15 18 9 12 15 6"/>
                </svg>
              </button>

              <div className="pagination__pages">
                {Array.from({ length: totalPages }, (_, i) => i + 1)
                  .filter((p) => p === 1 || p === totalPages || Math.abs(p - page) <= 1)
                  .reduce<(number | '...')[]>((acc, p, idx, arr) => {
                    if (idx > 0 && typeof arr[idx - 1] === 'number' && (p as number) - (arr[idx - 1] as number) > 1) {
                      acc.push('...');
                    }
                    acc.push(p);
                    return acc;
                  }, [])
                  .map((item, idx) =>
                    item === '...' ? (
                      <span key={`ellipsis-${idx}`} className="pagination__ellipsis">…</span>
                    ) : (
                      <button
                        key={item}
                        className={`pagination__page ${page === item ? 'pagination__page--active' : ''}`}
                        onClick={() => setPage(item as number)}
                        aria-label={`Сторінка ${item}`}
                        aria-current={page === item ? 'page' : undefined}
                      >
                        {item}
                      </button>
                    ),
                  )}
              </div>

              <button
                className="pagination__btn"
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                id="next-page-btn"
                aria-label="Наступна сторінка"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="9 18 15 12 9 6"/>
                </svg>
              </button>

              <span className="pagination__info">
                Показано {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, ads.length)} з {ads.length}
              </span>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default DashboardPage;