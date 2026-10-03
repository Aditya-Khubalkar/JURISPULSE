/**
 * Animation and transition design tokens for JurisPulse
 *
 * Consistent motion makes the UI feel polished and predictable.
 * Durations follow a linear scale; easings match Material Design 3 conventions.
 *
 * Rules:
 *  - Micro-interactions (hover, focus): use 'fast' duration.
 *  - Element enter/exit (fade, slide):  use 'base' or 'slow'.
 *  - Layout shifts (sidebar, panels):   use 'slow' or 'slower'.
 *  - Never animate layout-triggering properties (width, height) when
 *    transform/opacity achieve the same visual result.
 */

// ── Durations ──────────────────────────────────────────────────────────────
export const duration = {
  instant:  '0ms',
  fast:     '100ms',
  base:     '150ms',
  slow:     '200ms',
  slower:   '300ms',
  sluggish: '500ms',
} as const;

// ── Easings ────────────────────────────────────────────────────────────────
export const easing = {
  /** Standard – for elements that stay on screen */
  standard:       'cubic-bezier(0.4, 0, 0.2, 1)',
  /** Decelerate – for elements entering the screen */
  decelerate:     'cubic-bezier(0, 0, 0.2, 1)',
  /** Accelerate – for elements leaving the screen */
  accelerate:     'cubic-bezier(0.4, 0, 1, 1)',
  /** Emphasized – for expressive, prominent transitions */
  emphasized:     'cubic-bezier(0.2, 0, 0, 1)',
  /** Linear – for continuous animations (spinners, progress) */
  linear:         'linear',
  /** Spring-like bounce for playful micro-interactions */
  spring:         'cubic-bezier(0.34, 1.56, 0.64, 1)',
} as const;

// ── Pre-composed transition strings ───────────────────────────────────────
export const transition = {
  /** All properties – avoid using for performance-sensitive components */
  all:     `all ${duration.base} ${easing.standard}`,
  /** Opacity + transform – GPU-composited, safest to animate */
  fade:    `opacity ${duration.base} ${easing.standard}`,
  move:    `transform ${duration.slow} ${easing.decelerate}`,
  fadeMove:`opacity ${duration.slow} ${easing.decelerate}, transform ${duration.slow} ${easing.decelerate}`,
  /** Colors, borders, backgrounds */
  color:   `color ${duration.fast} ${easing.standard}, background-color ${duration.fast} ${easing.standard}, border-color ${duration.fast} ${easing.standard}`,
  /** Shadow for hover lift effect */
  shadow:  `box-shadow ${duration.base} ${easing.standard}`,
  /** Sidebar collapse/expand */
  sidebar: `width ${duration.slower} ${easing.standard}, opacity ${duration.slow} ${easing.standard}`,
} as const;

// ── Keyframe animation names (matches globals.css @keyframes) ──────────────
export const keyframe = {
  skeletonShimmer: 'skeleton-shimmer',
  pageIn:          'page-in',
  toastIn:         'toast-in',
  toastOut:        'toast-out',
  spin:            'spin',
  pulse:           'pulse',
  fadeIn:          'fade-in',
  slideUp:         'slide-up',
  slideDown:       'slide-down',
} as const;

export type DurationKey  = keyof typeof duration;
export type EasingKey    = keyof typeof easing;
export type TransitionKey= keyof typeof transition;

export const animation = { duration, easing, transition, keyframe } as const;
