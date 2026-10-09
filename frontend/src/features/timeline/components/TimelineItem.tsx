import React from 'react';
import { Card } from '@/design-system';
export const TimelineItem: React.FC<{ event: any }> = ({ event }) => (
  <Card>
    <div className="text-xs text-ink-muted">{event.date} · {event.category}</div>
    <h4 className="font-bold text-sm text-ink">{event.title}</h4>
    <p className="text-xs text-ink-secondary mt-0.5">{event.description}</p>
  </Card>
);
