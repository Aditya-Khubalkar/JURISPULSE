import React from 'react';
import { useNavigate } from 'react-router-dom';
import { CheckSquare, Calendar, Clock, Scale, Users, UserCheck, MessageSquare, FileBarChart, ShieldCheck, Construction } from 'lucide-react';
import { Card, EmptyState, Breadcrumb, StatCard, StatusBadge, PriorityBadge, Badge } from '@/design-system';
import { Button } from '@/design-system';
import { Avatar } from '@/design-system';
import { mockTasks, mockHearings, mockTimelineEvents, mockClients, mockTeamMembers, mockNotifications } from '@/services/api/mockData';
import { formatDate, formatHearingDate } from '@/lib/utils';
import { ROUTES } from '@/constants';

// ── Placeholder shell ─────────────────────────────────────────────────────────

function ComingSoon({ icon, title, description }: { icon?: React.ReactNode; title: string; description?: string }) {
  return (
    <div className="flex items-center justify-center h-60">
      <div className="text-center">
        <div className="w-14 h-14 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 mx-auto mb-4">
          {icon ?? <Construction className="w-6 h-6" />}
        </div>
        <h2 className="text-base font-semibold text-ink mb-1">{title}</h2>
        <p className="text-sm text-ink-secondary">{description ?? 'This module is under active development.'}</p>
      </div>
    </div>
  );
}

// ── Tasks Page ────────────────────────────────────────────────────────────────

