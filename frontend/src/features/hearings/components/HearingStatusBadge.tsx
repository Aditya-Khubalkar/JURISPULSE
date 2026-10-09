import React from 'react';
import { HearingStatus } from '../types';
export const HearingStatusBadge: React.FC<{ status: HearingStatus }> = ({ status }) => (
  <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-50 text-blue-700 capitalize">
    {status.replace('_', ' ')}
  </span>
);
