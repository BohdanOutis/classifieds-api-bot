import apiClient from './axios';
import type { UserResponse, UserCreate, UserUpdate } from '../types/api';

export const createUser = async (payload: UserCreate): Promise<UserResponse> => {
  const { data } = await apiClient.post<UserResponse>('/api/v1/users/', payload);
  return data;
};

export const getUserByTgId = async (tg_id: number): Promise<UserResponse> => {
  const { data } = await apiClient.get<UserResponse>(`/api/v1/users/${tg_id}`);
  return data;
};

export const getUserByUsername = async (username: string): Promise<UserResponse> => {
  const { data } = await apiClient.get<UserResponse>(`/api/v1/users/by-username/${username}`);
  return data;
};

export const updateUser = async (tg_id: number, payload: UserUpdate): Promise<UserResponse> => {
  const { data } = await apiClient.patch<UserResponse>(`/api/v1/users/${tg_id}`, payload);
  return data;
};

export const activateVip = async (tg_id: number, days = 30): Promise<void> => {
  await apiClient.patch(`/api/v1/users/${tg_id}/activate-vip`, null, { params: { days } });
};
