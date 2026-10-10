import React from 'react';
import { Card } from '@/design-system';
export const CaseTrendsChart: React.FC = () => (
  <Card className="space-y-2">
    <h3 className="font-bold text-sm text-ink">Disposal vs Institution Velocity</h3>
    <div className="h-24 flex items-end justify-around gap-2 pt-2 border-b">
      {['Jun', 'Jul', 'Aug', 'Sep', 'Oct'].map(m => (
        <div key={m} className="w-8 bg-primary-600 rounded-t h-16 text-[10px] text-center text-white">{m}</div>
      ))}
    </div>
  </Card>
);
