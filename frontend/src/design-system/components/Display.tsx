/**
 * Display components including Card, Alert, and Skeleton.
 */
import React from 'react';
import { cn } from '@/lib/utils';

// ── Card ──────────────────────────────────────────────────────────────────────

export interface CardProps {
  children: React.ReactNode;
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hoverable?: boolean;
  clickable?: boolean;
  onClick?: () => void;
}

const cardPadding = { none: '', sm: 'p-3', md: 'p-4 sm:p-5', lg: 'p-6' };

export function Card({ children, className, padding = 'md', hoverable, clickable, onClick }: CardProps) {
  const Tag = clickable || onClick ? 'button' : 'div';
  return (
    <Tag
      onClick={onClick}
      className={cn(
        'bg-surface-raised rounded-[12px] border border-border shadow-sm',
        cardPadding[padding],
        (hoverable || clickable || onClick) && 'hover:shadow-md hover:border-border-strong transition-all duration-150',
        (clickable || onClick) && 'cursor-pointer text-left w-full',
        className
      )}
    >
      {children}
    </Tag>
  );
}

// ── StatCard ──────────────────────────────────────────────────────────────────

export interface StatCardProps {
  label: string;
  value: string | number;
  icon?: React.ReactNode;
  change?: number;
  changeLabel?: string;
  colorClass?: string;
  onClick?: () => void;
  className?: string;
}

export function StatCard({ label, value, icon, change, changeLabel, colorClass, onClick, className }: StatCardProps) {
  const isPositive = change !== undefined && change >= 0;
  return (
    <Card
      className={className}
      hoverable={!!onClick}
      clickable={!!onClick}
      onClick={onClick}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm text-ink-secondary font-medium">{label}</p>
          <p className="text-2xl font-bold text-ink mt-1">{value}</p>
          {change !== undefined && (
            <p className={cn('text-xs mt-1', isPositive ? 'text-primary-700' : 'text-red-600')}>
              {isPositive ? '↑' : '↓'} {Math.abs(change)}% {changeLabel}
            </p>
          )}
        </div>
        {icon && (
          <div className={cn('w-10 h-10 rounded-[8px] flex items-center justify-center', colorClass ?? 'bg-primary-100 text-primary-700')}>
            {icon}
          </div>
        )}
      </div>
    </Card>
  );
}

// ── Skeleton ──────────────────────────────────────────────────────────────────

export function Skeleton({ className }: { className?: string }) {
  return <div className={cn('skeleton rounded-[6px]', className)} />;
}

export function SkeletonCard({ lines = 3 }: { lines?: number }) {
  return (
    <Card>
      <Skeleton className="h-4 w-1/3 mb-4" />
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton key={i} className={cn('h-3 mb-2', i === lines - 1 ? 'w-2/3' : 'w-full')} />
      ))}
    </Card>
  );
}

export function SkeletonText({ lines = 3, className }: { lines?: number; className?: string }) {
  return (
    <div className={className}>
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton key={i} className={cn('h-3 mb-2', i === lines - 1 ? 'w-2/3' : 'w-full')} />
      ))}
    </div>
  );
}

// ── EmptyState ────────────────────────────────────────────────────────────────

export interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}

