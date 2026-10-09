import React from 'react';
export const ActivityFeed: React.FC<{ items: any[] }> = ({ items }) => (
  <div className="space-y-2">{items.map((it, idx) => <div key={idx} className="text-xs"><strong>{it.user}</strong>: {it.action}</div>)}</div>
);
