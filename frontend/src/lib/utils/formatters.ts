export function formatINR(amount: number): string {
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(amount);
}
export function formatDateIST(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-IN', { timeZone: 'Asia/Kolkata' });
}
