import { useEffect, useMemo } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks/useStore';
import { fetchAds } from '../store/adsSlice';
import Spinner from '../components/Spinner';

const StatsPage = () => {
  const dispatch = useAppDispatch();
  const { ads, loading, error } = useAppSelector((s) => s.ads);

  useEffect(() => {
    if (!ads.length) {
      dispatch(fetchAds());
    }
  }, [dispatch, ads.length]);

  // Підрахунок метрик з Redux-стору
  const { totalUsers, totalAds, totalRevenue } = useMemo(() => {
    const totalAds = ads.length;
    // Унікальні користувачі за tg_id (або user_id)
    const totalUsers = new Set(ads.map((a) => a.tg_id)).size;
    // Сума оголошень
    const totalRevenue = ads.reduce((acc, ad) => acc + (ad.price || 0), 0);

    return { totalUsers, totalAds, totalRevenue };
  }, [ads]);

  if (loading && !ads.length) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[300px] gap-3">
        <Spinner size={32} />
        <p className="text-sm text-(--clr-text-2)">Завантаження статистики...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 text-center text-red-400">
        <p>Не вдалося завантажити дані: {error}</p>
      </div>
    );
  }

  return (
    <div className="px-9 py-8 max-w-[1400px] [animation:fadeInUp_350ms_ease]">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-8 flex-wrap">
        <div>
          <h1 className="text-[1.75rem] font-[800] text-(--clr-text) tracking-[-0.03em] leading-[1.2]">
            Статистика
          </h1>
          <p className="text-sm text-(--clr-text-2) mt-1">Статистика сервісу</p>
        </div>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-3 gap-4 mb-7 max-lg:grid-cols-2 max-sm:grid-cols-1">
        {/* Users */}
        <div className="flex items-center gap-4 px-6 py-5 bg-(--clr-surface) border border-(--clr-border) rounded-[--radius-md] transition-all duration-[220ms] [animation:fadeInUp_350ms_ease_both] hover:border-(--clr-border-hover) hover:-translate-y-[2px] hover:shadow-[0_4px_16px_rgba(0,0,0,0.5)]">
          <div className="w-12 h-12 rounded-[--radius-sm] flex items-center justify-center shrink-0 bg-[#6c63ff]/15 text-(--clr-accent-2)">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
            </svg>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.05em] text-(--clr-text-2)">Кількість юзерів</p>
            <p className="text-[2rem] font-[800] leading-none text-(--clr-text) tracking-[-0.04em] mt-1">
              {totalUsers}
            </p>
          </div>
        </div>

        {/* Ads */}
        <div className="flex items-center gap-4 px-6 py-5 bg-(--clr-surface) border border-(--clr-border) rounded-[--radius-md] transition-all duration-[220ms] [animation:fadeInUp_350ms_ease_both] hover:border-(--clr-border-hover) hover:-translate-y-[2px] hover:shadow-[0_4px_16px_rgba(0,0,0,0.5)]">
          <div className="w-12 h-12 rounded-[--radius-sm] flex items-center justify-center shrink-0 bg-[#22c55e]/15 text-[#4ade80]">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.05em] text-(--clr-text-2)">Кількість оголошень</p>
            <p className="text-[2rem] font-[800] leading-none text-[#4ade80] tracking-[-0.04em] mt-1">
              {totalAds}
            </p>
          </div>
        </div>

        {/* Revenue */}
        <div className="flex items-center gap-4 px-6 py-5 bg-(--clr-surface) border border-(--clr-border) rounded-[--radius-md] transition-all duration-[220ms] [animation:fadeInUp_350ms_ease_both] hover:border-(--clr-border-hover) hover:-translate-y-[2px] hover:shadow-[0_4px_16px_rgba(0,0,0,0.5)]">
          <div className="w-12 h-12 rounded-[--radius-sm] flex items-center justify-center shrink-0 bg-[#f59e0b]/15 text-[#fbbf24]">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="12" y1="1" x2="12" y2="23"/>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.05em] text-(--clr-text-2)">Загальний заробіток</p>
            <p className="text-[2rem] font-[800] leading-none text-[#fbbf24] tracking-[-0.04em] mt-1">
              {totalRevenue.toLocaleString('uk-UA')} ₴
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatsPage;