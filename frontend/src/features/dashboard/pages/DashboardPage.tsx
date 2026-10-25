import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Briefcase, Calendar, CheckSquare, FileText, FileEdit, ShieldCheck,
  Plus, Search, Upload, ArrowRight, Clock, AlertCircle, TrendingUp,
  Scale
} from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import {
  StatCard, Card, Badge, StatusBadge, PriorityBadge, ConfidenceBadge,
  EmptyState, Skeleton, SkeletonCard,
} from '@/design-system';
import { Button } from '@/design-system';
import { Avatar } from '@/design-system';
import { formatDate, formatHearingDate } from '@/lib/utils';
import { ROUTES } from '@/constants';
import {
  mockCases, mockHearings, mockTasks, mockDocuments,
  mockAnalytics, mockNotifications, mockDrafts, mockAgentExecutions,
} from '@/services/api/mockData';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell,
} from 'recharts';
import { mockMonthlyActivity, mockCasesByStatus } from '@/services/api/mockData';

// ── Greeting ──────────────────────────────────────────────────────────────────

function getGreeting() {
  const h = new Date().getHours();
  if (h < 12) return 'Good morning';
  if (h < 17) return 'Good afternoon';
  return 'Good evening';
}

// ── Quick Action ──────────────────────────────────────────────────────────────

function QuickAction({ icon, label, onClick }: { icon: React.ReactNode; label: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="flex flex-col items-center gap-2 p-3 rounded-xl bg-surface/50 border border-border/70 hover:border-primary-500/40 hover:bg-surface-overlay transition-all duration-150 text-center group cursor-pointer"
    >
      <div className="w-9 h-9 rounded-lg bg-primary-500/10 border border-primary-500/20 text-primary-600 dark:text-primary-400 flex items-center justify-center group-hover:scale-105 group-hover:bg-primary-500/20 transition-all duration-150">
        {icon}
      </div>
      <span className="text-xs font-medium text-ink-secondary group-hover:text-ink transition-colors">{label}</span>
    </button>
  );
}

// ── Main Dashboard ────────────────────────────────────────────────────────────

