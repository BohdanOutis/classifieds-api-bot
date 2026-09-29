import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';


interface AuthState {
  apiKey: string | null;
  isAuthenticated: boolean;
}

const storedKey = localStorage.getItem('api_key');

const initialState: AuthState = {
  apiKey: storedKey,
  isAuthenticated: !!storedKey,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setApiKey(state, action: PayloadAction<string>) {
      state.apiKey = action.payload;
      state.isAuthenticated = true;
      localStorage.setItem('api_key', action.payload);
    },
    logout(state) {
      state.apiKey = null;
      state.isAuthenticated = false;
      localStorage.removeItem('api_key');
    },
  },
});

export const { setApiKey, logout } = authSlice.actions;
export default authSlice.reducer;