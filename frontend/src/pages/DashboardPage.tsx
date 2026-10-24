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

  // Утилітні класи для елементів керування фільтрами
  const formControlClasses =
    'w-full px-4 py-2.5 bg-[var(--clr-surface-2)] border border-[var(--clr-border)] rounded-[var(--radius-sm)] text-[var(--clr-text)] text-sm outline-none transition-all duration-200 placeholder:text-[var(--clr-text-3)] focus:border-[var(--clr-accent)] focus:ring-3 focus:ring-[rgba(108,99,255,0.15)] focus:bg-[var(--clr-surface-3)] disabled:opacity-50';

  return (
    <div className="p-6 max-w-7xl mx-auto flex flex-col gap-8">
      {/* ── Header ──────────────────────────────────────────────────────── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-[var(--clr-text)]">Оголошення</h1>
          <p className="text-sm text-[var(--clr-text-2)] mt-1">Управління оголошеннями дошки</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-[var(--radius-sm)] text-sm font-medium bg-[var(--clr-surface)] border border-[var(--clr-border)] text-[var(--clr-text-2)] transition-all duration-200 cursor-pointer hover:enabled:text-[var(--clr-text)] hover:enabled:border-[var(--clr-border-hover)] hover:enabled:bg-[var(--clr-surface-2)] disabled:opacity-40 disabled:cursor-not-allowed"
            onClick={() => fetchWithFilters()}
            disabled={loading}
            id="refresh-ads-btn"
            aria-label="Оновити список"
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className={loading ? 'animate-spin' : ''}
            >
              <polyline points="23 4 23 10 17 10" />
              <polyline points="1 20 1 14 7 14" />
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
            </svg>
            Оновити
          </button>
          <Link
            to="/create-ad"
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-[var(--radius-sm)] text-sm font-semibold text-white bg-gradient-to-br from-[var(--clr-accent)] to-purple-600 shadow-[0_4px_14px_var(--clr-accent-glow)] transition-all duration-200 hover:from-[var(--clr-accent-hover)] hover:to-purple-500 hover:shadow-[0_6px_20px_var(--clr-accent-glow)] hover:-translate-y-0.5 active:translate-y-0"
            id="create-ad-link"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            Нове оголошення
          </Link>
        </div>
      </div>

      {/* ── Stats ───────────────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Stat */}
        <div className="flex items-center gap-4 p-5 sm:p-6 bg-[var(--clr-surface)] border border-[var(--clr-border)] rounded-[var(--radius-md)] transition-all duration-200 hover:border-[var(--clr-border-hover)] hover:-translate-y-0.5 hover:shadow-md animate-fade-in-up">
          <div className="w-12 h-12 rounded-[var(--radius-sm)] flex items-center justify-center shrink-0 bg-[rgba(108,99,255,0.15)] text-[var(--clr-accent-2)]">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="7" height="7" rx="1" />
              <rect x="14" y="3" width="7" height="7" rx="1" />
              <rect x="3" y="14" width="7" height="7" rx="1" />
              <rect x="14" y="14" width="7" height="7" rx="1" />
            </svg>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-[var(--clr-text-2)]">Всього</p>
            <p className="text-3xl font-extrabold tracking-tight text-[var(--clr-text)] leading-none mt-1">{stats.total}</p>
          </div>
        </div>

        {/* Active Stat */}
        <div className="flex items-center gap-4 p-5 sm:p-6 bg-[var(--clr-surface)] border border-[var(--clr-border)] rounded-[var(--radius-md)] transition-all duration-200 hover:border-[var(--clr-border-hover)] hover:-translate-y-0.5 hover:shadow-md animate-fade-in-up">
          <div className="w-12 h-12 rounded-[var(--radius-sm)] flex items-center justify-center shrink-0 bg-emerald-500/15 text-emerald-400">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-[var(--clr-text-2)]">Активні</p>
            <p className="text-3xl font-extrabold tracking-tight text-emerald-400 leading-none mt-1">{stats.active}</p>
          </div>
        </div>

        {/* Pending Stat */}
        <div className="flex items-center gap-4 p-5 sm:p-6 bg-[var(--clr-surface)] border border-[var(--clr-border)] rounded-[var(--radius-md)] transition-all duration-200 hover:border-[var(--clr-border-hover)] hover:-translate-y-0.5 hover:shadow-md animate-fade-in-up">
          <div className="w-12 h-12 rounded-[var(--radius-sm)] flex items-center justify-center shrink-0 bg-amber-500/15 text-amber-400">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-[var(--clr-text-2)]">На модерації</p>
            <p className="text-3xl font-extrabold tracking-tight text-amber-400 leading-none mt-1">{stats.pending}</p>
          </div>
        </div>

        {/* Rejected Stat */}
        <div className="flex items-center gap-4 p-5 sm:p-6 bg-[var(--clr-surface)] border border-[var(--clr-border)] rounded-[var(--radius-md)] transition-all duration-200 hover:border-[var(--clr-border-hover)] hover:-translate-y-0.5 hover:shadow-md animate-fade-in-up">
          <div className="w-12 h-12 rounded-[var(--radius-sm)] flex items-center justify-center shrink-0 bg-red-500/15 text-red-400">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="15" y1="9" x2="9" y2="15" />
              <line x1="9" y1="9" x2="15" y2="15" />
            </svg>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-[var(--clr-text-2)]">Відхилені</p>
            <p className="text-3xl font-extrabold tracking-tight text-red-400 leading-none mt-1">{stats.rejected}</p>
          </div>
        </div>
      </div>

      {/* ── Filters ─────────────────────────────────────────────────────── */}
      <div className="flex flex-wrap items-end gap-4 p-5 sm:p-6 bg-[var(--clr-surface)] border border-[var(--clr-border)] rounded-[var(--radius-md)]">
        <div className="flex flex-col gap-1.5 flex-1 min-w-[160px]">
          <label htmlFor="status-filter" className="text-xs font-semibold uppercase tracking-wider text-[var(--clr-text-2)]">
            Статус
          </label>
          <select
            id="status-filter"
            className={`${formControlClasses} appearance-none pr-10 cursor-pointer bg-[url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='16'%20height='16'%20viewBox='0 0 24 24'%20fill='none'%20stroke='%2394a3b8'%20stroke-width='2'%3E%3Cpolyline%20points='6 9 12 15 18 9'/%3E%3C/svg%3E")] bg-no-repeat bg-[right_12px_center]`}
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            {STATUS_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1.5 flex-1 min-w-[160px]">
          <label htmlFor="tg-id-filter" className="text-xs font-semibold uppercase tracking-wider text-[var(--clr-text-2)]">
            Telegram ID
          </label>
          <input
            id="tg-id-filter"
            className={formControlClasses}
            type="text"
            inputMode="numeric"
            pattern="[0-9]*"
            placeholder="Пошук за tg_id..."
            value={tgIdFilter}
            onChange={(e) => setTgIdFilter(e.target.value)}
            min="1"
          />
        </div>

        <div className="flex items-center gap-2.5 pt-0.5">
          <button
            className="inline-flex items-center justify-center px-4 py-2.5 rounded-[var(--radius-sm)] text-sm font-semibold text-white bg-gradient-to-br from-[var(--clr-accent)] to-purple-600 shadow-[0_4px_14px_var(--clr-accent-glow)] transition-all duration-200 cursor-pointer hover:enabled:from-[var(--clr-accent-hover)] hover:enabled:to-purple-500 disabled:opacity-40 disabled:cursor-not-allowed"
            onClick={handleApplyFilters}
            id="apply-filters-btn"
            disabled={loading}
          >
            Застосувати
          </button>
          <button
            className="inline-flex items-center justify-center px-4 py-2.5 rounded-[var(--radius-sm)] text-sm font-medium text-[var(--clr-text-2)] transition-all duration-200 cursor-pointer hover:enabled:text-[var(--clr-text)] hover:enabled:bg-[var(--clr-surface-2)] disabled:opacity-40 disabled:cursor-not-allowed"
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
        <div className="flex flex-col items-center justify-center gap-5 py-20 px-10 text-center text-[var(--clr-text-3)] animate-fade-in-up">
          <Spinner size={48} />
          <p className="text-base text-[var(--clr-text-2)]">Завантаження оголошень...</p>
        </div>
      ) : error ? (
        <div className="flex flex-col items-center justify-center gap-5 py-20 px-10 text-center text-[var(--clr-rejected)] animate-fade-in-up">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <p className="text-base text-[var(--clr-text-2)]">{error}</p>
          <button
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-[var(--radius-sm)] text-sm font-medium bg-[var(--clr-surface)] border border-[var(--clr-border)] text-[var(--clr-text-2)] transition-all duration-200 cursor-pointer hover:text-[var(--clr-text)] hover:border-[var(--clr-border-hover)] hover:bg-[var(--clr-surface-2)]"
            onClick={() => fetchWithFilters()}
          >
            Спробувати знову
          </button>
        </div>
      ) : paginated.length === 0 ? (
        <div className="flex flex-col items-center justify-center gap-5 py-20 px-10 text-center text-[var(--clr-text-3)] animate-fade-in-up">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
          <p className="text-base text-[var(--clr-text-2)]">Оголошень не знайдено</p>
          <Link
            to="/create-ad"
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-[var(--radius-sm)] text-sm font-semibold text-white bg-gradient-to-br from-[var(--clr-accent)] to-purple-600 shadow-[0_4px_14px_var(--clr-accent-glow)] transition-all duration-200 hover:from-[var(--clr-accent-hover)] hover:to-purple-500"
          >
            Створити перше оголошення
          </Link>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" id="ads-grid">
            {paginated.map((ad) => (
              <AdCard key={ad.id} ad={ad} />
            ))}
          </div>

          {/* ── Pagination ────────────────────────────────────────────── */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2 pt-4 flex-wrap" role="navigation" aria-label="Pagination">
              <button
                className="min-w-[36px] h-9 px-2.5 rounded-[var(--radius-sm)] border border-[var(--clr-border)] bg-[var(--clr-surface)] text-[var(--clr-text-2)] text-sm font-medium inline-flex items-center justify-center transition-all duration-200 hover:enabled:bg-[var(--clr-surface-2)] hover:enabled:text-[var(--clr-text)] hover:enabled:border-[var(--clr-border-hover)] disabled:opacity-30 disabled:cursor-not-allowed"
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                id="prev-page-btn"
                aria-label="Попередня сторінка"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="15 18 9 12 15 6" />
                </svg>
              </button>

              <div className="flex items-center gap-1.5">
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
                      <span key={`ellipsis-${idx}`} className="min-w-[36px] text-center text-sm text-[var(--clr-text-3)]">
                        …
                      </span>
                    ) : (
                      <button
                        key={item}
                        className={`min-w-[36px] h-9 px-2.5 rounded-[var(--radius-sm)] border text-sm font-medium inline-flex items-center justify-center transition-all duration-200 ${
                          page === item
                            ? 'bg-gradient-to-br from-[var(--clr-accent)] to-purple-600 border-transparent text-white shadow-[0_4px_12px_var(--clr-accent-glow)]'
                            : 'bg-[var(--clr-surface)] border-[var(--clr-border)] text-[var(--clr-text-2)] hover:bg-[var(--clr-surface-2)] hover:text-[var(--clr-text)] hover:border-[var(--clr-border-hover)]'
                        }`}
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
                className="min-w-[36px] h-9 px-2.5 rounded-[var(--radius-sm)] border border-[var(--clr-border)] bg-[var(--clr-surface)] text-[var(--clr-text-2)] text-sm font-medium inline-flex items-center justify-center transition-all duration-200 hover:enabled:bg-[var(--clr-surface-2)] hover:enabled:text-[var(--clr-text)] hover:enabled:border-[var(--clr-border-hover)] disabled:opacity-30 disabled:cursor-not-allowed"
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                id="next-page-btn"
                aria-label="Наступна сторінка"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="9 18 15 12 9 6" />
                </svg>
              </button>

              <span className="text-[0.8125rem] text-[var(--clr-text-3)] ml-2">
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