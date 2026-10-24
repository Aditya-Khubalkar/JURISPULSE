import React from 'react';
import { FolderOpen } from 'lucide-react';

export const EmptyState: React.FC<{ title: string; description?: string }> = ({ title, description }) => (
  <div className="flex flex-col items-center justify-center p-8 text-center text-neutral-500">
    <FolderOpen className="w-12 h-12 mb-3 text-neutral-400 stroke-[1.5]" />
    <h4 className="font-semibold text-neutral-700 text-sm">{title}</h4>
    {description && <p className="text-xs text-neutral-400 mt-1 max-w-sm">{description}</p>}
  </div>
);
