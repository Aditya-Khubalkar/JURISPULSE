import React from 'react';
export function Table({ className, ...props }: React.HTMLAttributes<HTMLTableElement>) {
  return <div className="w-full overflow-auto"><table className="w-full text-sm" {...props} /></div>;
}
