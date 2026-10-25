/**
 * Primary UI Button component for user interactions.
 */
import React from 'react';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

// ── Button ────────────────────────────────────────────────────────────────────

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'outline' | 'warning';
export type ButtonSize = 'xs' | 'sm' | 'md' | 'lg';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

const buttonVariants: Record<ButtonVariant, string> = {
  primary: 'bg-primary-500 hover:bg-primary-600 text-white font-semibold shadow-xs hover:shadow-sm border border-primary-600/30 transition-all',
  secondary: 'bg-surface-raised hover:bg-surface-overlay text-ink border border-border shadow-xs hover:border-border-strong transition-all',
  ghost: 'bg-transparent hover:bg-surface-overlay text-ink border border-transparent transition-all',
  outline: 'bg-transparent hover:bg-surface-overlay text-primary-600 dark:text-primary-400 border border-primary-500/40 transition-all',
  danger: 'bg-rose-600 hover:bg-rose-700 text-white font-semibold border border-transparent shadow-xs transition-all',
  warning: 'bg-amber-600 hover:bg-amber-700 text-white font-semibold border border-transparent shadow-xs transition-all',
};

const buttonSizes: Record<ButtonSize, string> = {
  xs: 'h-6 px-2 text-xs rounded-[4px]',
  sm: 'h-8 px-3 text-sm rounded-[6px]',
  md: 'h-9 px-4 text-sm rounded-[6px]',
  lg: 'h-11 px-6 text-base rounded-[8px]',
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      loading = false,
      leftIcon,
      rightIcon,
      fullWidth,
      children,
      className,
      disabled,
      ...props
    },
    ref
  ) => {
    const isDisabled = disabled || loading;
    return (
      <button
        ref={ref}
        disabled={isDisabled}
        className={cn(
          'inline-flex items-center justify-center gap-2',
          'font-medium transition-all duration-150 cursor-pointer',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-400 focus-visible:ring-offset-2',
          'disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none',
          buttonVariants[variant],
          buttonSizes[size],
          fullWidth && 'w-full',
          className
        )}
        {...props}
      >
        {loading ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : leftIcon ? (
          <span className="shrink-0">{leftIcon}</span>
        ) : null}
        {children}
        {rightIcon && !loading && (
          <span className="shrink-0">{rightIcon}</span>
        )}
      </button>
    );
  }
);
Button.displayName = 'Button';

// ── IconButton ────────────────────────────────────────────────────────────────

export interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  label: string;
}

export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ variant = 'ghost', size = 'md', loading, label, children, className, disabled, ...props }, ref) => {
    const sizeMap: Record<ButtonSize, string> = {
      xs: 'h-6 w-6 rounded-[4px]',
      sm: 'h-8 w-8 rounded-[6px]',
      md: 'h-9 w-9 rounded-[6px]',
      lg: 'h-11 w-11 rounded-[8px]',
    };
    return (
      <button
        ref={ref}
        aria-label={label}
        title={label}
        disabled={disabled || loading}
        className={cn(
          'inline-flex items-center justify-center',
          'font-medium transition-all duration-150 cursor-pointer',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-400 focus-visible:ring-offset-2',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          buttonVariants[variant],
          sizeMap[size],
          className
        )}
        {...props}
      >
        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : children}
      </button>
    );
  }
);
IconButton.displayName = 'IconButton';
