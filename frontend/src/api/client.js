import axios from 'axios'

// The browser may see VITE_ variables, so this contains only the public API URL.
export const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL })

export function setAccessToken(token) {
  // Keep the token in memory; page refreshes deliberately require a fresh sign-in.
  if (token) api.defaults.headers.common.Authorization = `Bearer ${token}`
  else delete api.defaults.headers.common.Authorization
}

api.interceptors.response.use(
  (response) => response.data,
  (response) => Promise.reject(response.response?.data ?? { error: 'Network error. Is Flask running?' }),
)
