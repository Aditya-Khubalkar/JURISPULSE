import React from 'react';
import { Card } from '@/design-system';
export const NotificationList: React.FC<{ items: any[] }> = ({ items }) => (
  <div className="space-y-2">{items.map(it => <Card key={it.id}>{it.title}</Card>)}</div>
);
