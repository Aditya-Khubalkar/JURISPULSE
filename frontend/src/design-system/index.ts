// Design System Public API
// Import from '@/design-system' to use any component

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
