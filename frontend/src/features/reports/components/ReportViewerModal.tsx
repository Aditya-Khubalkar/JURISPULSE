import React from 'react';
export const ReportViewerModal: React.FC<{ onClose: () => void }> = ({ onClose }) => (
  <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4">
    <div className="bg-surface p-6 rounded-lg max-w-lg w-full">Report Content</div>
  </div>
);
