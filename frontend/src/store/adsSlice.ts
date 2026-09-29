import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

import type { AdvertResponse, AdvertCreate, AdsQueryParams } from '../types/api';
import { getAds, createAd } from '../api/ads';

interface AdsState {
  ads: AdvertResponse[];
  loading: boolean;
  error: string | null;
  creating: boolean;
}

const initialState: AdsState = {
  ads: [],
  loading: false,
  error: null,
  creating: false,
};


export const fetchAds = createAsyncThunk<AdvertResponse[], AdsQueryParams | undefined>(
  'ads/fetchAds',
  async (params, { rejectWithValue }) => {
    try {
      return await getAds(params);
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : 'Не вдалося завантажити оголошення';
      return rejectWithValue(message);
    }
  },
);

export const createAdThunk = createAsyncThunk<AdvertResponse, AdvertCreate>(
  'ads/createAd',
  async (payload, { rejectWithValue }) => {
    try {
      return await createAd(payload);
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : 'Не вдалося створити оголошення';
      return rejectWithValue(message);
    }
  },
);


const adsSlice = createSlice({
  name: 'ads',
  initialState,
  reducers: {
    clearAdsError(state) {
      state.error = null;
    },
    addAd(state, action: PayloadAction<AdvertResponse>) {
      state.ads.unshift(action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      // fetchAds
      .addCase(fetchAds.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAds.fulfilled, (state, action) => {
        state.loading = false;
        state.ads = action.payload;
      })
      .addCase(fetchAds.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // createAdThunk
      .addCase(createAdThunk.pending, (state) => {
        state.creating = true;
        state.error = null;
      })
      .addCase(createAdThunk.fulfilled, (state, action) => {
        state.creating = false;
        state.ads.unshift(action.payload);
      })
      .addCase(createAdThunk.rejected, (state, action) => {
        state.creating = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearAdsError, addAd } = adsSlice.actions;
export default adsSlice.reducer;
