import React from 'react';
export const HearingCalendarBadge: React.FC<{ date: string }> = ({ date }) => (
  <div className="w-12 h-12 rounded bg-neutral-100 flex flex-col items-center justify-center border text-xs font-bold text-ink">
    <span>{date}</span>
  </div>
);
