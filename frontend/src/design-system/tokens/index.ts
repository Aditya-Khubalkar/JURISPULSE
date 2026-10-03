/**
 * Design token barrel export for JurisPulse
 *
 * Import tokens from '@/design-system/tokens' to access the full token set.
 * Each sub-module is also directly importable for tree-shaking.
 */

export * from './colors';
export * from './typography';
export * from './spacing';
export * from './radius';
export * from './shadows';
export * from './zIndex';
export * from './animation';
export * from './breakpoints';
export * from './icons';
export * from './theme';

// Convenience re-exports for common access patterns
export { colors }     from './colors';
export { typography } from './typography';
export { spacing }    from './spacing';
export { radii }      from './radius';
export { shadows }    from './shadows';
export { animation }  from './animation';
export { breakpoints }from './breakpoints';
export { lightTheme, darkTheme } from './theme';
