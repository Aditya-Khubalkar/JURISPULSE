import React from 'react';
import { Card } from '@/design-system';
import { CitationBadge } from './CitationBadge';
export const ResearchResultCard: React.FC<{ result: any }> = ({ result }) => (
  <Card hoverable className="space-y-2">
    <div className="flex items-center gap-2"><CitationBadge citation={result.citation} /><span className="text-xs text-ink-muted">{result.court}</span></div>
    <h3 className="font-bold text-ink">{result.title}</h3>
    <p className="text-xs text-ink-secondary">{result.summary}</p>
  </Card>
);
