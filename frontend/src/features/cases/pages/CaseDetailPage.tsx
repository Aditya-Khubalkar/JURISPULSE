import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Briefcase, Upload, Search, FileEdit, Calendar, Plus,
  MoreHorizontal, Clock, Users, AlertTriangle, FileText, Scale,
  ArrowLeft, CheckCircle,
} from 'lucide-react';
import {
  Card, StatCard, StatusBadge, PriorityBadge, Badge, Tabs,
  EmptyState, Breadcrumb, Button, Avatar, AvatarGroup, VerificationBadge,
  ConfidenceBadge, AgentStatusBadge,
} from '@/design-system';
import { formatDate, formatHearingDate } from '@/lib/utils';
import { ROUTES, CASE_TYPE_LABELS } from '@/constants';
import { mockCases, mockDocuments, mockHearings, mockTasks, mockTimelineEvents, mockDrafts, mockAgentExecutions } from '@/services/api/mockData';
import type { TabItem } from '@/design-system';

const CASE_TABS: TabItem[] = [
  { id: 'overview', label: 'Overview' },
  { id: 'documents', label: 'Documents' },
  { id: 'evidence', label: 'Evidence' },
  { id: 'research', label: 'Research' },
  { id: 'drafts', label: 'Drafts' },
  { id: 'timeline', label: 'Timeline' },
  { id: 'hearings', label: 'Hearings' },
  { id: 'tasks', label: 'Tasks' },
  { id: 'notes', label: 'Notes' },
  { id: 'activity', label: 'Activity' },
  { id: 'ai', label: 'AI Insights' },
];

// ── Case Overview Tab ─────────────────────────────────────────────────────────

