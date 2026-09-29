import apiClient from './axios';
import type { AdvertCreate, AdvertUpdate, AdvertResponse, AdsQueryParams } from '../types/api';

export const getAds = async (params?: AdsQueryParams): Promise<AdvertResponse[]> => {
  const { data } = await apiClient.get<AdvertResponse[]>('/api/v1/ads/', { params });
  return data;
};

export const getAdById = async (id: number): Promise<AdvertResponse> => {
  const { data } = await apiClient.get<AdvertResponse>(`/api/v1/ads/${id}`);
  return data;
};

export const createAd = async (payload: AdvertCreate): Promise<AdvertResponse> => {
  const { data } = await apiClient.post<AdvertResponse>('/api/v1/ads/', payload);
  return data;
};

export const updateAd = async (id: number, payload: AdvertUpdate): Promise<AdvertResponse> => {
  const { data } = await apiClient.patch<AdvertResponse>(`/api/v1/ads/${id}`, payload);
  return data;
};