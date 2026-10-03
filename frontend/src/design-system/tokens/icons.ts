/**
 * Icon conventions for JurisPulse
 *
 * Icon library: lucide-react (already a project dependency)
 * All icons in the project must be imported from lucide-react.
 * Do not use SVG files directly unless a custom icon is unavoidable.
 *
 * Rules:
 *  1. Use the `size` prop rather than CSS width/height to set icon size.
 *  2. Never hard-code a color; pass `color` or rely on `currentColor`.
 *  3. Use `strokeWidth={1.75}` for regular icons (default 2 is too heavy).
 *  4. Wrap interactive icons in <button> or <IconButton> from the design system.
 *  5. Always provide an aria-label when an icon is the only child of an action.
 *
 * Standard sizes:
 *   xs  – 12px  (badge decorators, inline micro-icons)
 *   sm  – 14px  (compact list items, dense table cells)
 *   md  – 16px  (default – buttons, nav items, form adornments)
 *   lg  – 20px  (headings, empty-state illustrations)
 *   xl  – 24px  (hero / feature icons)
 *   2xl – 32px  (large empty states)
 *   3xl – 48px  (full-page empty states / onboarding)
 */

export const iconSize = {
  xs:    12,
  sm:    14,
  md:    16,
  lg:    20,
  xl:    24,
  '2xl': 32,
  '3xl': 48,
} as const;

export type IconSize = keyof typeof iconSize;

/** Default stroke width for all icons */
export const iconStrokeWidth = 1.75;

/**
 * Icon name map – canonical icon identifier per domain concept.
 * Update this map when replacing an icon so every usage is updated at once.
 */
export const iconName = {
  // ── Navigation ──────────────────────────────────────────────────────────
  dashboard:     'LayoutDashboard',
  cases:         'Briefcase',
  documents:     'FileText',
  hearings:      'Calendar',
  evidence:      'Microscope',
  research:      'Search',
  analytics:     'BarChart3',
  reports:       'ClipboardList',
  notifications: 'Bell',
  settings:      'Settings',
  profile:       'User',
  clients:       'Users',
  timeline:      'GitBranch',
  collaboration: 'Users2',
  logout:        'LogOut',

  // ── Actions ─────────────────────────────────────────────────────────────
  add:           'Plus',
  edit:          'Pencil',
  delete:        'Trash2',
  archive:       'Archive',
  download:      'Download',
  upload:        'Upload',
  share:         'Share2',
  copy:          'Copy',
  search:        'Search',
  filter:        'SlidersHorizontal',
  sort:          'ArrowUpDown',
  refresh:       'RefreshCw',
  close:         'X',
  confirm:       'Check',
  back:          'ArrowLeft',
  forward:       'ArrowRight',
  expand:        'ChevronDown',
  collapse:      'ChevronUp',
  moreHoriz:     'MoreHorizontal',
  moreVert:      'MoreVertical',
  externalLink:  'ExternalLink',

  // ── Status / feedback ────────────────────────────────────────────────────
  success:       'CheckCircle2',
  warning:       'AlertTriangle',
  error:         'XCircle',
  info:          'Info',
  loading:       'Loader2',
  verified:      'ShieldCheck',
  lock:          'Lock',
  unlock:        'Unlock',
  eye:           'Eye',
  eyeOff:        'EyeOff',

  // ── File types ───────────────────────────────────────────────────────────
  filePdf:       'FileText',
  fileDoc:       'FileText',
  fileImage:     'Image',
  fileAudio:     'Music',
  fileVideo:     'Video',
  fileZip:       'FileArchive',

  // ── AI / research ────────────────────────────────────────────────────────
  ai:            'Sparkles',
  brain:         'Brain',
  citation:      'Quote',
  verified_ai:   'ShieldCheck',
} as const;

export type IconNameKey = keyof typeof iconName;
export type IconNameValue = typeof iconName[IconNameKey];
