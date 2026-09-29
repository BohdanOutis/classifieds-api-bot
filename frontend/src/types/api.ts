// ─── Advertisement ────────────────────────────────────────────────────────────

export interface AdvertCreate {
  name: string;
  description: string;
  price: number;
  category?: string;
  tg_id: number;
}

export interface AdvertUpdate {
  name?: string | null;
  description?: string | null;
  price?: number | null;
  category?: string | null;
  status?: string | null;
  wp_post_id?: number | null;
}

export interface AdvertResponse {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  user_id: number;
  status: string;
  wp_post_id: number | null;
}

// ─── Advertisement Photos ─────────────────────────────────────────────────────

export interface AdvertPhotoCreate {
  advert_id: number;
  file_ids: string[];
}

export interface AdvertPhotoResponse {
  id: number;
  advert_id: number;
  file_id: string;
}

// ─── Users ────────────────────────────────────────────────────────────────────

export interface UserCreate {
  tg_id: number;
  name: string;
}

export interface UserUpdate {
  username?: string | null;
  status?: string | null;
  is_vip?: boolean | null;
  vip_expires_at?: string | null;
}

export interface UserResponse {
  id: number;
  tg_id: number;
  name: string;
  status: string;
  is_vip: boolean;
  created_at: string;
}

// ─── Payments ────────────────────────────────────────────────────────────────

export type PaymentStatus = 'pending' | 'success' | 'failed' | 'cancelled';
export type PaymentType = 'vip_subscription' | 'product_purchase';

export interface PaymentCreate {
  user_id: number;
  shop_order_number: string;
  amount: number | string;
  currency?: string;
  service_type: PaymentType;
  status?: PaymentStatus;
  ad_id?: number | null;
  provider?: string;
  external_payment_id?: string | null;
}

// ─── News ─────────────────────────────────────────────────────────────────────

export interface NewsSourceResponse {
  id: number;
  name: string;
  url: string;
  is_active: boolean;
}

export interface ProcessedNewsCreate {
  source_id: number;
  news_hash: string;
  title: string;
  link: string;
}

export interface ProcessedNewsResponse {
  id: number;
  source_id: number;
  news_hash: string;
  title: string;
  link: string;
  created_at: string;
}

// ─── API Filters ─────────────────────────────────────────────────────────────

export interface AdsQueryParams {
  tg_id?: number;
  status?: string;
}