export function EmptyState({ icon, title, description, action, className }: EmptyStateProps) {
  return (
    <div className={cn('flex flex-col items-center justify-center py-16 px-6 text-center', className)}>
      {icon && (
        <div className="w-16 h-16 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 mb-4">
          {icon}
        </div>
      )}
      <h3 className="text-base font-semibold text-ink mb-1">{title}</h3>
      {description && <p className="text-sm text-ink-secondary max-w-sm">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}

// ── ErrorState ────────────────────────────────────────────────────────────────

export interface ErrorStateProps {
  title?: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}

export function ErrorState({
  title = 'Something went wrong',
  description = 'An error occurred while loading this content. Please try again.',
  action,
  className,
}: ErrorStateProps) {
  return (
    <div className={cn('flex flex-col items-center justify-center py-16 px-6 text-center', className)}>
      <div className="w-16 h-16 rounded-full bg-red-50 flex items-center justify-center text-red-500 mb-4">
        <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
        </svg>
      </div>
      <h3 className="text-base font-semibold text-ink mb-1">{title}</h3>
      <p className="text-sm text-ink-secondary max-w-sm">{description}</p>
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}

// ── Alert ─────────────────────────────────────────────────────────────────────

export interface AlertProps {
  variant?: 'info' | 'success' | 'warning' | 'danger';
  title?: string;
  children: React.ReactNode;
  className?: string;
  onDismiss?: () => void;
}

const alertStyles = {
  info: 'bg-blue-50 border-blue-200 text-blue-800',
  success: 'bg-primary-100 border-primary-200 text-primary-700',
  warning: 'bg-amber-50 border-amber-200 text-amber-800',
  danger: 'bg-red-50 border-red-200 text-red-800',
};

export function Alert({ variant = 'info', title, children, className, onDismiss }: AlertProps) {
  return (
    <div className={cn('flex gap-3 px-4 py-3 rounded-[8px] border text-sm', alertStyles[variant], className)}>
      <div className="flex-1">
        {title && <p className="font-semibold mb-0.5">{title}</p>}
        <div>{children}</div>
      </div>
      {onDismiss && (
        <button
          onClick={onDismiss}
          aria-label="Dismiss"
          className="shrink-0 opacity-70 hover:opacity-100"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </div>
  );
}

// ── ProgressBar ───────────────────────────────────────────────────────────────

export function ProgressBar({
  value,
  max = 100,
  label,
  showValue,
  colorClass,
  className,
}: {
  value: number;
  max?: number;
  label?: string;
  showValue?: boolean;
  colorClass?: string;
  className?: string;
}) {
  const pct = Math.min(100, (value / max) * 100);
  return (
    <div className={className}>
      {(label || showValue) && (
        <div className="flex justify-between items-center mb-1">
          {label && <span className="text-xs text-ink-secondary">{label}</span>}
          {showValue && <span className="text-xs font-medium text-ink">{Math.round(pct)}%</span>}
        </div>
      )}
      <div className="h-1.5 bg-primary-100 rounded-full overflow-hidden">
        <div
          className={cn('h-full rounded-full transition-all duration-500', colorClass ?? 'bg-primary-400')}
          style={{ width: `${pct}%` }}
          role="progressbar"
          aria-valuenow={value}
          aria-valuemax={max}
        />
      </div>
    </div>
  );
}

// ── Tabs ──────────────────────────────────────────────────────────────────────

export interface TabItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
  badge?: number;
  disabled?: boolean;
}

export interface TabsProps {
  tabs: TabItem[];
  activeTab: string;
  onChange: (id: string) => void;
  className?: string;
  variant?: 'underline' | 'pills';
}

export function Tabs({ tabs, activeTab, onChange, className, variant = 'underline' }: TabsProps) {
  if (variant === 'pills') {
    return (
      <div className={cn('flex gap-1 p-1 bg-surface-overlay rounded-[8px]', className)} role="tablist">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            aria-selected={activeTab === tab.id}
            disabled={tab.disabled}
            onClick={() => onChange(tab.id)}
            className={cn(
              'flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium rounded-[6px] transition-all duration-150',
              activeTab === tab.id
                ? 'bg-surface-raised text-ink shadow-sm'
                : 'text-ink-secondary hover:text-ink',
              tab.disabled && 'opacity-50 cursor-not-allowed'
            )}
          >
            {tab.icon && <span className="w-4 h-4">{tab.icon}</span>}
            {tab.label}
            {tab.badge !== undefined && (
              <span className="ml-0.5 px-1.5 py-0.5 text-[10px] font-bold bg-primary-100 text-primary-700 rounded-full">
                {tab.badge}
              </span>
            )}
          </button>
        ))}
      </div>
    );
  }

  return (
    <div
      className={cn('flex border-b border-border overflow-x-auto', className)}
      role="tablist"
    >
      {tabs.map((tab) => (
        <button
          key={tab.id}
          role="tab"
          aria-selected={activeTab === tab.id}
          disabled={tab.disabled}
          onClick={() => onChange(tab.id)}
          className={cn(
            'flex items-center gap-1.5 px-4 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors duration-150 whitespace-nowrap',
            activeTab === tab.id
              ? 'border-primary-400 text-primary-700'
              : 'border-transparent text-ink-secondary hover:text-ink hover:border-border-strong',
            tab.disabled && 'opacity-50 cursor-not-allowed'
          )}
        >
          {tab.icon && <span>{tab.icon}</span>}
          {tab.label}
          {tab.badge !== undefined && (
            <span className="ml-1 px-1.5 py-0.5 text-[10px] font-bold bg-primary-100 text-primary-700 rounded-full">
              {tab.badge}
            </span>
          )}
        </button>
      ))}
    </div>
  );
}

// ── Breadcrumb ────────────────────────────────────────────────────────────────

export interface BreadcrumbItem {
  label: string;
  href?: string;
  onClick?: () => void;
}

export function Breadcrumb({ items, className }: { items: BreadcrumbItem[]; className?: string }) {
  return (
    <nav aria-label="Breadcrumb" className={cn('flex items-center gap-1.5 text-sm', className)}>
      {items.map((item, i) => (
        <React.Fragment key={i}>
          {i > 0 && <span className="text-ink-muted">/</span>}
          {i < items.length - 1 ? (
            <button
              onClick={item.onClick}
              className="text-ink-secondary hover:text-ink transition-colors"
            >
              {item.label}
            </button>
          ) : (
            <span className="text-ink font-medium">{item.label}</span>
          )}
        </React.Fragment>
      ))}
    </nav>
  );
}

// ── Divider ───────────────────────────────────────────────────────────────────

export function Divider({ className, label }: { className?: string; label?: string }) {
  if (label) {
    return (
      <div className={cn('flex items-center gap-3 my-4', className)}>
        <div className="flex-1 h-px bg-border" />
        <span className="text-xs text-ink-secondary font-medium">{label}</span>
        <div className="flex-1 h-px bg-border" />
      </div>
    );
  }
  return <hr className={cn('border-border my-4', className)} />;
}
