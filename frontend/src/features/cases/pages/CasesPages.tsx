/**
 * Cases list view with search and filters.
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, Filter, SortAsc, Eye, Briefcase, ChevronRight } from 'lucide-react';
import {
  Card, StatusBadge, PriorityBadge, Badge, EmptyState,
  Breadcrumb, Button, Avatar,
} from '@/design-system';
import { formatDate, formatHearingDate, truncate } from '@/lib/utils';
import { ROUTES, CASE_TYPE_LABELS } from '@/constants';
import { mockCases } from '@/services/api/mockData';
import type { CaseStatus, CasePriority } from '@/types';

// ── Filters ───────────────────────────────────────────────────────────────────

const STATUS_OPTIONS = [
  { value: '', label: 'All Statuses' },
  { value: 'active', label: 'Active' },
  { value: 'pending', label: 'Pending' },
  { value: 'closed', label: 'Closed' },
  { value: 'stayed', label: 'Stayed' },
  { value: 'disposed', label: 'Disposed' },
];

const PRIORITY_OPTIONS = [
  { value: '', label: 'All Priorities' },
  { value: 'critical', label: 'Critical' },
  { value: 'high', label: 'High' },
  { value: 'medium', label: 'Medium' },
  { value: 'low', label: 'Low' },
];

// ── Cases List Page ───────────────────────────────────────────────────────────

export function CasesListPage() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');

  const filtered = mockCases.filter((c) => {
    const matchSearch =
      !search ||
      c.title.toLowerCase().includes(search.toLowerCase()) ||
      c.caseNumber.toLowerCase().includes(search.toLowerCase()) ||
      c.clientName.toLowerCase().includes(search.toLowerCase());
    const matchStatus = !statusFilter || c.status === statusFilter;
    const matchPriority = !priorityFilter || c.priority === priorityFilter;
    return matchSearch && matchStatus && matchPriority;
  });

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <Breadcrumb items={[{ label: 'Workspace' }, { label: 'Cases' }]} />
          <h1 className="text-2xl font-bold text-ink mt-1">Cases</h1>
          <p className="text-sm text-ink-secondary">{mockCases.length} total cases</p>
        </div>
        <Button
          variant="primary"
          leftIcon={<Plus className="w-4 h-4" />}
          onClick={() => navigate(ROUTES.CASE_NEW)}
        >
          New Case
        </Button>
      </div>

      {/* Filters */}
      <Card padding="sm">
        <div className="flex flex-wrap gap-3">
          <div className="flex-1 min-w-[200px] relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-secondary pointer-events-none" />
            <input
              type="search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search cases, case numbers, clients..."
              className="w-full h-9 pl-9 pr-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="h-9 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
            aria-label="Filter by status"
          >
            {STATUS_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="h-9 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
            aria-label="Filter by priority"
          >
            {PRIORITY_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
          {(statusFilter || priorityFilter || search) && (
            <button
              onClick={() => { setSearch(''); setStatusFilter(''); setPriorityFilter(''); }}
              className="text-sm text-ink-secondary hover:text-ink px-2"
            >
              Clear filters
            </button>
          )}
        </div>
      </Card>

      {/* Cases Table */}
      <Card padding="none">
        {filtered.length === 0 ? (
          <EmptyState
            icon={<Briefcase className="w-6 h-6" />}
            title="No cases found"
            description="Try adjusting your search or filters."
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm" role="table" aria-label="Cases list">
              <thead>
                <tr className="border-b border-border bg-surface">
                  {['Case', 'Client', 'Court / Type', 'Status', 'Priority', 'Next Hearing', 'Updated', ''].map((col) => (
                    <th
                      key={col}
                      className="px-4 py-3 text-left text-xs font-semibold text-ink-secondary uppercase tracking-wider whitespace-nowrap"
                    >
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filtered.map((c, i) => (
                  <tr
                    key={c.id}
                    className="border-b border-surface-overlay hover:bg-primary-50 transition-colors cursor-pointer"
                    onClick={() => navigate(ROUTES.CASE_DETAIL(c.id))}
                    role="row"
                    tabIndex={0}
                    onKeyDown={(e) => e.key === 'Enter' && navigate(ROUTES.CASE_DETAIL(c.id))}
                  >
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2.5">
                        <div className="w-8 h-8 rounded-[6px] bg-primary-100 flex items-center justify-center shrink-0">
                          <Briefcase className="w-3.5 h-3.5 text-primary-700" />
                        </div>
                        <div>
                          <p className="font-medium text-ink">{truncate(c.title, 40)}</p>
                          <p className="text-xs text-ink-secondary">{c.caseNumber}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-ink">{c.clientName}</td>
                    <td className="px-4 py-3">
                      <p className="text-ink">{truncate(c.court, 30)}</p>
                      <p className="text-xs text-ink-secondary">{CASE_TYPE_LABELS[c.caseType] ?? c.caseType}</p>
                    </td>
                    <td className="px-4 py-3"><StatusBadge status={c.status} /></td>
                    <td className="px-4 py-3"><PriorityBadge priority={c.priority} /></td>
                    <td className="px-4 py-3 text-ink-secondary">
                      {c.nextHearing ? formatHearingDate(c.nextHearing) : '—'}
                    </td>
                    <td className="px-4 py-3 text-ink-secondary">{formatDate(c.updatedAt)}</td>
                    <td className="px-4 py-3">
                      <ChevronRight className="w-4 h-4 text-ink-muted" />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      {/* Pagination placeholder */}
      <div className="flex items-center justify-between text-sm text-ink-secondary">
        <span>Showing {filtered.length} of {mockCases.length} cases</span>
      </div>
    </div>
  );
}

// ── Case New Page ─────────────────────────────────────────────────────────────

export function CaseNewPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await new Promise((r) => setTimeout(r, 1000));
    setLoading(false);
    navigate(ROUTES.CASES);
  };

  return (
    <div className="max-w-2xl">
      <Breadcrumb
        items={[
          { label: 'Cases', onClick: () => navigate(ROUTES.CASES) },
          { label: 'New Case' },
        ]}
        className="mb-4"
      />
      <h1 className="text-2xl font-bold text-ink mb-6">New Case</h1>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2">
              <label htmlFor="case-title" className="block text-sm font-medium text-ink mb-1">Case Title <span className="text-red-500">*</span></label>
              <input id="case-title" type="text" required
                className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                placeholder="e.g. Ramesh Kumar vs. Union of India" />
            </div>
            <div>
              <label htmlFor="case-number" className="block text-sm font-medium text-ink mb-1">Case Number</label>
              <input id="case-number" type="text"
                className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                placeholder="e.g. WP(C)/2024/00345" />
            </div>
            <div>
              <label htmlFor="case-type" className="block text-sm font-medium text-ink mb-1">Case Type <span className="text-red-500">*</span></label>
              <select id="case-type" required
                className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent">
                <option value="">Select type</option>
                {Object.entries(CASE_TYPE_LABELS).map(([v, l]) => (
                  <option key={v} value={v}>{l}</option>
                ))}
              </select>
            </div>
            <div className="col-span-2">
              <label htmlFor="case-court" className="block text-sm font-medium text-ink mb-1">Court <span className="text-red-500">*</span></label>
              <input id="case-court" type="text" required list="courts-list"
                className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                placeholder="Delhi High Court" />
            </div>
            <div>
              <label htmlFor="case-priority" className="block text-sm font-medium text-ink mb-1">Priority</label>
              <select id="case-priority"
                className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent">
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
                <option value="low">Low</option>
              </select>
            </div>
            <div>
              <label htmlFor="case-filing-date" className="block text-sm font-medium text-ink mb-1">Filing Date</label>
              <input id="case-filing-date" type="date"
                className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent" />
            </div>
            <div className="col-span-2">
              <label htmlFor="case-client" className="block text-sm font-medium text-ink mb-1">Client Name <span className="text-red-500">*</span></label>
              <input id="case-client" type="text" required
                className="w-full h-9 px-3 text-sm border border-border rounded-[6px] focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                placeholder="Client name or organization" />
            </div>
            <div className="col-span-2">
              <label htmlFor="case-description" className="block text-sm font-medium text-ink mb-1">Description</label>
              <textarea id="case-description" rows={3}
                className="w-full px-3 py-2 text-sm border border-border rounded-[6px] resize-none focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
                placeholder="Brief description of the case..." />
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-2">
            <Button variant="secondary" onClick={() => navigate(ROUTES.CASES)}>
              Cancel
            </Button>
            <Button type="submit" loading={loading}>
              Create Case
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}

// Add case card or row

// Add case search

// Add case filters

// Add case sorting

// Add case pagination

// Validate cases navigation
