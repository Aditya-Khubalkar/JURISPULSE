/**\n * Form input primitives including Input, Select, and Textarea.\n */\nimport React from 'react';
import { cn } from '@/lib/utils';

// ── Input ─────────────────────────────────────────────────────────────────────

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
  leftElement?: React.ReactNode;
  rightElement?: React.ReactNode;
  fullWidth?: boolean;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, hint, leftElement, rightElement, fullWidth, className, id, ...props }, ref) => {
    const inputId = id ?? label?.toLowerCase().replace(/\s+/g, '-');

    return (
      <div className={cn('flex flex-col gap-1', fullWidth && 'w-full')}>
        {label && (
          <label
            htmlFor={inputId}
            className="text-sm font-medium text-ink"
          >
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <div className="relative flex items-center">
          {leftElement && (
            <div className="absolute left-3 flex items-center text-ink-secondary pointer-events-none">
              {leftElement}
            </div>
          )}
          <input
            ref={ref}
            id={inputId}
            className={cn(
              'w-full h-9 bg-surface-raised border rounded-[6px] px-3 text-sm text-ink',
              'placeholder:text-ink-muted transition-colors duration-150',
              'focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent',
              error
                ? 'border-red-400 focus:ring-red-400'
                : 'border-border hover:border-border-strong',
              leftElement && 'pl-9',
              rightElement && 'pr-9',
              className
            )}
            {...props}
          />
          {rightElement && (
            <div className="absolute right-3 flex items-center text-ink-secondary">
              {rightElement}
            </div>
          )}
        </div>
        {error && <p className="text-xs text-red-600">{error}</p>}
        {!error && hint && <p className="text-xs text-ink-secondary">{hint}</p>}
      </div>
    );
  }
);
Input.displayName = 'Input';

// ── Textarea ──────────────────────────────────────────────────────────────────

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  hint?: string;
  fullWidth?: boolean;
}

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, hint, fullWidth, className, id, ...props }, ref) => {
    const textareaId = id ?? label?.toLowerCase().replace(/\s+/g, '-');

    return (
      <div className={cn('flex flex-col gap-1', fullWidth && 'w-full')}>
        {label && (
          <label htmlFor={textareaId} className="text-sm font-medium text-ink">
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <textarea
          ref={ref}
          id={textareaId}
          className={cn(
            'w-full bg-surface-raised border rounded-[6px] px-3 py-2 text-sm text-ink',
            'placeholder:text-ink-muted transition-colors duration-150 resize-y min-h-[80px]',
            'focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent',
            error
              ? 'border-red-400 focus:ring-red-400'
              : 'border-border hover:border-border-strong',
            className
          )}
          {...props}
        />
        {error && <p className="text-xs text-red-600">{error}</p>}
        {!error && hint && <p className="text-xs text-ink-secondary">{hint}</p>}
      </div>
    );
  }
);
Textarea.displayName = 'Textarea';

// ── Select ────────────────────────────────────────────────────────────────────

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  hint?: string;
  options: { value: string; label: string; disabled?: boolean }[];
  placeholder?: string;
  fullWidth?: boolean;
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, hint, options, placeholder, fullWidth, className, id, ...props }, ref) => {
    const selectId = id ?? label?.toLowerCase().replace(/\s+/g, '-');

    return (
      <div className={cn('flex flex-col gap-1', fullWidth && 'w-full')}>
        {label && (
          <label htmlFor={selectId} className="text-sm font-medium text-ink">
            {label}
            {props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <select
          ref={ref}
          id={selectId}
          className={cn(
            'w-full h-9 bg-surface-raised border rounded-[6px] px-3 text-sm text-ink',
            'transition-colors duration-150 cursor-pointer appearance-none',
            'focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent',
            error
              ? 'border-red-400 focus:ring-red-400'
              : 'border-border hover:border-border-strong',
            !props.value && 'text-ink-muted',
            className
          )}
          style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2365736b' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E")`, backgroundRepeat: 'no-repeat', backgroundPosition: 'right 12px center', paddingRight: '32px' }}
          {...props}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((opt) => (
            <option key={opt.value} value={opt.value} disabled={opt.disabled}>
              {opt.label}
            </option>
          ))}
        </select>
        {error && <p className="text-xs text-red-600">{error}</p>}
        {!error && hint && <p className="text-xs text-ink-secondary">{hint}</p>}
      </div>
    );
  }
);
Select.displayName = 'Select';

// ── SearchInput ───────────────────────────────────────────────────────────────

export interface SearchInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  shortcut?: string;
  fullWidth?: boolean;
}

export function SearchInput({ shortcut, fullWidth, className, ...props }: SearchInputProps) {
  return (
    <div className={cn('relative flex items-center', fullWidth && 'w-full')}>
      <svg
        className="absolute left-3 w-4 h-4 text-ink-secondary pointer-events-none"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={2}
      >
        <circle cx="11" cy="11" r="8" />
        <path d="m21 21-4.35-4.35" />
      </svg>
      <input
        type="search"
        className={cn(
          'h-9 bg-surface-raised border border-border rounded-[6px] pl-9 pr-3 text-sm text-ink',
          'placeholder:text-ink-muted transition-colors duration-150',
          'focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent',
          'hover:border-border-strong',
          shortcut && 'pr-16',
          fullWidth && 'w-full',
          className
        )}
        {...props}
      />
      {shortcut && (
        <kbd className="absolute right-3 hidden sm:inline-flex items-center gap-0.5 px-1.5 py-0.5 text-[10px] text-ink-secondary bg-surface-overlay border border-border rounded font-mono">
          {shortcut}
        </kbd>
      )}
    </div>
  );
}
