import React from 'react';
import { cn } from '@/lib/utils';
export interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}
export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(({ className, label, ...props }, ref) => (
  <label className="flex items-center gap-2 cursor-pointer">
    <input type="checkbox" ref={ref} className={cn("w-4 h-4 rounded border-border text-primary-500", className)} {...props} />
    {label && <span className="text-sm font-medium text-ink">{label}</span>}
  </label>
));
Checkbox.displayName = 'Checkbox';
