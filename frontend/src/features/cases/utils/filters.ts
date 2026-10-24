export function filterOpenCases<T extends { status: string }>(cases: T[]): T[] {
  return cases.filter(c => c.status === 'open' || c.status === 'in_progress');
}
