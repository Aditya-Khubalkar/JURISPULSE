/**\n * Avatar component for user display.\n */\nimport React from 'react';
import { cn, getInitials } from '@/lib/utils';

// ── Avatar ────────────────────────────────────────────────────────────────────

const AVATAR_COLORS = [
  'bg-primary-100 text-primary-700',
  'bg-blue-50 text-blue-700',
  'bg-purple-50 text-purple-700',
  'bg-amber-50 text-amber-700',
  'bg-orange-50 text-orange-700',
  'bg-teal-50 text-teal-700',
];

function getAvatarColor(name: string): string {
  const idx = name.charCodeAt(0) % AVATAR_COLORS.length;
  return AVATAR_COLORS[idx];
}

export type AvatarSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

export interface AvatarProps {
  name: string;
  src?: string;
  size?: AvatarSize;
  className?: string;
}

const sizeCls: Record<AvatarSize, string> = {
  xs: 'w-6 h-6 text-[10px]',
  sm: 'w-8 h-8 text-xs',
  md: 'w-10 h-10 text-sm',
  lg: 'w-12 h-12 text-base',
  xl: 'w-16 h-16 text-lg',
};

export function Avatar({ name, src, size = 'md', className }: AvatarProps) {
  const initials = getInitials(name);
  const colorCls = getAvatarColor(name);

  return (
    <div
      className={cn(
        'rounded-full inline-flex items-center justify-center font-semibold shrink-0 overflow-hidden',
        sizeCls[size],
        !src && colorCls,
        className
      )}
      title={name}
      aria-label={name}
    >
      {src ? (
        <img src={src} alt={name} className="w-full h-full object-cover" />
      ) : (
        initials
      )}
    </div>
  );
}

// ── AvatarGroup ───────────────────────────────────────────────────────────────

export interface AvatarGroupProps {
  avatars: { name: string; src?: string }[];
  max?: number;
  size?: AvatarSize;
  className?: string;
}

export function AvatarGroup({ avatars, max = 3, size = 'sm', className }: AvatarGroupProps) {
  const visible = avatars.slice(0, max);
  const overflow = avatars.length - max;

  return (
    <div className={cn('flex -space-x-2', className)}>
      {visible.map((a, i) => (
        <Avatar
          key={i}
          name={a.name}
          src={a.src}
          size={size}
          className="ring-2 ring-white"
        />
      ))}
      {overflow > 0 && (
        <div
          className={cn(
            'rounded-full inline-flex items-center justify-center font-semibold ring-2 ring-white',
            'bg-border text-ink-secondary text-xs',
            sizeCls[size]
          )}
        >
          +{overflow}
        </div>
      )}
    </div>
  );
}
