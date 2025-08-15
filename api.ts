import Constants from 'expo-constants';
const API_URL = (Constants?.expoConfig?.extra as any)?.API_URL || 'http://127.0.0.1:8000';
export async function api(path: string, opts: RequestInit = {}) {
  const res = await fetch(`${API_URL}${path}`, { headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) }, ...opts });
  if (!res.ok) { const text = await res.text(); throw new Error(`HTTP ${res.status}: ${text}`); }
  const ct = res.headers.get('content-type') || '';
  return ct.includes('application/json') ? res.json() : res.text();
}
