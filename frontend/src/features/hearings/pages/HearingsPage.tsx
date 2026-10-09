import React, { useState, useEffect } from 'react';
import { Breadcrumb } from '@/design-system';
import { HearingList } from '../components/HearingList';
import { HearingDetailCard } from '../components/HearingDetailCard';
import { hearingsApi } from '@/services/api/hearingsApi';

export const HearingsPage: React.FC = () => {
  const [hearings, setHearings] = useState<any[]>([]);
  const [selected, setSelected] = useState<any>(null);
  useEffect(() => { hearingsApi.getHearings().then(setHearings); }, []);
  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <Breadcrumb items={[{ label: 'Workspace' }, { label: 'Hearings' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">Cause List & Hearings</h1>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2"><HearingList hearings={hearings} onSelectHearing={setSelected} /></div>
        <div>{selected && <HearingDetailCard hearing={selected} onClose={() => setSelected(null)} />}</div>
      </div>
    </div>
  );
};
