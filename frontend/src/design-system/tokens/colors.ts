/**
 * Color design tokens for JurisPulse
 *
 * Primary: Forest-green legal palette  (#1f6b45 → #5cbc38)
 * Accent:  Warm amber                  (#edb53a)
 * Ink:     Near-black text on light bg / near-white on dark
 *
 * Every CSS custom property in globals.css maps 1-to-1 to a constant here
 * so TypeScript components can reference tokens without hard-coding hex values.
 */

// ── Primary palette ────────────────────────────────────────────────────────
export const primary = {
  50:  '#f5fcf2',
  100: '#e9f8e5',
  200: '#cdefca',
  300: '#a3df9e',
  400: '#7ed957',
  500: '#5cbc38',
  600: '#3e9a24',
  700: '#1f6b45',
  800: '#174a35',
  900: '#0f3024',
} as const;

// ── Accent palette ─────────────────────────────────────────────────────────
export const accent = {
  400: '#f4c95d',
  500: '#edb53a',
} as const;

// ── Warning palette ────────────────────────────────────────────────────────
export const warning = {
  100: '#fef3c7',
  400: '#f4a261',
  500: '#e8883c',
} as const;

// ── Danger palette ─────────────────────────────────────────────────────────
export const danger = {
  100: '#fde8e3',
  400: '#e76f51',
  500: '#d4502f',
} as const;

// ── Semantic surface tokens (light) ────────────────────────────────────────
export const surface = {
  default:  '#f8faf7',
  raised:   '#ffffff',
  overlay:  '#f0f5ef',
} as const;

// ── Semantic ink tokens (light) ────────────────────────────────────────────
export const ink = {
  default:   '#18231d',
  secondary: '#65736b',
  muted:     '#8fa299',
  disabled:  '#b8c4be',
} as const;

// ── Border tokens (light) ──────────────────────────────────────────────────
export const border = {
  default: '#dde7df',
  strong:  '#b8cebe',
} as const;

// ── Dark-mode surface overrides ────────────────────────────────────────────
export const surfaceDark = {
  default:  '#121212',
  raised:   '#1e1e1e',
  overlay:  '#2a2a2a',
} as const;

// ── Dark-mode ink overrides ────────────────────────────────────────────────
export const inkDark = {
  default:   '#f0f5ef',
  secondary: '#b8cebe',
  muted:     '#8fa299',
  disabled:  '#65736b',
} as const;

// ── Dark-mode border overrides ─────────────────────────────────────────────
export const borderDark = {
  default: '#333333',
  strong:  '#4a4a4a',
} as const;

// ── Status semantic colors ─────────────────────────────────────────────────
export const status = {
  active:    { text: '#1f6b45', bg: '#e9f8e5' },
  pending:   { text: '#b45309', bg: '#fef3c7' },
  closed:    { text: '#65736b', bg: '#f0f5ef' },
  urgent:    { text: '#d4502f', bg: '#fde8e3' },
  draft:     { text: '#6366f1', bg: '#eef2ff' },
  verified:  { text: '#1f6b45', bg: '#e9f8e5' },
  reviewing: { text: '#92400e', bg: '#fef3c7' },
  failed:    { text: '#d4502f', bg: '#fde8e3' },
} as const;

export type StatusKey = keyof typeof status;

// ── Collected export ───────────────────────────────────────────────────────
export const colors = { primary, accent, warning, danger, surface, ink, border, status } as const;
