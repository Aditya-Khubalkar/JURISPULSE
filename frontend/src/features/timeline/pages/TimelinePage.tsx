import React, { useState } from 'react';
import { Breadcrumb } from '@/design-system';
import { TimelineItem } from '../components/TimelineItem';
import { TimelineFilter } from '../components/TimelineFilter';
import { mockTimelineEvents } from '@/services/api/mockData';

export const TimelinePage: React.FC = () => {
  const [filter, setFilter] = useState('all');
  const events = (mockTimelineEvents as any[]).filter(e => filter === 'all' || e.category === filter);
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <Breadcrumb items={[{ label: 'Workspace' }, { label: 'Timeline' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">Case Chronology</h1>
      </div>
      <TimelineFilter selected={filter} onChange={setFilter} />
      <div className="border-l-2 border-primary-200 pl-6 space-y-4">
        {events.map((e, idx) => <TimelineItem key={e.id || idx} event={e} />)}
      </div>
    </div>
  );
};
