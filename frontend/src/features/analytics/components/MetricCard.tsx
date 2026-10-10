import React from 'react';
import { Card } from '@/design-system';
export const MetricCard: React.FC<{ metric: any }> = ({ metric }) => (
  <Card className="space-y-1"><span className="text-xs text-ink-muted">{metric.title}</span><div className="text-xl font-bold text-ink">{metric.value}</div></Card>
);
