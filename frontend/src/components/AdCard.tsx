import type { AdvertResponse } from '../types/api';
import StatusBadge from './StatusBadge';

interface AdCardProps {
  ad: AdvertResponse;
}

const categoryLabels: Record<string, string> = {
  other: 'Інше',
  electronics: 'Електроніка',
  clothing: 'Одяг',
  vehicles: 'Транспорт',
  realestate: 'Нерухомість',
  services: 'Послуги',
  furniture: 'Меблі',
};

const AdCard = ({ ad }: AdCardProps) => {
  const categoryLabel = categoryLabels[ad.category] ?? ad.category;

  return (
    <article className="group relative flex flex-col gap-3 rounded-radius-md border border-(--clr-border) bg-(--clr-surface) p-5 overflow-hidden transition-all duration-300 animate-[fadeInUp_350ms_ease_both] hover:-translate-y-1 hover:border-(--clr-border-hover) hover:shadow-md before:absolute before:top-0 before:inset-x-0 before:h-[2px] before:bg-gradient-to-r before:from-(--clr-accent) before:to-[#8b5cf6] before:opacity-0 before:transition-opacity hover:before:opacity-100">
      
      {/* Header */}
      <div className="flex items-center justify-between gap-2">
        <span className="text-[0.7rem] font-semibold uppercase tracking-wider text-(--clr-accent-2) bg-[#6c63ff]/10 px-2.5 py-0.5 rounded-full border border-[#6c63ff]/20">
          {categoryLabel}
        </span>
        <StatusBadge status={ad.status} />
      </div>

      {/* Title */}
      <h3 className="text-base font-bold text-(--clr-text) leading-snug line-clamp-2" title={ad.name}>
        {ad.name}
      </h3>

      {/* Description */}
      <p className="text-[0.8125rem] text-(--clr-text-2) leading-relaxed line-clamp-3 flex-1">
        {ad.description}
      </p>

      {/* Footer */}
      <div className="flex items-center justify-between mt-auto pt-3 border-t border-(--clr-border)">
        <span className="text-lg font-extrabold text-(--clr-text) tracking-tight">
          {ad.price.toLocaleString('uk-UA')} ₴
        </span>
        
        <div className="flex items-center gap-2.5">
          <span className="text-xs text-(--clr-text-3) font-mono">
            #{ad.id}
          </span>
          {ad.user_id && (
            <span className="flex items-center gap-1 text-xs text-(--clr-text-3)" title="Telegram ID">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
              </svg>
              {ad.user_id}
            </span>
          )}
        </div>
      </div>
    </article>
  );
};

export default AdCard;