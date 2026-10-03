/**
 * Theme configuration for JurisPulse
 *
 * Defines the structure of a theme object that components consume via
 * React context.  Both light and dark themes satisfy the Theme interface.
 *
 * Usage:
 *   import { lightTheme, darkTheme, type Theme } from '@/design-system/tokens/theme';
 */

import { colors, surfaceDark, inkDark, borderDark, type StatusKey } from './colors';
import { typography } from './typography';
import { spacing }    from './spacing';
import { radii }      from './radius';
import { shadows }    from './shadows';
import { zIndex }     from './zIndex';
import { animation }  from './animation';

// ── Theme interface ────────────────────────────────────────────────────────
export interface ThemeColors {
  primary:  typeof colors.primary;
  accent:   typeof colors.accent;
  warning:  typeof colors.warning;
  danger:   typeof colors.danger;
  surface: {
    default:  string;
    raised:   string;
    overlay:  string;
  };
  ink: {
    default:   string;
    secondary: string;
    muted:     string;
    disabled:  string;
  };
  border: {
    default: string;
    strong:  string;
  };
  status: typeof colors.status;
}

export interface Theme {
  name:       'light' | 'dark';
  colors:     ThemeColors;
  typography: typeof typography;
  spacing:    typeof spacing;
  radii:      typeof radii;
  shadows:    typeof shadows;
  zIndex:     typeof zIndex;
  animation:  typeof animation;
}

// ── Shared token slices ────────────────────────────────────────────────────
const sharedTokens = { typography, spacing, radii, shadows, zIndex, animation } as const;
const sharedPalette = {
  primary: colors.primary,
  accent:  colors.accent,
  warning: colors.warning,
  danger:  colors.danger,
  status:  colors.status,
} as const;

// ── Light theme ────────────────────────────────────────────────────────────
export const lightTheme: Theme = {
  name: 'light',
  colors: {
    ...sharedPalette,
    surface: { ...colors.surface },
    ink:     { ...colors.ink },
    border:  { ...colors.border },
  },
  ...sharedTokens,
};

// ── Dark theme ─────────────────────────────────────────────────────────────
export const darkTheme: Theme = {
  name: 'dark',
  colors: {
    ...sharedPalette,
    surface: { ...surfaceDark },
    ink:     { ...inkDark },
    border:  { ...borderDark },
  },
  ...sharedTokens,
};

export type { StatusKey };
