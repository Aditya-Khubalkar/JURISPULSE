import React from 'react';
import { Hearing } from '../types';
import { Card } from '@/design-system';
import { Calendar, MapPin } from 'lucide-react';
import { HearingStatusBadge } from './HearingStatusBadge';

export const HearingList: React.FC<{ hearings: Hearing[]; onSelectHearing?: (h: Hearing) => void }> = ({ hearings, onSelectHearing }) => (
  <div className="space-y-3">
    {hearings.map((h) => (
      <Card key={h.id} hoverable onClick={() => onSelectHearing?.(h)} className="cursor-pointer">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="font-mono text-xs text-primary-600 font-bold">{h.caseNumber}</span>
              <HearingStatusBadge status={h.status} />
            </div>
            <h3 className="font-semibold text-ink text-sm">{h.caseTitle}</h3>
            <p className="text-xs text-ink-secondary">{h.purpose}</p>
          </div>
          <div className="text-xs text-ink-muted text-right">
            <div>{h.date} at {h.time}</div>
            <div>{h.courtName} ({h.courtroom})</div>
          </div>
        </div>
      </Card>
    ))}
  </div>
);