function CaseOverviewTab({ caseId }: { caseId: string }) {
  const caseData = mockCases.find((c) => c.id === caseId);
  if (!caseData) return null;

  const nextHearing = mockHearings.find((h) => h.caseId === caseId && h.status === 'scheduled');

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 pt-4">
      <div className="lg:col-span-2 space-y-4">
        {/* Case summary */}
        <Card>
          <h3 className="font-semibold text-ink mb-3">Case Summary</h3>
          <p className="text-sm text-ink-secondary leading-relaxed">
            {caseData.description ?? 'No description provided.'}
          </p>
          <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
            <div>
              <span className="text-ink-muted text-xs uppercase tracking-wider">Court</span>
              <p className="text-ink font-medium mt-0.5">{caseData.court}</p>
            </div>
            <div>
              <span className="text-ink-muted text-xs uppercase tracking-wider">Case Type</span>
              <p className="text-ink font-medium mt-0.5">{CASE_TYPE_LABELS[caseData.caseType]}</p>
            </div>
            <div>
              <span className="text-ink-muted text-xs uppercase tracking-wider">Filing Date</span>
              <p className="text-ink font-medium mt-0.5">{formatDate(caseData.filingDate)}</p>
            </div>
            <div>
              <span className="text-ink-muted text-xs uppercase tracking-wider">Jurisdiction</span>
              <p className="text-ink font-medium mt-0.5">{caseData.jurisdiction}</p>
            </div>
          </div>
        </Card>

        {/* Parties */}
        <Card>
          <h3 className="font-semibold text-ink mb-3">Parties</h3>
          <div className="space-y-2">
            {caseData.parties.map((party) => (
              <div key={party.id} className="flex items-center gap-3 p-2.5 bg-surface rounded-[6px]">
                <Avatar name={party.name} size="sm" />
                <div>
                  <p className="text-sm font-medium text-ink">{party.name}</p>
                  <Badge variant="neutral" size="sm">{party.role}</Badge>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Next Hearing */}
        {nextHearing && (
          <Card className="border-blue-200 bg-blue-50">
            <div className="flex items-start gap-3">
              <Calendar className="w-5 h-5 text-blue-600 mt-0.5 shrink-0" />
              <div>
                <p className="font-semibold text-blue-900">Next Hearing</p>
                <p className="text-sm text-blue-700">
                  {formatDate(nextHearing.date)} at {nextHearing.time} — {nextHearing.purpose}
                </p>
                <p className="text-xs text-blue-600 mt-0.5">{nextHearing.court}</p>
              </div>
            </div>
          </Card>
        )}
      </div>

      {/* Sidebar */}
      <div className="space-y-4">
        <Card>
          <h3 className="font-semibold text-ink mb-3">Assigned Team</h3>
          <div className="space-y-2">
            {['Arjun Sharma (Lead)', 'Rahul Verma (Junior)'].map((name) => (
              <div key={name} className="flex items-center gap-2">
                <Avatar name={name.split(' ')[0]} size="sm" />
                <span className="text-sm text-ink">{name}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <h3 className="font-semibold text-ink mb-3">Risk Overview</h3>
          <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-[6px] text-sm font-medium ${
            caseData.riskLevel === 'high' ? 'bg-red-50 text-red-700' :
            caseData.riskLevel === 'medium' ? 'bg-amber-50 text-amber-700' :
            'bg-green-50 text-green-700'
          }`}>
            <AlertTriangle className="w-3.5 h-3.5" />
            {caseData.riskLevel?.charAt(0).toUpperCase()}{caseData.riskLevel?.slice(1)} Risk
          </div>
          {caseData.tags && (
            <div className="mt-3 flex flex-wrap gap-1.5">
              {caseData.tags.map((tag) => (
                <Badge key={tag} variant="neutral" size="sm">{tag}</Badge>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

// ── Documents Tab ─────────────────────────────────────────────────────────────

function CaseDocumentsTab({ caseId }: { caseId: string }) {
  const docs = mockDocuments.filter((d) => d.caseId === caseId);
  return (
    <div className="pt-4 space-y-3">
      <div className="flex justify-end">
        <Button size="sm" leftIcon={<Upload className="w-4 h-4" />} variant="secondary">
          Upload Document
        </Button>
      </div>
      {docs.length === 0 ? (
        <EmptyState
          icon={<FileText className="w-6 h-6" />}
          title="No documents"
          description="Upload documents for this case."
        />
      ) : (
        docs.map((d) => (
          <Card key={d.id} hoverable>
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-[6px] bg-red-50 flex items-center justify-center shrink-0">
                <FileText className="w-4 h-4 text-red-400" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-ink">{d.title}</p>
                <p className="text-xs text-ink-secondary">{d.fileName} · {formatDate(d.uploadedAt)}</p>
              </div>
              <StatusBadge status={d.status} />
            </div>
          </Card>
        ))
      )}
    </div>
  );
}

// ── Timeline Tab ──────────────────────────────────────────────────────────────

function CaseTimelineTab({ caseId }: { caseId: string }) {
  const events = mockTimelineEvents.filter((e) => e.caseId === caseId);
  const typeColors: Record<string, string> = {
    filing: 'bg-blue-500',
    hearing: 'bg-primary-400',
    notice: 'bg-amber-400',
    reply: 'bg-purple-400',
    evidence: 'bg-orange-400',
    order: 'bg-primary-700',
    judgment: 'bg-red-500',
    other: 'bg-gray-400',
  };
  return (
    <div className="pt-4">
      {events.length === 0 ? (
        <EmptyState icon={<Clock className="w-6 h-6" />} title="No timeline events" description="Events will appear here as the case progresses." />
      ) : (
        <div className="relative">
          <div className="absolute left-4 top-0 bottom-0 w-px bg-border" />
          <div className="space-y-4 ml-10">
            {events.map((ev) => (
              <div key={ev.id} className="relative">
                <div
                  className={`absolute -left-10 w-3 h-3 rounded-full border-2 border-white mt-0.5 ${typeColors[ev.type] ?? 'bg-gray-400'}`}
                  style={{ left: '-2.2rem' }}
                />
                <Card>
                  <div className="flex items-start justify-between">
                    <div>
                      <Badge variant="neutral" size="sm" className="mb-1.5">{ev.type}</Badge>
                      <p className="font-medium text-ink">{ev.title}</p>
                      {ev.description && <p className="text-sm text-ink-secondary mt-0.5">{ev.description}</p>}
                    </div>
                    <span className="text-xs text-ink-muted shrink-0 ml-4">{formatDate(ev.date)}</span>
                  </div>
                </Card>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ── Hearings Tab ──────────────────────────────────────────────────────────────

function CaseHearingsTab({ caseId }: { caseId: string }) {
  const hearings = mockHearings.filter((h) => h.caseId === caseId);
  return (
    <div className="pt-4 space-y-3">
      {hearings.map((h) => (
        <Card key={h.id}>
          <div className="flex items-start justify-between">
            <div className="flex gap-3">
              <div className="w-10 h-10 rounded-[8px] bg-primary-100 flex flex-col items-center justify-center shrink-0">
                <span className="text-[10px] font-bold text-primary-700 uppercase">{formatDate(h.date, 'MMM')}</span>
                <span className="text-base font-bold text-primary-700 leading-none">{formatDate(h.date, 'd')}</span>
              </div>
              <div>
                <p className="font-medium text-ink">{h.purpose}</p>
                <p className="text-sm text-ink-secondary">{h.court}</p>
                {h.judge && <p className="text-xs text-ink-muted">Before: {h.judge}</p>}
                {h.outcome && (
                  <div className="mt-1.5 p-2 bg-primary-50 rounded-[6px] text-xs text-primary-700">
                    <CheckCircle className="w-3 h-3 inline mr-1" />
                    {h.outcome}
                  </div>
                )}
              </div>
            </div>
            <StatusBadge status={h.status} />
          </div>
        </Card>
      ))}
    </div>
  );
}

// ── Tasks Tab ─────────────────────────────────────────────────────────────────

function CaseTasksTab({ caseId }: { caseId: string }) {
  const tasks = mockTasks.filter((t) => t.caseId === caseId);
  return (
    <div className="pt-4 space-y-3">
      {tasks.map((t) => (
        <Card key={t.id}>
          <div className="flex items-center gap-3">
            <div className={`w-2 h-2 rounded-full shrink-0 ${
              t.priority === 'critical' ? 'bg-red-500' :
              t.priority === 'high' ? 'bg-orange-400' :
              t.priority === 'medium' ? 'bg-amber-400' : 'bg-gray-300'
            }`} />
            <div className="flex-1">
              <p className="font-medium text-ink">{t.title}</p>
              <div className="flex items-center gap-2 mt-1">
                <Avatar name={t.assigneeName} size="xs" />
                <span className="text-xs text-ink-secondary">{t.assigneeName}</span>
                {t.dueDate && <span className="text-xs text-ink-muted">Due: {formatDate(t.dueDate)}</span>}
              </div>
            </div>
            <StatusBadge status={t.status} />
          </div>
        </Card>
      ))}
    </div>
  );
}

// ── AI Insights Tab ───────────────────────────────────────────────────────────

function CaseAIInsightsTab({ caseId }: { caseId: string }) {
  const executions = mockAgentExecutions.filter((e) => e.caseId === caseId);
  return (
    <div className="pt-4 space-y-4">
      <Card className="border-primary-200 bg-primary-50">
        <div className="flex items-center gap-2 mb-2">
          <Scale className="w-4 h-4 text-primary-700" />
          <span className="font-semibold text-primary-700 text-sm">AI Case Summary</span>
          <ConfidenceBadge score={0.88} />
        </div>
        <p className="text-sm text-ink leading-relaxed">
          This is a writ petition challenging arbitrary transfer orders issued by the Ministry of Railways.
          The petitioner alleges violation of service rules and Article 226 rights. Notice has been issued and a
          counter affidavit received. Arguments are scheduled. Risk level is <strong>medium</strong> based on precedents.
        </p>
      </Card>

      <h3 className="font-semibold text-ink">Agent Executions</h3>
      <div className="space-y-2">
        {executions.map((ex) => (
          <Card key={ex.id}>
            <div className="flex items-center gap-3">
              <div className={`w-2 h-2 rounded-full ${
                ex.status === 'completed' ? 'bg-green-400' :
                ex.status === 'running' ? 'bg-blue-400 animate-pulse' :
                ex.status === 'failed' ? 'bg-red-400' : 'bg-gray-300'
              }`} />
              <div className="flex-1">
                <p className="font-medium text-sm text-ink">{ex.agentName}</p>
                {ex.sources && (
                  <p className="text-xs text-ink-secondary">Sources: {ex.sources.join(', ')}</p>
                )}
              </div>
              <div className="flex items-center gap-2">
                {ex.confidence && <ConfidenceBadge score={ex.confidence} />}
                <AgentStatusBadge status={ex.status} />
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// ── Case Detail Page ──────────────────────────────────────────────────────────

export function CaseDetailPage() {
  const { caseId } = useParams<{ caseId: string }>();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');

  const caseData = mockCases.find((c) => c.id === caseId);

  if (!caseData) {
    return (
      <div className="text-center py-20">
        <p className="text-ink-secondary">Case not found.</p>
        <button onClick={() => navigate(ROUTES.CASES)} className="text-primary-700 hover:underline mt-2 block mx-auto">
          Back to Cases
        </button>
      </div>
    );
  }

  const tabContent: Record<string, React.ReactNode> = {
    overview: <CaseOverviewTab caseId={caseData.id} />,
    documents: <CaseDocumentsTab caseId={caseData.id} />,
    evidence: <EmptyState icon={<Scale className="w-6 h-6" />} title="Evidence" description="Evidence management coming soon." className="pt-8" />,
    research: <EmptyState icon={<Search className="w-6 h-6" />} title="Research" description="Saved research will appear here." className="pt-8" />,
    drafts: <EmptyState icon={<FileEdit className="w-6 h-6" />} title="Drafts" description="Generated drafts for this case will appear here." className="pt-8" />,
    timeline: <CaseTimelineTab caseId={caseData.id} />,
    hearings: <CaseHearingsTab caseId={caseData.id} />,
    tasks: <CaseTasksTab caseId={caseData.id} />,
    notes: <EmptyState icon={<FileText className="w-6 h-6" />} title="Notes" description="Internal notes will appear here." className="pt-8" />,
    activity: <EmptyState icon={<Clock className="w-6 h-6" />} title="Activity" description="Recent activity log will appear here." className="pt-8" />,
    ai: <CaseAIInsightsTab caseId={caseData.id} />,
  };

  return (
    <div className="space-y-5">
      {/* Breadcrumb */}
      <Breadcrumb
        items={[
          { label: 'Cases', onClick: () => navigate(ROUTES.CASES) },
          { label: caseData.title },
        ]}
      />

      {/* Case Header */}
      <Card>
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-[10px] bg-primary-100 flex items-center justify-center shrink-0">
              <Briefcase className="w-6 h-6 text-primary-700" />
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <h1 className="text-xl font-bold text-ink">{caseData.title}</h1>
                <StatusBadge status={caseData.status} />
                <PriorityBadge priority={caseData.priority} />
              </div>
              <p className="text-sm text-ink-secondary mt-0.5">
                {caseData.caseNumber} · {caseData.court}
              </p>
              {caseData.clientName && (
                <p className="text-sm text-ink-secondary">Client: <span className="text-ink font-medium">{caseData.clientName}</span></p>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex flex-wrap gap-2">
            <Button size="sm" variant="secondary" leftIcon={<Upload className="w-3.5 h-3.5" />}>
              Upload
            </Button>
            <Button size="sm" variant="secondary" leftIcon={<Search className="w-3.5 h-3.5" />}
              onClick={() => navigate(ROUTES.RESEARCH)}>
              Research
            </Button>
            <Button size="sm" variant="secondary" leftIcon={<FileEdit className="w-3.5 h-3.5" />}
              onClick={() => navigate(ROUTES.DRAFT_NEW)}>
              Draft
            </Button>
            <Button size="sm" variant="secondary" leftIcon={<Calendar className="w-3.5 h-3.5" />}>
              Add Hearing
            </Button>
            <Button size="sm" variant="secondary" leftIcon={<Plus className="w-3.5 h-3.5" />}>
              Add Task
            </Button>
          </div>
        </div>
      </Card>

      {/* Tabs */}
      <div>
        <Tabs tabs={CASE_TABS} activeTab={activeTab} onChange={setActiveTab} />
        {tabContent[activeTab]}
      </div>
    </div>
  );
}
