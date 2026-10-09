import React from 'react';
import { Button } from '@/design-system';
export const ClientDetailModal: React.FC<{ client: any; onClose: () => void }> = ({ client, onClose }) => (
  <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4">
    <div className="bg-surface rounded-xl p-5 max-w-sm w-full space-y-3">
      <h3 className="font-bold text-ink">{client.name}</h3>
      <p className="text-xs text-ink-secondary">{client.email}</p>
      <div className="flex justify-end"><Button variant="primary" size="sm" onClick={onClose}>Close</Button></div>
    </div>
  </div>
);
