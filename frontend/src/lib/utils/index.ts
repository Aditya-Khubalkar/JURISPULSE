import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { format, formatDistanceToNow, parseISO, isToday, isTomorrow } from 'date-fns';

// ── Class Name Utility ────────────────────────────────────────────────────────

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

// ── Date Formatting ───────────────────────────────────────────────────────────

export function formatDate(date: string | Date, fmt = 'dd MMM yyyy'): string {
  try {
    const d = typeof date === 'string' ? parseISO(date) : date;
    return format(d, fmt);
  } catch {
    return '—';
  }
}

export function formatDateTime(date: string | Date): string {
  return formatDate(date, 'dd MMM yyyy, hh:mm a');
}

export function formatRelativeTime(date: string | Date): string {
  try {
    const d = typeof date === 'string' ? parseISO(date) : date;
    if (isToday(d)) return `Today, ${format(d, 'hh:mm a')}`;
    if (isTomorrow(d)) return `Tomorrow, ${format(d, 'hh:mm a')}`;
    return formatDistanceToNow(d, { addSuffix: true });
  } catch {
    return '—';
  }
}

export function formatHearingDate(date: string): string {
  try {
    const d = parseISO(date);
    if (isToday(d)) return `Today`;
    if (isTomorrow(d)) return `Tomorrow`;
    return format(d, 'dd MMM yyyy');
  } catch {
    return '—';
  }
}

// ── File Size Formatting ──────────────────────────────────────────────────────

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}

// ── String Utilities ──────────────────────────────────────────────────────────

export function truncate(str: string, maxLength: number): string {
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength).trimEnd() + '…';
}

