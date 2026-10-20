export async function apiClient(url: string, opts = {}) {
  return fetch(url, opts).then(r => r.json());
}
