/**
 * Spacing design tokens for JurisPulse
 *
 * Base unit: 4 px (0.25 rem).
 * Scale steps follow a 4-pt grid – every value is a multiple of 4 px.
 * Use these constants instead of arbitrary pixel values in component styles.
 */

// ── Numeric scale (rem values) ─────────────────────────────────────────────
export const space = {
  0:    '0',
  px:   '1px',     // 1 px – hairline borders
  0.5:  '0.125rem', //  2 px
  1:    '0.25rem',  //  4 px
  1.5:  '0.375rem', //  6 px
  2:    '0.5rem',   //  8 px
  2.5:  '0.625rem', // 10 px
  3:    '0.75rem',  // 12 px
  3.5:  '0.875rem', // 14 px
  4:    '1rem',     // 16 px
  5:    '1.25rem',  // 20 px
  6:    '1.5rem',   // 24 px
  7:    '1.75rem',  // 28 px
  8:    '2rem',     // 32 px
  9:    '2.25rem',  // 36 px
  10:   '2.5rem',   // 40 px
  11:   '2.75rem',  // 44 px
  12:   '3rem',     // 48 px
  14:   '3.5rem',   // 56 px
  16:   '4rem',     // 64 px
  20:   '5rem',     // 80 px
  24:   '6rem',     // 96 px
  32:   '8rem',     // 128 px
  40:   '10rem',    // 160 px
  48:   '12rem',    // 192 px
  56:   '14rem',    // 224 px
  64:   '16rem',    // 256 px
} as const;

// ── Named semantic roles ───────────────────────────────────────────────────
/** Component-level padding for common interactive elements */
export const componentPadding = {
  buttonSm:    `${space[1.5]} ${space[3]}`,  // 6 × 12
  buttonMd:    `${space[2]}   ${space[4]}`,  // 8 × 16
  buttonLg:    `${space[3]}   ${space[6]}`,  // 12 × 24
  inputSm:     `${space[1.5]} ${space[3]}`,
  inputMd:     `${space[2]}   ${space[3.5]}`,
  inputLg:     `${space[3]}   ${space[4]}`,
  cardSm:      space[3],   // 12 px
  cardMd:      space[4],   // 16 px
  cardLg:      space[6],   // 24 px
  cardXl:      space[8],   // 32 px
} as const;

/** Layout-level gaps and gutters */
export const layout = {
  gutter:       space[6],   // 24 px – page horizontal padding
  gutterMobile: space[4],   // 16 px – mobile page padding
  sectionGap:   space[12],  // 48 px – between major page sections
  stackGap:     space[4],   // 16 px – default flex/grid gap
  inlineGap:    space[2],   // 8  px – icon + label gap
  navHeight:    '3.5rem',   // 56 px – top nav bar
  sidebarWidth: '15rem',    // 240 px – expanded sidebar
  sidebarMin:   '4rem',     // 64 px  – collapsed sidebar
} as const;

export type SpaceKey = keyof typeof space;

export const spacing = { space, componentPadding, layout } as const;
