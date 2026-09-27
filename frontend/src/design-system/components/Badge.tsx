import React from 'react';
import { cn } from '@/lib/utils';

// ── Badge ─────────────────────────────────────────────────────────────────────

export type BadgeVariant = 'default' | 'success' | 'warning' | 'danger' | 'info' | 'purple' | 'neutral';

export interface BadgeProps {
  variant?: BadgeVariant;
  size?: 'sm' | 'md';
  dot?: boolean;
  children: React.ReactNode;
  className?: string;
}

const badgeVariants: Record<BadgeVariant, string> = {
  default: 'bg-primary-100 text-primary-700 border-primary-200',
  success: 'bg-primary-100 text-primary-700 border-primary-200',
  warning: 'bg-amber-50 text-amber-700 border-amber-200',
  danger: 'bg-red-50 text-red-700 border-red-200',
  info: 'bg-blue-50 text-blue-700 border-blue-200',
  purple: 'bg-purple-50 text-purple-700 border-purple-200',
  neutral: 'bg-gray-50 text-gray-600 border-gray-200',
};

const dotColors: Record<BadgeVariant, string> = {
  default: 'bg-primary-400',
  success: 'bg-primary-400',
  warning: 'bg-amber-500',
  danger: 'bg-red-500',
  info: 'bg-blue-500',
  purple: 'bg-purple-500',
  neutral: 'bg-gray-400',
};

export function Badge({ variant = 'default', size = 'sm', dot = false, children, className }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 font-medium border rounded-full',
        size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-2.5 py-1 text-sm',
        badgeVariants[variant],
        className
      )}
    >
      {dot && (
        <span className={cn('w-1.5 h-1.5 rounded-full shrink-0', dotColors[variant])} />
      )}
      {children}
    </span>
  );
}

// ── StatusBadge ───────────────────────────────────────────────────────────────

export function StatusBadge({ status, className }: { status: string; className?: string }) {
  const config: Record<string, { variant: BadgeVariant; label: string }> = {
    // Case statuses
    active: { variant: 'success', label: 'Active' },
    pending: { variant: 'warning', label: 'Pending' },
    closed: { variant: 'neutral', label: 'Closed' },
    stayed: { variant: 'purple', label: 'Stayed' },
    disposed: { variant: 'info', label: 'Disposed' },
    appeal: { variant: 'warning', label: 'In Appeal' },
    // Document statuses
    uploaded: { variant: 'info', label: 'Uploaded' },
    processing: { variant: 'warning', label: 'Processing' },
    processed: { variant: 'success', label: 'Processed' },
    needs_review: { variant: 'warning', label: 'Needs Review' },
    verified: { variant: 'success', label: 'Verified' },
    failed: { variant: 'danger', label: 'Failed' },
    // Draft statuses
    draft: { variant: 'neutral', label: 'Draft' },
    generated: { variant: 'info', label: 'Generated' },
    reviewing: { variant: 'warning', label: 'Under Review' },
    approved: { variant: 'success', label: 'Approved' },
    rejected: { variant: 'danger', label: 'Rejected' },
    // Task statuses
    todo: { variant: 'neutral', label: 'To Do' },
    in_progress: { variant: 'info', label: 'In Progress' },
    waiting: { variant: 'warning', label: 'Waiting' },
    completed: { variant: 'success', label: 'Completed' },
    // Agent statuses
    running: { variant: 'info', label: 'Running' },
    queued: { variant: 'neutral', label: 'Queued' },
    // Hearing statuses
    scheduled: { variant: 'info', label: 'Scheduled' },
    adjourned: { variant: 'warning', label: 'Adjourned' },
    cancelled: { variant: 'danger', label: 'Cancelled' },
    // Model statuses
    available: { variant: 'success', label: 'Available' },
    unavailable: { variant: 'danger', label: 'Unavailable' },
    coming_soon: { variant: 'neutral', label: 'Coming Soon' },
    degraded: { variant: 'warning', label: 'Degraded' },
  };

  const cfg = config[status] ?? { variant: 'neutral' as BadgeVariant, label: status };
  return (
    <Badge variant={cfg.variant} dot className={className}>
      {cfg.label}
    </Badge>
  );
}

// ── PriorityBadge ─────────────────────────────────────────────────────────────

export function PriorityBadge({ priority, className }: { priority: string; className?: string }) {
  const config: Record<string, { variant: BadgeVariant; label: string }> = {
    critical: { variant: 'danger', label: 'Critical' },
    high: { variant: 'warning', label: 'High' },
    medium: { variant: 'info', label: 'Medium' },
    low: { variant: 'neutral', label: 'Low' },
  };
  const cfg = config[priority] ?? { variant: 'neutral' as BadgeVariant, label: priority };
  return <Badge variant={cfg.variant} className={className}>{cfg.label}</Badge>;
}

// ── ConfidenceBadge ───────────────────────────────────────────────────────────

export function ConfidenceBadge({ score, className }: { score: number; className?: string }) {
  const pct = Math.round(score * 100);
  const variant: BadgeVariant = score >= 0.75 ? 'success' : score >= 0.5 ? 'warning' : 'danger';
  return (
    <Badge variant={variant} className={className}>
      {pct}% confidence
    </Badge>
  );
}

// ── VerificationBadge ─────────────────────────────────────────────────────────

export function VerificationBadge({ status, className }: { status: string; className?: string }) {
  const config: Record<string, { variant: BadgeVariant; label: string }> = {
    verified: { variant: 'success', label: '✓ Verified' },
    partial: { variant: 'warning', label: '~ Partial' },
    unsupported: { variant: 'danger', label: '✗ Unsupported' },
    contradicted: { variant: 'danger', label: '⊗ Contradicted' },
    pending: { variant: 'neutral', label: '… Pending' },
  };
  const cfg = config[status] ?? { variant: 'neutral' as BadgeVariant, label: status };
  return <Badge variant={cfg.variant} className={className}>{cfg.label}</Badge>;
}

// ── AgentStatusBadge ──────────────────────────────────────────────────────────

export function AgentStatusBadge({ status, className }: { status: string; className?: string }) {
  const config: Record<string, { variant: BadgeVariant; label: string }> = {
    running: { variant: 'info', label: '⟳ Running' },
    completed: { variant: 'success', label: '✓ Completed' },
    queued: { variant: 'neutral', label: '… Queued' },
    waiting: { variant: 'warning', label: '⏸ Waiting' },
    failed: { variant: 'danger', label: '✗ Failed' },
    paused: { variant: 'purple', label: '⏸ Paused' },
  };
  const cfg = config[status] ?? { variant: 'neutral' as BadgeVariant, label: status };
  return <Badge variant={cfg.variant} className={className}>{cfg.label}</Badge>;
}
