import React from 'react';
export const TimelineFilter: React.FC<{ selected: string; onChange: (c: string) => void }> = ({ selected, onChange }) => (
  <div className="flex gap-2">
    {['all', 'hearing', 'order', 'filing'].map(c => (
      <button key={c} onClick={() => onChange(c)} className={`px-3 py-1 text-xs rounded capitalize ${selected === c ? 'bg-primary-600 text-white' : 'bg-neutral-100'}`}>
        {c}
      </button>
    ))}
  </div>
);
