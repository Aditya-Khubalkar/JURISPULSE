# JurisPulse Design System

The design system lives in `frontend/src/design-system/` and provides
tokens, primitives, and components for the entire frontend.

## Directory layout

```
design-system/
├── tokens/           Design tokens (TypeScript constants)
│   ├── colors.ts     Color palette and semantic tokens
│   ├── typography.ts Font families, scale, weights, roles
│   ├── spacing.ts    4-pt spacing scale and semantic shortcuts
│   ├── radius.ts     Border-radius scale and component map
│   ├── shadows.ts    Elevation shadows, focus rings
│   ├── zIndex.ts     Layer stack (dropdown → modal → toast)
│   ├── animation.ts  Durations, easings, transition strings
│   ├── breakpoints.ts Responsive breakpoints, media queries
│   ├── icons.ts      Icon size scale and canonical icon names
│   ├── theme.ts      Light and dark Theme objects (composed)
│   └── index.ts      Barrel export for all tokens
└── components/       React components built on the tokens
    ├── Button.tsx
    ├── Badge.tsx
    ├── Avatar.tsx
    ├── Inputs.tsx
    ├── Overlay.tsx
    └── Display.tsx
```

## CSS files

```
styles/
├── globals.css     @theme block – all CSS custom properties
├── dark-theme.css  .dark overrides + prefers-color-scheme fallback
├── base.css        Box-model reset, element defaults
├── forms.css       Form field primitives (.input-base, .field-label …)
├── surfaces.css    Card, panel, divider, status-badge primitives
├── typography.css  Text utility classes (.text-h1 … .prose-legal)
├── motion.css      Keyframes, .animate-* classes, skeleton, transitions
└── breakpoints.css Container, grid, flex, gap, show/hide utilities
```

Import order in `main.tsx`:

```ts
import './styles/globals.css';
import './styles/dark-theme.css';
import './styles/base.css';
import './styles/forms.css';
import './styles/surfaces.css';
import './styles/typography.css';
import './styles/motion.css';
import './styles/breakpoints.css';
```

## Token usage

Always import tokens through the design-system alias:

```ts
import { colors, spacing, iconSize } from '@/design-system';
```

Or directly from the sub-module for tree-shaking:

```ts
import { primary } from '@/design-system/tokens/colors';
```

## Color palette

| Alias | Role | Light value |
|-------|------|-------------|
| `--color-primary-700` | Brand / key actions | `#1f6b45` |
| `--color-primary-500` | Hover / interactive | `#5cbc38` |
| `--color-accent-500`  | Highlights          | `#edb53a` |
| `--color-danger-500`  | Errors / delete     | `#d4502f` |
| `--color-surface`     | Page background     | `#f8faf7` |
| `--color-surface-raised` | Cards           | `#ffffff`  |
| `--color-ink`         | Primary text        | `#18231d` |
| `--color-ink-secondary` | Secondary text   | `#65736b` |
| `--color-border`      | Dividers            | `#dde7df` |

## Typography

| Class | Usage |
|-------|-------|
| `.text-display-lg` | Hero headings |
| `.text-h1` – `.text-h4` | Section headings |
| `.text-body` / `.text-body-sm` | Paragraph text |
| `.text-label` | Form labels, nav items |
| `.text-label-xs` | Section headers, overlines |
| `.text-caption` | Metadata, timestamps |
| `.text-legal` | Legal document serif body |
| `.prose-legal` | Full document reading blocks |

## Status colors

| Key | Text | Background |
|-----|------|------------|
| `active`    | `#1f6b45` | `#e9f8e5` |
| `pending`   | `#b45309` | `#fef3c7` |
| `closed`    | `#65736b` | `#f0f5ef` |
| `urgent`    | `#d4502f` | `#fde8e3` |
| `draft`     | `#6366f1` | `#eef2ff` |
| `verified`  | `#1f6b45` | `#e9f8e5` |
| `reviewing` | `#92400e` | `#fef3c7` |
| `failed`    | `#d4502f` | `#fde8e3` |

## Icon conventions

- Library: `lucide-react`
- Default size: `md` (16 px) with `strokeWidth={1.75}`
- Use `iconName` map from `@/design-system/tokens/icons` to get the
  canonical icon identifier for a domain concept.

## Theming

The active theme is applied via the `.dark` class on `<html>`.
The `ThemeContext` (in `src/app/providers/ThemeProvider.tsx`) exposes
`theme` and `toggleTheme`.  Components read CSS variables directly;
the TypeScript theme objects are available for runtime colour access.

## Adding new tokens

1. Add the constant to the relevant `tokens/*.ts` file.
2. Add the matching CSS custom property to `styles/globals.css` (`@theme`).
3. Add a dark-mode override in `styles/dark-theme.css` if the token is semantic.
4. Re-export the new type/constant from `tokens/index.ts` if needed.
