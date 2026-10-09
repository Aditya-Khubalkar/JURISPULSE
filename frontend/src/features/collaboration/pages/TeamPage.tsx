import React from 'react';
import { Breadcrumb, Card, Avatar } from '@/design-system';
import { mockTeamMembers } from '@/services/api/mockData';
export const TeamPage: React.FC = () => (
  <div className="space-y-6 max-w-5xl mx-auto">
    <div>
      <Breadcrumb items={[{ label: 'Firm' }, { label: 'Team' }]} />
      <h1 className="text-2xl font-bold text-ink mt-1">Legal Team</h1>
    </div>
    <div className="grid grid-cols-2 gap-4">
      {mockTeamMembers.map(m => (
        <Card key={m.id} className="flex items-center gap-3">
          <Avatar name={m.name} size="md" />
          <div><h4 className="font-bold text-sm text-ink">{m.name}</h4><p className="text-xs text-ink-secondary">{m.role}</p></div>
        </Card>
      ))}
    </div>
  </div>
);
