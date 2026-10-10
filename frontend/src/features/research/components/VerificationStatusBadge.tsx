import React from 'react';
export const VerificationStatusBadge: React.FC<{ confidence: number }> = ({ confidence }) => (
  <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 text-xs font-medium">Verified {Math.round(confidence * 100)}%</span>
);
