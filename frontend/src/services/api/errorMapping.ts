export function mapHttpError(code: number) {
  if (code === 401) return 'Session expired.';
  if (code === 403) return 'Access denied.';
  return 'An error occurred.';
}