export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function toTitleCase(str: string): string {
  return str.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

export function getInitials(name: string): string {
  return name
    .split(' ')
    .slice(0, 2)
    .map((n) => n.charAt(0).toUpperCase())
    .join('');
}

// ── Number Formatting ─────────────────────────────────────────────────────────

export function formatNumber(n: number): string {
  return new Intl.NumberFormat('en-IN').format(n);
}

export function formatPercentage(n: number, decimals = 1): string {
  return `${n.toFixed(decimals)}%`;
}

// ── Confidence Utilities ──────────────────────────────────────────────────────

export function getConfidenceLabel(score: number): string {
  if (score >= 0.9) return 'Very High';
  if (score >= 0.75) return 'High';
  if (score >= 0.6) return 'Moderate';
  if (score >= 0.4) return 'Low';
  return 'Very Low';
}

export function getConfidenceColor(score: number): string {
  if (score >= 0.75) return 'text-green-700 bg-green-50';
  if (score >= 0.5) return 'text-amber-700 bg-amber-50';
  return 'text-red-700 bg-red-50';
}

// ── Status Color Utilities ────────────────────────────────────────────────────

export function getCaseStatusColor(status: string): string {
  const map: Record<string, string> = {
    active: 'text-green-700 bg-green-50 border-green-200',
    pending: 'text-amber-700 bg-amber-50 border-amber-200',
    closed: 'text-gray-600 bg-gray-50 border-gray-200',
    stayed: 'text-purple-700 bg-purple-50 border-purple-200',
    disposed: 'text-blue-700 bg-blue-50 border-blue-200',
    appeal: 'text-orange-700 bg-orange-50 border-orange-200',
  };
  return map[status] ?? 'text-gray-600 bg-gray-50 border-gray-200';
}

export function getPriorityColor(priority: string): string {
  const map: Record<string, string> = {
    critical: 'text-red-700 bg-red-50 border-red-200',
    high: 'text-orange-700 bg-orange-50 border-orange-200',
    medium: 'text-amber-700 bg-amber-50 border-amber-200',
    low: 'text-gray-600 bg-gray-50 border-gray-200',
  };
  return map[priority] ?? 'text-gray-600 bg-gray-50 border-gray-200';
}

export function getDocumentStatusColor(status: string): string {
  const map: Record<string, string> = {
    uploaded: 'text-blue-700 bg-blue-50 border-blue-200',
    processing: 'text-amber-700 bg-amber-50 border-amber-200',
    processed: 'text-green-700 bg-green-50 border-green-200',
    needs_review: 'text-orange-700 bg-orange-50 border-orange-200',
    verified: 'text-green-800 bg-green-100 border-green-300',
    failed: 'text-red-700 bg-red-50 border-red-200',
  };
  return map[status] ?? 'text-gray-600 bg-gray-50 border-gray-200';
}

export function getVerificationStatusColor(status: string): string {
  const map: Record<string, string> = {
    verified: 'text-green-700 bg-green-50 border-green-200',
    partial: 'text-amber-700 bg-amber-50 border-amber-200',
    unsupported: 'text-red-700 bg-red-50 border-red-200',
    contradicted: 'text-red-800 bg-red-100 border-red-300',
    pending: 'text-gray-600 bg-gray-50 border-gray-200',
  };
  return map[status] ?? 'text-gray-600 bg-gray-50 border-gray-200';
}

export function getAgentStatusColor(status: string): string {
  const map: Record<string, string> = {
    running: 'text-blue-700 bg-blue-50',
    completed: 'text-green-700 bg-green-50',
    queued: 'text-gray-600 bg-gray-50',
    waiting: 'text-amber-700 bg-amber-50',
    failed: 'text-red-700 bg-red-50',
    paused: 'text-purple-700 bg-purple-50',
  };
  return map[status] ?? 'text-gray-600 bg-gray-50';
}

// ── URL Utilities ─────────────────────────────────────────────────────────────

export function buildQueryString(params: Record<string, string | number | boolean | undefined>): string {
  const qs = new URLSearchParams();
  for (const [key, val] of Object.entries(params)) {
    if (val !== undefined && val !== '') {
      qs.append(key, String(val));
    }
  }
  return qs.toString() ? `?${qs.toString()}` : '';
}

// ── Array Utilities ───────────────────────────────────────────────────────────

export function groupBy<T>(arr: T[], key: keyof T): Record<string, T[]> {
  return arr.reduce((acc, item) => {
    const group = String(item[key]);
    if (!acc[group]) acc[group] = [];
    acc[group].push(item);
    return acc;
  }, {} as Record<string, T[]>);
}

export function unique<T>(arr: T[]): T[] {
  return [...new Set(arr)];
}

// ── Debounce ──────────────────────────────────────────────────────────────────

export function debounce<T extends (...args: unknown[]) => unknown>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// ── Storage Utilities ─────────────────────────────────────────────────────────

export function safeJsonParse<T>(str: string | null, fallback: T): T {
  if (!str) return fallback;
  try {
    return JSON.parse(str) as T;
  } catch {
    return fallback;
  }
}

// ── Error Message Extraction ──────────────────────────────────────────────────

export function getErrorMessage(error: unknown): string {
  if (typeof error === 'string') return error;
  if (error instanceof Error) return error.message;
  if (typeof error === 'object' && error !== null && 'message' in error) {
    return String((error as { message: unknown }).message);
  }
  return 'An unexpected error occurred';
}

export function getHttpErrorMessage(status: number): string {
  const messages: Record<number, string> = {
    400: 'Invalid request. Please check your input.',
    401: 'Your session has expired. Please log in again.',
    403: 'You do not have permission to perform this action.',
    404: 'The requested resource was not found.',
    409: 'A conflict occurred. This resource may already exist.',
    422: 'The data provided is invalid.',
    429: 'Too many requests. Please wait a moment and try again.',
    500: 'Something went wrong on our end. Please try again.',
    502: 'Service temporarily unavailable. Please try again.',
    503: 'The service is currently unavailable. Please try again later.',
  };
  return messages[status] ?? 'An unexpected error occurred.';
}
