/**
 * Responsive breakpoints design tokens for JurisPulse
 *
 * Breakpoints follow a mobile-first approach.  The values here match the
 * CSS custom properties in globals.css (--breakpoint-*) so TypeScript
 * helpers and CSS are always in sync.
 *
 * Usage in components:
 *   import { bp, mq } from '@/design-system/tokens/breakpoints';
 *   const style = { [`@media ${mq.md}`]: { display: 'grid' } };
 */

// ── Pixel values ───────────────────────────────────────────────────────────
export const bp = {
  sm:  640,   // Small devices (landscape phones)
  md:  768,   // Medium devices (tablets)
  lg:  1024,  // Large devices (desktops)
  xl:  1280,  // Extra-large devices (wide desktops)
  '2xl': 1536, // Ultra-wide
} as const;

// ── rem values (for CSS-in-JS) ─────────────────────────────────────────────
export const bpRem = {
  sm:    '40rem',   // 640px
  md:    '48rem',   // 768px
  lg:    '64rem',   // 1024px
  xl:    '80rem',   // 1280px
  '2xl': '96rem',   // 1536px
} as const;

// ── Media query strings (min-width, mobile-first) ──────────────────────────
export const mq = {
  sm:    `(min-width: ${bp.sm}px)`,
  md:    `(min-width: ${bp.md}px)`,
  lg:    `(min-width: ${bp.lg}px)`,
  xl:    `(min-width: ${bp.xl}px)`,
  '2xl': `(min-width: ${bp['2xl']}px)`,
} as const;

// ── Max-width queries (for mobile-only logic) ──────────────────────────────
export const mqMax = {
  xs:  `(max-width: ${bp.sm - 1}px)`,   // < 640px – phones
  sm:  `(max-width: ${bp.md - 1}px)`,   // < 768px – phones + small tablets
  md:  `(max-width: ${bp.lg - 1}px)`,   // < 1024px – tablets
  lg:  `(max-width: ${bp.xl - 1}px)`,   // < 1280px – laptops
} as const;

// ── Container max-widths ───────────────────────────────────────────────────
export const containerWidth = {
  sm:    '640px',
  md:    '768px',
  lg:    '1024px',
  xl:    '1280px',
  '2xl': '1440px',
  prose: '72ch',    // optimal reading width for legal text
  form:  '480px',   // standard form max-width
} as const;

// ── Layout column counts per breakpoint ────────────────────────────────────
export const gridCols = {
  default: 1,
  sm:      1,
  md:      2,
  lg:      3,
  xl:      4,
} as const;

export type BreakpointKey = keyof typeof bp;

export const breakpoints = { bp, bpRem, mq, mqMax, containerWidth, gridCols } as const;
