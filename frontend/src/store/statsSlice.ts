import { createSlice } from "@reduxjs/toolkit";


interface statsState{
    "total_users": number,
    "total_ads": number,
    "total_revenue": number,
}

const initialState: statsState = {
    "total_users": 0,
    "total_ads": 0,
    "total_revenue": 0,
}

const statsSlice = createSlice({
    name: 'stats',
    initialState,
    reducers:{
    }
})

export default statsSlice.reducer;