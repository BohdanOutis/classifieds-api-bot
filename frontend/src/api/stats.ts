import apiClient from "./axios";

export const getStats = async () => {
    const {data} = await apiClient.get('api/v1/stats');
    return data;
};