export function TasksPage() {
  const pending = mockTasks.filter((t) => t.status !== 'completed');
  const completed = mockTasks.filter((t) => t.status === 'completed');

  return (
    <div className="space-y-5 max-w-3xl">
      <div className="flex items-center justify-between">
        <div>
          <Breadcrumb items={[{ label: 'Workspace' }, { label: 'Tasks' }]} />
          <h1 className="text-2xl font-bold text-ink mt-1">Tasks</h1>
          <p className="text-sm text-ink-secondary">{pending.length} pending · {completed.length} completed</p>
        </div>
        <Button variant="primary" leftIcon={<CheckSquare className="w-4 h-4" />} size="sm">
          Add Task
        </Button>
      </div>

      <div className="space-y-2">
        {mockTasks.map((t) => (
          <Card key={t.id} hoverable>
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                defaultChecked={t.status === 'completed'}
                className="w-4 h-4 rounded border-border accent-primary-400 shrink-0"
                aria-label={`Toggle task: ${t.title}`}
              />
              <div className="flex-1 min-w-0">
                <p className={`font-medium ${t.status === 'completed' ? 'line-through text-ink-muted' : 'text-ink'}`}>
                  {t.title}
                </p>
                <div className="flex items-center gap-2 mt-0.5">
                  {t.caseName && <span className="text-xs text-ink-secondary">{t.caseName}</span>}
                  {t.dueDate && (
                    <span className={`text-xs ${new Date(t.dueDate) < new Date() && t.status !== 'completed' ? 'text-red-500 font-medium' : 'text-ink-muted'}`}>
                      Due: {formatDate(t.dueDate)}
                    </span>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <Avatar name={t.assigneeName} size="xs" />
                <PriorityBadge priority={t.priority} />
                <StatusBadge status={t.status} />
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// ── Hearings Page ─────────────────────────────────────────────────────────────

export function HearingsPage() {
  const upcoming = mockHearings.filter((h) => h.status === 'scheduled').sort(
    (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
  );
  const past = mockHearings.filter((h) => h.status !== 'scheduled');

  return (
    <div className="space-y-5 max-w-3xl">
      <div>
        <Breadcrumb items={[{ label: 'Workspace' }, { label: 'Hearings' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">Hearings</h1>
      </div>

      <h2 className="font-semibold text-ink">Upcoming ({upcoming.length})</h2>
      <div className="space-y-3">
        {upcoming.map((h) => (
          <Card key={h.id} hoverable>
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-[8px] bg-primary-100 flex flex-col items-center justify-center shrink-0">
                <span className="text-[10px] font-bold text-primary-700 uppercase">{formatDate(h.date, 'MMM')}</span>
                <span className="text-lg font-bold text-primary-700 leading-none">{formatDate(h.date, 'd')}</span>
              </div>
              <div className="flex-1">
                <p className="font-semibold text-ink">{h.caseName}</p>
                <p className="text-sm text-ink-secondary">{h.court}</p>
                <div className="flex items-center gap-2 mt-1 flex-wrap">
                  <Badge variant="info" size="sm">{h.purpose}</Badge>
                  <span className="text-xs text-ink-muted">{h.time}</span>
                  {h.judge && <span className="text-xs text-ink-secondary">Before: {h.judge}</span>}
                </div>
              </div>
              <StatusBadge status={h.status} />
            </div>
          </Card>
        ))}
      </div>

      <h2 className="font-semibold text-ink pt-2">Past Hearings ({past.length})</h2>
      <div className="space-y-2">
        {past.map((h) => (
          <Card key={h.id} className="opacity-70">
            <div className="flex items-center gap-3">
              <div className="text-center text-xs shrink-0 w-10">
                <div className="font-bold text-primary-700">{formatDate(h.date, 'd MMM')}</div>
                <div className="text-ink-muted">{formatDate(h.date, 'yyyy')}</div>
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-ink">{h.caseName}</p>
                {h.outcome && <p className="text-xs text-ink-secondary mt-0.5">{h.outcome}</p>}
              </div>
              <StatusBadge status={h.status} />
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// ── Clients Page ──────────────────────────────────────────────────────────────

export function ClientsPage() {
  return (
    <div className="space-y-5">
      <div>
        <Breadcrumb items={[{ label: 'Collaboration' }, { label: 'Clients' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">Clients</h1>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockClients.map((c) => (
          <Card key={c.id} hoverable>
            <div className="flex items-start gap-3">
              <Avatar name={c.name} size="md" />
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-ink">{c.name}</p>
                {c.organization && <p className="text-xs text-ink-secondary">{c.organization}</p>}
                <p className="text-xs text-ink-secondary mt-0.5">{c.email}</p>
                {c.activeCases !== undefined && (
                  <Badge variant="success" size="sm" className="mt-1.5">
                    {c.activeCases} active case{c.activeCases !== 1 ? 's' : ''}
                  </Badge>
                )}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// ── Team Page ─────────────────────────────────────────────────────────────────

export function TeamPage() {
  return (
    <div className="space-y-5">
      <div>
        <Breadcrumb items={[{ label: 'Collaboration' }, { label: 'Team' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">Team</h1>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockTeamMembers.map((m) => (
          <Card key={m.id} hoverable>
            <div className="flex items-start gap-3">
              <Avatar name={m.name} size="md" />
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-ink">{m.name}</p>
                <p className="text-xs text-ink-secondary capitalize">{m.role} · {m.specialization}</p>
                <p className="text-xs text-ink-secondary mt-0.5">{m.email}</p>
                {m.barCouncilId && (
                  <p className="text-xs text-ink-muted mt-0.5">Bar: {m.barCouncilId}</p>
                )}
                {m.caseCount !== undefined && (
                  <Badge variant="neutral" size="sm" className="mt-1.5">{m.caseCount} cases</Badge>
                )}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// ── Notifications Page ────────────────────────────────────────────────────────

export function NotificationsPage() {
  return (
    <div className="space-y-5 max-w-2xl">
      <div>
        <Breadcrumb items={[{ label: 'Notifications' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">Notifications</h1>
      </div>
      <div className="space-y-2">
        {mockNotifications.map((n) => (
          <Card key={n.id} className={!n.isRead ? 'border-primary-200 bg-primary-50' : ''}>
            <div className="flex items-start gap-3">
              <div className="flex-1">
                <p className="font-medium text-ink text-sm">{n.title}</p>
                <p className="text-xs text-ink-secondary mt-0.5">{n.message}</p>
                <p className="text-xs text-ink-muted mt-1">{formatDate(n.createdAt)}</p>
              </div>
              {!n.isRead && <div className="w-2 h-2 bg-primary-400 rounded-full mt-1.5 shrink-0" />}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// ── Placeholder Pages ─────────────────────────────────────────────────────────

export function EvidencePage() {
  return (
    <div className="space-y-4">
      <Breadcrumb items={[{ label: 'Workspace' }, { label: 'Evidence' }]} />
      <h1 className="text-2xl font-bold text-ink">Evidence</h1>
      <ComingSoon icon={<Scale className="w-6 h-6" />} title="Evidence Management" description="Evidence chain of custody, authentication, and classification coming soon." />
    </div>
  );
}

export function TimelinePage() {
  return (
    <div className="space-y-4">
      <Breadcrumb items={[{ label: 'Workspace' }, { label: 'Timeline' }]} />
      <h1 className="text-2xl font-bold text-ink">Timeline</h1>
      <div className="relative max-w-2xl">
        <div className="absolute left-4 top-0 bottom-0 w-px bg-border" />
        <div className="space-y-3 ml-10">
          {mockTimelineEvents.map((ev) => (
            <div key={ev.id} className="relative">
              <div className="absolute -left-9 w-3 h-3 rounded-full bg-primary-400 border-2 border-white mt-0.5" style={{ left: '-2.2rem' }} />
              <Card>
                <div className="flex items-start justify-between">
                  <div>
                    <Badge variant="neutral" size="sm" className="mb-1">{ev.type}</Badge>
                    <p className="font-medium text-ink text-sm">{ev.title}</p>
                    {ev.description && <p className="text-xs text-ink-secondary">{ev.description}</p>}
                  </div>
                  <span className="text-xs text-ink-muted ml-2 shrink-0">{formatDate(ev.date)}</span>
                </div>
              </Card>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export function CalendarPage() {
  return (
    <div className="space-y-4">
      <Breadcrumb items={[{ label: 'Workspace' }, { label: 'Calendar' }]} />
      <h1 className="text-2xl font-bold text-ink">Calendar</h1>
      <ComingSoon icon={<Calendar className="w-6 h-6" />} title="Calendar View" description="Monthly and weekly calendar view of hearings, deadlines, and tasks coming soon." />
    </div>
  );
}

export function CollaborationPage() {
  return (
    <div className="space-y-4">
      <Breadcrumb items={[{ label: 'Collaboration' }, { label: 'Comments' }]} />
      <h1 className="text-2xl font-bold text-ink">Collaboration</h1>
      <ComingSoon icon={<MessageSquare className="w-6 h-6" />} title="Team Collaboration" description="Comments, mentions, and shared workspaces coming soon." />
    </div>
  );
}

export function ReportsPage() {
  return (
    <div className="space-y-4">
      <Breadcrumb items={[{ label: 'Insights' }, { label: 'Reports' }]} />
      <h1 className="text-2xl font-bold text-ink">Reports</h1>
      <ComingSoon icon={<FileBarChart className="w-6 h-6" />} title="Reports" description="Automated case outcome, billing, and court appearance reports coming soon." />
    </div>
  );
}

export function AdminPage() {
  return (
    <div className="space-y-4">
      <Breadcrumb items={[{ label: 'Administration' }, { label: 'Admin Panel' }]} />
      <h1 className="text-2xl font-bold text-ink">Admin Panel</h1>
      <ComingSoon icon={<ShieldCheck className="w-6 h-6" />} title="Administration" description="User management, permissions, firm settings, and billing coming soon." />
    </div>
  );
}
