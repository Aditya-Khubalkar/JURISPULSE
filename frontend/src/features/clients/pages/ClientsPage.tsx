import React, { useState } from 'react';
import { Breadcrumb, Card, Avatar } from '@/design-system';
import { mockClients } from '@/services/api/mockData';
import { ClientDetailModal } from '../components/ClientDetailModal';

export const ClientsPage: React.FC = () => {
  const [selected, setSelected] = useState<any>(null);
  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <Breadcrumb items={[{ label: 'Directory' }, { label: 'Clients' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">Client Management</h1>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {mockClients.map(c => (
          <Card key={c.id} hoverable onClick={() => setSelected(c)} className="cursor-pointer">
            <div className="flex items-center gap-3">
              <Avatar name={c.name} size="md" />
              <div>
                <h4 className="font-bold text-sm text-ink">{c.name}</h4>
                <p className="text-xs text-ink-secondary">{c.company || 'Private Retainer'}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
      {selected && <ClientDetailModal client={selected} onClose={() => setSelected(null)} />}
    </div>
  );
};