export function DashboardPage() {
  const { user } = useAuthStore();
  const navigate = useNavigate();

  const activeCases = mockCases.filter((c) => c.status === 'active');
  const upcomingHearings = mockHearings
    .filter((h) => h.status === 'scheduled' && new Date(h.date) > new Date())
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    .slice(0, 3);
  const pendingTasks = mockTasks.filter((t) => t.status !== 'completed');
  const urgentTasks = mockTasks.filter((t) => t.priority === 'critical' && t.status !== 'completed');
  const recentDocs = mockDocuments.slice(0, 4);
  const verificationAlerts = mockNotifications.filter((n) => n.type === 'verification_warning');
  const unreadNotifications = mockNotifications.filter((n) => !n.isRead);

  return (
    <div className="space-y-6">
      {/* ── Page Header ─────────────────────────────────────── */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-ink">
            {getGreeting()}, {user?.name?.split(' ')[0]} 👋
          </h1>
          <p className="text-sm text-ink-secondary mt-1">
            Here's what needs your attention today.
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="secondary"
            size="sm"
            leftIcon={<Search className="w-4 h-4" />}
            onClick={() => navigate(ROUTES.RESEARCH)}
          >
            Research
          </Button>
          <Button
            variant="primary"
            size="sm"
            leftIcon={<Plus className="w-4 h-4" />}
            onClick={() => navigate(ROUTES.CASE_NEW)}
          >
            New Case
          </Button>
        </div>
      </div>

      {/* ── Urgent Alert ─────────────────────────────────────── */}
      {urgentTasks.length > 0 && (
        <div className="flex items-center justify-between gap-3 px-4 py-3 bg-rose-500/10 border border-rose-500/30 dark:bg-rose-950/40 dark:border-rose-800/60 rounded-xl shadow-xs">
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-500 flex items-center justify-center shrink-0">
              <AlertCircle className="w-4 h-4" />
            </div>
            <div className="min-w-0">
              <p className="text-sm font-semibold text-rose-700 dark:text-rose-200 truncate">
                {urgentTasks.length} critical task{urgentTasks.length > 1 ? 's' : ''} {urgentTasks.length === 1 ? 'needs' : 'need'} your attention
              </p>
              <p className="text-xs text-rose-600/80 dark:text-rose-300/80 hidden sm:block">
                Hearing preparations and court deadlines scheduled within 48 hours.
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate(ROUTES.TASKS)}
            className="shrink-0 px-3 py-1.5 text-xs font-semibold rounded-lg bg-rose-600 hover:bg-rose-700 text-white shadow-xs transition-colors cursor-pointer"
          >
            Review Tasks →
          </button>
        </div>
      )}

      {/* ── Stats Row ─────────────────────────────────────────── */}
      <div className="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-6 gap-3.5">
        <StatCard
          label="Active Cases"
          value={mockAnalytics.activeCases}
          icon={<Briefcase className="w-3.5 h-3.5" />}
          colorClass="bg-emerald-500/15 text-emerald-600 dark:text-emerald-400"
          onClick={() => navigate(ROUTES.CASES)}
        />
        <StatCard
          label="Upcoming Hearings"
          value={upcomingHearings.length}
          icon={<Calendar className="w-3.5 h-3.5" />}
          colorClass="bg-blue-500/15 text-blue-600 dark:text-blue-400"
          onClick={() => navigate(ROUTES.HEARINGS)}
        />
        <StatCard
          label="Pending Tasks"
          value={pendingTasks.length}
          icon={<CheckSquare className="w-3.5 h-3.5" />}
          colorClass="bg-amber-500/15 text-amber-600 dark:text-amber-400"
          onClick={() => navigate(ROUTES.TASKS)}
        />
        <StatCard
          label="Docs for Review"
          value={mockDocuments.filter((d) => d.status === 'needs_review').length}
          icon={<FileText className="w-3.5 h-3.5" />}
          colorClass="bg-purple-500/15 text-purple-600 dark:text-purple-400"
          onClick={() => navigate(ROUTES.DOCUMENTS)}
        />
        <StatCard
          label="Drafts in Review"
          value={mockDrafts.filter((d) => d.status === 'reviewing').length}
          icon={<FileEdit className="w-3.5 h-3.5" />}
          colorClass="bg-orange-500/15 text-orange-600 dark:text-orange-400"
          onClick={() => navigate(ROUTES.DRAFTS)}
        />
        <StatCard
          label="Verification Alerts"
          value={verificationAlerts.length}
          icon={<ShieldCheck className="w-3.5 h-3.5" />}
          colorClass="bg-rose-500/15 text-rose-600 dark:text-rose-400"
          onClick={() => navigate(ROUTES.VERIFICATION)}
        />
      </div>

      {/* ── Main Grid ─────────────────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column (2/3) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Today's Upcoming Hearings */}
          <Card>
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-ink">Upcoming Hearings</h2>
              <button
                onClick={() => navigate(ROUTES.HEARINGS)}
                className="text-xs text-primary-600 dark:text-primary-400 hover:underline flex items-center gap-1"
              >
                View all <ArrowRight className="w-3 h-3" />
              </button>
            </div>
            <div className="space-y-3">
              {upcomingHearings.length === 0 ? (
                <EmptyState
                  title="No upcoming hearings"
                  description="Your schedule is clear for now."
                  icon={<Calendar className="w-6 h-6" />}
                />
              ) : (
                upcomingHearings.map((h) => (
                  <div
                    key={h.id}
                    className="flex items-start gap-3.5 p-3.5 bg-surface/50 hover:bg-surface-overlay border border-border/50 hover:border-border-strong rounded-xl transition-all duration-150 cursor-pointer group"
                    onClick={() => navigate(ROUTES.CASES)}
                  >
                    <div className="w-11 h-11 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex flex-col items-center justify-center shrink-0 text-center group-hover:border-emerald-500/40 transition-colors">
                      <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider leading-none">
                        {formatDate(h.date, 'MMM')}
                      </span>
                      <span className="text-base font-extrabold text-ink leading-tight mt-0.5">
                        {formatDate(h.date, 'd')}
                      </span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold text-ink group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors truncate">
                        {h.caseName}
                      </p>
                      <p className="text-xs text-ink-secondary">{h.court}</p>
                      <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                        <span className="text-xs text-ink-muted flex items-center gap-1">
                          <Clock className="w-3 h-3 text-ink-muted" />
                          {formatHearingDate(h.date)} · {h.time}
                        </span>
                        <Badge variant="info" size="sm">{h.purpose}</Badge>
                      </div>
                    </div>
                    <StatusBadge status={h.status} />
                  </div>
                ))
              )}
            </div>
          </Card>

          {/* Active Cases */}
          <Card>
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-ink">My Active Cases</h2>
              <button
                onClick={() => navigate(ROUTES.CASES)}
                className="text-xs text-primary-600 dark:text-primary-400 hover:underline flex items-center gap-1"
              >
                View all <ArrowRight className="w-3 h-3" />
              </button>
            </div>
            <div className="space-y-2">
              {activeCases.slice(0, 4).map((c) => (
                <div
                  key={c.id}
                  className="flex items-center gap-3.5 p-3 rounded-xl border border-border/40 hover:border-border-strong hover:bg-surface-overlay transition-all duration-150 cursor-pointer group"
                  onClick={() => navigate(ROUTES.CASE_DETAIL(c.id))}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => e.key === 'Enter' && navigate(ROUTES.CASE_DETAIL(c.id))}
                >
                  <div className="w-9 h-9 rounded-lg bg-primary-500/10 border border-primary-500/20 text-primary-600 dark:text-primary-400 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
                    <Scale className="w-4 h-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-ink group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors truncate">
                      {c.title}
                    </p>
                    <p className="text-xs text-ink-secondary">{c.caseNumber} · {c.court}</p>
                  </div>
                  <div className="flex items-center gap-2.5 shrink-0">
                    <PriorityBadge priority={c.priority} />
                    {c.nextHearing && (
                      <span className="text-xs text-ink-muted hidden sm:inline-flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {formatHearingDate(c.nextHearing)}
                      </span>
                    )}
                  </div>
                  <ArrowRight className="w-4 h-4 text-ink-muted group-hover:text-ink group-hover:translate-x-0.5 transition-all shrink-0" />
                </div>
              ))}
            </div>
          </Card>

          {/* Activity Chart */}
          <Card>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="font-semibold text-ink">Activity Overview</h2>
                <p className="text-xs text-ink-secondary mt-0.5">Documents & legal research volume</p>
              </div>
              <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-surface-overlay text-ink-secondary border border-border">
                Last 6 months
              </span>
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <AreaChart data={mockMonthlyActivity} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorDocs" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.35} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="colorResearch" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.35} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="currentColor" className="text-border/40" />
                <XAxis dataKey="label" tick={{ fontSize: 11, fill: 'currentColor' }} className="text-ink-secondary" axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: 'currentColor' }} className="text-ink-secondary" axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--color-surface-raised)',
                    borderColor: 'var(--color-border)',
                    borderRadius: 8,
                    fontSize: 12,
                    color: 'var(--color-ink)',
                    boxShadow: 'var(--shadow-md)',
                  }}
                  itemStyle={{ color: 'var(--color-ink)' }}
                />
                <Area type="monotone" dataKey="docs" stroke="#10b981" strokeWidth={2} fill="url(#colorDocs)" name="Documents" />
                <Area type="monotone" dataKey="research" stroke="#3b82f6" strokeWidth={2} fill="url(#colorResearch)" name="Research" />
              </AreaChart>
            </ResponsiveContainer>
          </Card>
        </div>

        {/* Right column (1/3) */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <Card>
            <h2 className="font-semibold text-ink mb-3">Quick Actions</h2>
            <div className="grid grid-cols-3 gap-2">
              <QuickAction icon={<Plus className="w-4 h-4" />} label="New Case" onClick={() => navigate(ROUTES.CASE_NEW)} />
              <QuickAction icon={<Upload className="w-4 h-4" />} label="Upload Doc" onClick={() => navigate(ROUTES.DOCUMENTS)} />
              <QuickAction icon={<Search className="w-4 h-4" />} label="Research" onClick={() => navigate(ROUTES.RESEARCH)} />
              <QuickAction icon={<FileEdit className="w-4 h-4" />} label="New Draft" onClick={() => navigate(ROUTES.DRAFT_NEW)} />
              <QuickAction icon={<Calendar className="w-4 h-4" />} label="Add Hearing" onClick={() => navigate(ROUTES.HEARINGS)} />
              <QuickAction icon={<CheckSquare className="w-4 h-4" />} label="Add Task" onClick={() => navigate(ROUTES.TASKS)} />
            </div>
          </Card>

          {/* Tasks */}
          <Card>
            <div className="flex items-center justify-between mb-3">
              <h2 className="font-semibold text-ink">Pending Tasks</h2>
              <button
                onClick={() => navigate(ROUTES.TASKS)}
                className="text-xs text-primary-600 dark:text-primary-400 hover:underline flex items-center gap-1"
              >
                View all <ArrowRight className="w-3 h-3" />
              </button>
            </div>
            <div className="space-y-2">
              {pendingTasks.slice(0, 4).map((t) => (
                <div
                  key={t.id}
                  className="flex items-start gap-2.5 p-2.5 rounded-lg border border-border/40 hover:border-border-strong hover:bg-surface-overlay transition-all cursor-pointer group"
                  onClick={() => navigate(ROUTES.TASKS)}
                >
                  <div className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${
                    t.priority === 'critical' ? 'bg-rose-500 shadow-xs shadow-rose-500/50' :
                    t.priority === 'high' ? 'bg-amber-400' :
                    t.priority === 'medium' ? 'bg-blue-400' : 'bg-gray-400'
                  }`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-ink group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors leading-snug">{t.title}</p>
                    <p className="text-xs text-ink-secondary truncate mt-0.5">{t.caseName}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Cases by Status — Pie */}
          <Card>
            <h2 className="font-semibold text-ink mb-3">Cases by Status</h2>
            <div className="flex items-center gap-4">
              <ResponsiveContainer width={100} height={100}>
                <PieChart>
                  <Pie data={mockCasesByStatus} dataKey="value" cx="50%" cy="50%" innerRadius={30} outerRadius={48} strokeWidth={0}>
                    {mockCasesByStatus.map((entry, i) => (
                      <Cell
                        key={i}
                        fill={
                          entry.label === 'Active' ? '#10b981' :
                          entry.label === 'Pending' ? '#f59e0b' :
                          entry.label === 'Closed' ? '#64748b' : '#8b5cf6'
                        }
                      />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
              <div className="flex-1 space-y-1.5">
                {mockCasesByStatus.map((s) => {
                  const dotColor =
                    s.label === 'Active' ? '#10b981' :
                    s.label === 'Pending' ? '#f59e0b' :
                    s.label === 'Closed' ? '#64748b' : '#8b5cf6';
                  return (
                    <div key={s.label} className="flex items-center justify-between text-xs">
                      <div className="flex items-center gap-1.5">
                        <div className="w-2 h-2 rounded-full shrink-0" style={{ background: dotColor }} />
                        <span className="text-ink-secondary">{s.label}</span>
                      </div>
                      <span className="font-semibold text-ink">{s.value}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </Card>

          {/* Recent Documents */}
          <Card>
            <div className="flex items-center justify-between mb-3">
              <h2 className="font-semibold text-ink">Recent Documents</h2>
              <button
                onClick={() => navigate(ROUTES.DOCUMENTS)}
                className="text-xs text-primary-600 dark:text-primary-400 hover:underline flex items-center gap-1"
              >
                View all <ArrowRight className="w-3 h-3" />
              </button>
            </div>
            <div className="space-y-2">
              {recentDocs.map((d) => (
                <div
                  key={d.id}
                  className="flex items-center gap-3 p-2.5 rounded-lg border border-border/40 hover:border-border-strong hover:bg-surface-overlay transition-all cursor-pointer group"
                  onClick={() => navigate(ROUTES.DOCUMENTS)}
                >
                  <div className="w-8 h-8 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-center justify-center shrink-0 text-rose-500">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-ink group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors truncate">{d.title}</p>
                  </div>
                  <StatusBadge status={d.status} />
                </div>
              ))}
            </div>
          </Card>

          {/* Verification Alerts */}
          {verificationAlerts.length > 0 && (
            <Card className="border-amber-500/30 bg-amber-500/10 dark:bg-amber-950/30 dark:border-amber-800/50">
              <div className="flex items-center gap-2 mb-3">
                <ShieldCheck className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                <h2 className="font-semibold text-amber-800 dark:text-amber-200">Verification Alerts</h2>
              </div>
              {verificationAlerts.map((n) => (
                <div key={n.id} className="text-xs text-amber-700 dark:text-amber-300 p-2 bg-surface-raised rounded-[6px] border border-amber-500/20 mb-2">
                  {n.message}
                </div>
              ))}
              <button
                onClick={() => navigate(ROUTES.VERIFICATION)}
                className="text-xs text-amber-700 dark:text-amber-300 font-semibold hover:underline flex items-center gap-1"
              >
                Review all alerts <ArrowRight className="w-3 h-3" />
              </button>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
