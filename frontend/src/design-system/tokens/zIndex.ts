/**
 * Z-index design tokens for JurisPulse
 *
 * Defines explicit layering so components don't accidentally overlap.
 * All z-index values in the project must reference this map.
 *
 * Layer order (lowest → highest):
 *   base → sticky → dropdown → overlay → modal → toast → tooltip → dev
 */

export const zIndex = {
  // ── Page-level layers ────────────────────────────────────────────────
  /** Normal document flow */
  base:       0,
  /** Slightly raised elements, e.g. cards on hover */
  raised:     1,
  /** Sticky sidebar column or row headers */
  sticky:    10,
  /** Top navigation bar */
  nav:       20,
  /** Floating action button */
  fab:       30,

  // ── Interactive layers ───────────────────────────────────────────────
  /** Dropdown menus, command palettes, date pickers */
  dropdown:  100,
  /** Popover and rich tooltip panels */
  popover:   110,

  // ── Overlay layers ───────────────────────────────────────────────────
  /** Drawer/sheet side panels */
  drawer:    200,
  /** Modal backdrop */
  backdrop:  300,
  /** Modal dialog content */
  modal:     310,

  // ── Notification layers ──────────────────────────────────────────────
  /** Toast / snackbar notifications */
  toast:     400,
  /** Inline tooltips shown on hover */
  tooltip:   410,

  // ── Debug / dev layer ────────────────────────────────────────────────
  /** Dev overlay – never ship with a value this high in production UI */
  dev:       9999,
} as const;

export type ZIndexKey = keyof typeof zIndex;
