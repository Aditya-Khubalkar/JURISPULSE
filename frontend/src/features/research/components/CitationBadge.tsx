import React from 'react';
export const CitationBadge: React.FC<{ citation: string }> = ({ citation }) => (
  <span className="px-2 py-0.5 rounded bg-primary-50 text-primary-700 text-xs font-mono font-medium">{citation}</span>
);
