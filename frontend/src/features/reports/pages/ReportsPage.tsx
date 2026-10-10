import React from 'react';
import { Breadcrumb, Card } from '@/design-system';
export const ReportsPage: React.FC = () => (
  <div className="space-y-6 max-w-5xl mx-auto">
    <div><Breadcrumb items={[{ label: 'Workspace' }, { label: 'Reports' }]} /><h1 className="text-2xl font-bold text-ink mt-1">Court Reports</h1></div>
    <Card className="p-4">Monthly Cause List Roster Export</Card>
  </div>
);
