/**\n * Design system component exports.\n */\n// Design System Public API
// Import from '@/design-system' to use any component or token

// ── Tokens ──────────────────────────────────────────────────────────────────
export * from './tokens';
export type { Theme, ThemeColors, StatusKey } from './tokens/theme';
export type { StatusKey as ColorStatusKey }   from './tokens/colors';
export type { TextRole }                       from './tokens/typography';
export type { SpaceKey }                       from './tokens/spacing';
export type { RadiusKey, ComponentRadiusKey } from './tokens/radius';
export type { ShadowKey }                      from './tokens/shadows';
export type { ZIndexKey }                      from './tokens/zIndex';
export type { DurationKey, EasingKey }        from './tokens/animation';
export type { BreakpointKey }                  from './tokens/breakpoints';
export type { IconSize, IconNameKey }          from './tokens/icons';


export { Button, IconButton } from './components/Button';
export type { ButtonProps, ButtonVariant, ButtonSize } from './components/Button';

export {
  Badge,
  StatusBadge,
  PriorityBadge,
  ConfidenceBadge,
  VerificationBadge,
  AgentStatusBadge,
} from './components/Badge';
export type { BadgeProps, BadgeVariant } from './components/Badge';

export { Avatar, AvatarGroup } from './components/Avatar';
export type { AvatarProps, AvatarGroupProps, AvatarSize } from './components/Avatar';

export { Input, Textarea, Select, SearchInput } from './components/Inputs';
export type { InputProps, TextareaProps, SelectProps, SearchInputProps } from './components/Inputs';

export { Modal, ConfirmDialog, Drawer } from './components/Overlay';
export type { ModalProps, ConfirmDialogProps, DrawerProps } from './components/Overlay';

export {
  Card,
  StatCard,
  Skeleton,
  SkeletonCard,
  SkeletonText,
  EmptyState,
  ErrorState,
  Alert,
  ProgressBar,
  Tabs,
  Breadcrumb,
  Divider,
} from './components/Display';
export type {
  CardProps,
  StatCardProps,
  EmptyStateProps,
  ErrorStateProps,
  AlertProps,
  TabItem,
  TabsProps,
  BreadcrumbItem,
} from './components/Display';
