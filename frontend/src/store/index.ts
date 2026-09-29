import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import adsReducer from './adsSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    ads: adsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
