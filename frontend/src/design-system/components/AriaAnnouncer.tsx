import React from 'react';
export const AriaAnnouncer: React.FC<{ message: string; politeness?: 'polite' | 'assertive' }> = ({
  message,
  politeness = 'polite'
}) => (
  <div role="status" aria-live={politeness} className="sr-only">
    {message}
  </div>
);
