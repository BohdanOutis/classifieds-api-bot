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
    <article className="ad-card">
      <div className="ad-card__header">
        <span className="ad-card__category">{categoryLabel}</span>
        <StatusBadge status={ad.status} />
      </div>

      <h3 className="ad-card__title" title={ad.name}>
        {ad.name}
      </h3>

      <p className="ad-card__description">{ad.description}</p>

      <div className="ad-card__footer">
        <span className="ad-card__price">{ad.price.toLocaleString('uk-UA')} ₴</span>
        <div className="ad-card__meta">
          <span className="ad-card__id">#{ad.id}</span>
          {ad.user_id && (
            <span className="ad-card__user" title="Telegram ID">
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