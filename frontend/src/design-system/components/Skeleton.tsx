import React from 'react';
export const Skeleton: React.FC<{ className?: string }> = ({ className = 'h-4 w-full' }) => (
  <div className={`animate-pulse bg-neutral-200 rounded ${className}`} />
);
