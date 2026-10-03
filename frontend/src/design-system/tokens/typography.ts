/**
 * Typography design tokens for JurisPulse
 *
 * Two font families:
 *   sans  – Inter (UI chrome, navigation, labels, data)
 *   serif – Lora  (legal document bodies, quoted text, print output)
 *
 * Scale follows a modified major-third ratio (1.25×) anchored at 1 rem.
 * Line-height values are intentionally unitless so they scale with font-size.
 */

// ── Font families ──────────────────────────────────────────────────────────
export const fontFamily = {
  sans:  "'Inter', system-ui, -apple-system, sans-serif",
  serif: "'Lora', Georgia, serif",
  mono:  "'JetBrains Mono', 'Fira Code', ui-monospace, monospace",
} as const;

// ── Font sizes (rem) ───────────────────────────────────────────────────────
export const fontSize = {
  '2xs': '0.625rem',  //  10px
  xs:    '0.75rem',   //  12px
  sm:    '0.875rem',  //  14px
  base:  '1rem',      //  16px
  md:    '1.125rem',  //  18px
  lg:    '1.25rem',   //  20px
  xl:    '1.5rem',    //  24px
  '2xl': '1.875rem',  //  30px
  '3xl': '2.25rem',   //  36px
  '4xl': '3rem',      //  48px
  '5xl': '3.75rem',   //  60px
} as const;

// ── Font weights ───────────────────────────────────────────────────────────
export const fontWeight = {
  regular:   400,
  medium:    500,
  semibold:  600,
  bold:      700,
  extrabold: 800,
} as const;

// ── Line heights ───────────────────────────────────────────────────────────
export const lineHeight = {
  none:    1,
  tight:   1.25,
  snug:    1.375,
  normal:  1.5,
  relaxed: 1.625,
  loose:   1.75,
  prose:   1.8,  // legal document reading
} as const;

// ── Letter spacings ────────────────────────────────────────────────────────
export const letterSpacing = {
  tighter: '-0.05em',
  tight:   '-0.025em',
  normal:   '0em',
  wide:     '0.025em',
  wider:    '0.05em',
  widest:   '0.1em',
} as const;

// ── Semantic text roles ────────────────────────────────────────────────────
/** Map of UI role → token combination for consistent application across components */
export const textRole = {
  displayLarge: {
    fontFamily:    fontFamily.sans,
    fontSize:      'clamp(2rem, 5vw, 3.5rem)',
    fontWeight:    fontWeight.extrabold,
    lineHeight:    lineHeight.none,
    letterSpacing: letterSpacing.tighter,
  },
  displaySmall: {
    fontFamily:    fontFamily.sans,
    fontSize:      fontSize['3xl'],
    fontWeight:    fontWeight.bold,
    lineHeight:    lineHeight.tight,
    letterSpacing: letterSpacing.tight,
  },
  heading1: {
    fontFamily:    fontFamily.sans,
    fontSize:      fontSize['2xl'],
    fontWeight:    fontWeight.bold,
    lineHeight:    lineHeight.snug,
    letterSpacing: letterSpacing.tight,
  },
  heading2: {
    fontFamily:    fontFamily.sans,
    fontSize:      fontSize.xl,
    fontWeight:    fontWeight.semibold,
    lineHeight:    lineHeight.snug,
  },
  heading3: {
    fontFamily:    fontFamily.sans,
    fontSize:      fontSize.lg,
    fontWeight:    fontWeight.semibold,
    lineHeight:    lineHeight.normal,
  },
  body: {
    fontFamily: fontFamily.sans,
    fontSize:   fontSize.base,
    fontWeight: fontWeight.regular,
    lineHeight: lineHeight.normal,
  },
  bodySmall: {
    fontFamily: fontFamily.sans,
    fontSize:   fontSize.sm,
    fontWeight: fontWeight.regular,
    lineHeight: lineHeight.relaxed,
  },
  label: {
    fontFamily:    fontFamily.sans,
    fontSize:      fontSize.sm,
    fontWeight:    fontWeight.medium,
    lineHeight:    lineHeight.normal,
    letterSpacing: letterSpacing.wide,
  },
  caption: {
    fontFamily: fontFamily.sans,
    fontSize:   fontSize.xs,
    fontWeight: fontWeight.regular,
    lineHeight: lineHeight.normal,
  },
  legal: {
    fontFamily: fontFamily.serif,
    fontSize:   fontSize.base,
    fontWeight: fontWeight.regular,
    lineHeight: lineHeight.prose,
  },
  code: {
    fontFamily: fontFamily.mono,
    fontSize:   fontSize.sm,
    fontWeight: fontWeight.regular,
    lineHeight: lineHeight.relaxed,
  },
} as const;

export type TextRole = keyof typeof textRole;

export const typography = { fontFamily, fontSize, fontWeight, lineHeight, letterSpacing, textRole } as const;
