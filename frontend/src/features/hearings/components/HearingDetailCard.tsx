import React from 'react';
import { Hearing } from '../types';
import { Card, Button } from '@/design-system';

export const HearingDetailCard: React.FC<{ hearing: Hearing; onClose?: () => void }> = ({ hearing, onClose }) => (
  <Card className="space-y-3">
    <div className="flex justify-between items-start">
      <div>
        <span className="font-mono text-xs text-primary-600">{hearing.caseNumber}</span>
        <h2 className="text-base font-bold text-ink">{hearing.caseTitle}</h2>
      </div>
      {onClose && <Button variant="ghost" size="sm" onClick={onClose}>Close</Button>}
    </div>
    <div className="text-xs text-ink-secondary space-y-1">
      <div>Court: {hearing.courtName} - {hearing.courtroom}</div>
      <div>Bench: {hearing.judgeName}</div>
      <div>Purpose: {hearing.purpose}</div>
    </div>
  </Card>
);
