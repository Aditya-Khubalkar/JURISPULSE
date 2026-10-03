/**
 * Border-radius design tokens for JurisPulse
 *
 * Radius values are intentionally small – the legal-tech aesthetic is
 * professional and structured, not playful.  Use 'full' only for badges,
 * avatar images, and tag pills.
 */

// ── Radius scale ───────────────────────────────────────────────────────────
export const radius = {
  none:  '0',
  xs:    '4px',
  sm:    '6px',
  md:    '8px',
  lg:    '12px',
  xl:    '16px',
  '2xl': '24px',
  '3xl': '32px',
  full:  '9999px',
} as const;

// ── Semantic role map ──────────────────────────────────────────────────────
/** Which radius token to use for each common component shape */
export const componentRadius = {
  button:        radius.md,
  buttonRound:   radius.full,
  input:         radius.md,
  card:          radius.lg,
  cardNested:    radius.md,
  modal:         radius.xl,
  drawer:        radius.lg,
  tooltip:       radius.sm,
  badge:         radius.full,
  avatar:        radius.full,
  tag:           radius.full,
  dropdown:      radius.lg,
  toast:         radius.lg,
  progressBar:   radius.full,
  skeleton:      radius.sm,
  sidebar:       radius.none,
  divider:       radius.none,
} as const;

export type RadiusKey = keyof typeof radius;
export type ComponentRadiusKey = keyof typeof componentRadius;

export const radii = { radius, componentRadius } as const;
