import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { Button } from '@/design-system';
export const ResearchSearchInput: React.FC<{ onSearch: (q: string) => void }> = ({ onSearch }) => {
  const [q, setQ] = useState('');
  return (
    <form onSubmit={(e) => { e.preventDefault(); onSearch(q); }} className="relative">
      <Search className="w-5 h-5 absolute left-3 top-3 text-primary-500" />
      <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search caselaw, citations, legal propositions..." className="w-full pl-10 pr-24 py-2.5 border rounded-lg" />
      <div className="absolute right-2 top-1.5"><Button type="submit" variant="primary" size="sm">Search</Button></div>
    </form>
  );
};
