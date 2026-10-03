/**
 * ThemeProvider for JurisPulse
 *
 * Manages the active colour theme ('light' | 'dark') and persists the
 * user's preference in localStorage.  Applies the .dark class to <html>
 * so all CSS variables switch via the dark-theme.css overrides.
 *
 * Usage:
 *   import { useTheme } from '@/app/providers/ThemeProvider';
 *   const { theme, toggleTheme } = useTheme();
 */

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  type ReactNode,
} from 'react';
import { lightTheme, darkTheme, type Theme } from '@/design-system/tokens/theme';

// ── Types ──────────────────────────────────────────────────────────────────
type ThemeMode = 'light' | 'dark';

interface ThemeContextValue {
  mode:        ThemeMode;
  theme:       Theme;
  toggleTheme: () => void;
  setTheme:    (mode: ThemeMode) => void;
}

// ── Context ────────────────────────────────────────────────────────────────
const ThemeContext = createContext<ThemeContextValue | null>(null);

// ── Helpers ────────────────────────────────────────────────────────────────
const STORAGE_KEY = 'jurispulse-theme';

function getInitialMode(): ThemeMode {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'light' || stored === 'dark') return stored;
  } catch {
    // localStorage unavailable (SSR or private mode)
  }
  return window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light';
}

function applyThemeClass(mode: ThemeMode): void {
  const root = document.documentElement;
  if (mode === 'dark') {
    root.classList.add('dark');
    root.classList.remove('light');
  } else {
    root.classList.add('light');
    root.classList.remove('dark');
  }
}

// ── Provider ───────────────────────────────────────────────────────────────
interface ThemeProviderProps {
  children: ReactNode;
  /** Override the initial mode (useful for testing) */
  defaultMode?: ThemeMode;
}

export function ThemeProvider({ children, defaultMode }: ThemeProviderProps) {
  const [mode, setModeState] = useState<ThemeMode>(
    defaultMode ?? getInitialMode
  );

  // Apply the class whenever mode changes
  useEffect(() => {
    applyThemeClass(mode);
    try {
      localStorage.setItem(STORAGE_KEY, mode);
    } catch {
      // ignore write failures
    }
  }, [mode]);

  const setTheme = useCallback((next: ThemeMode) => {
    setModeState(next);
  }, []);

  const toggleTheme = useCallback(() => {
    setModeState(prev => (prev === 'light' ? 'dark' : 'light'));
  }, []);

  const theme = mode === 'dark' ? darkTheme : lightTheme;

  return (
    <ThemeContext.Provider value={{ mode, theme, toggleTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// ── Hook ───────────────────────────────────────────────────────────────────
export function useTheme(): ThemeContextValue {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return ctx;
}
