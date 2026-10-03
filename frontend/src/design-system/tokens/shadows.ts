/**
 * Shadow design tokens for JurisPulse
 *
 * Shadows use the ink base color (#18231d) at low opacity so they blend
 * naturally with both light and dark surfaces.  Avoid pure-black shadows.
 *
 * Elevation model (low → high):
 *   xs   – dividers, subtle separators
 *   sm   – cards on flat backgrounds
 *   md   – raised cards, dropdowns
 *   lg   – drawers, side panels
 *   xl   – modals, dialogs
 *   2xl  – full-screen overlays
 */

const INK = '24,35,29'; // RGB channels of --color-ink (#18231d)

// ── Elevation shadows ──────────────────────────────────────────────────────
export const shadow = {
  none: 'none',
  xs:   `0 1px 2px rgba(${INK},0.06)`,
  sm:   `0 1px 4px rgba(${INK},0.08), 0 1px 2px rgba(${INK},0.04)`,
  md:   `0 4px 12px rgba(${INK},0.10), 0 1px 3px rgba(${INK},0.06)`,
  lg:   `0 8px 24px rgba(${INK},0.12), 0 2px 6px rgba(${INK},0.06)`,
  xl:   `0 16px 48px rgba(${INK},0.14), 0 4px 12px rgba(${INK},0.08)`,
  '2xl':`0 24px 64px rgba(${INK},0.18), 0 8px 24px rgba(${INK},0.10)`,
} as const;

// ── Focus ring shadows (used in conjunction with outline) ──────────────────
export const focusRing = {
  primary: `0 0 0 3px rgba(94,188,56,0.35)`,   // primary-500 halo
  danger:  `0 0 0 3px rgba(231,111,81,0.30)`,  // danger-400 halo
  neutral: `0 0 0 3px rgba(143,162,153,0.30)`, // ink-muted halo
} as const;

// ── Inset / inner shadows ──────────────────────────────────────────────────
export const innerShadow = {
  sm: `inset 0 1px 2px rgba(${INK},0.06)`,
  md: `inset 0 2px 4px rgba(${INK},0.08)`,
} as const;

// ── Semantic elevation map ─────────────────────────────────────────────────
export const componentShadow = {
  card:       shadow.sm,
  cardHover:  shadow.md,
  dropdown:   shadow.md,
  drawer:     shadow.lg,
  modal:      shadow.xl,
  toast:      shadow.lg,
  tooltip:    shadow.sm,
  focusPrimary: focusRing.primary,
} as const;

export type ShadowKey = keyof typeof shadow;

export const shadows = { shadow, focusRing, innerShadow, componentShadow } as const;
