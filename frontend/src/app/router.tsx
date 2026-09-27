import React, { lazy, Suspense } from 'react';
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import { AppShell } from '@/components/layout/AppShell';
import { AuthGuard, GuestGuard } from '@/features/auth/components/AuthGuard';
import { ROUTES } from '@/constants';
import { Skeleton } from '@/design-system';

// ── Auth Pages ────────────────────────────────────────────────────────────────

import { LoginPage, RegisterPage, ForgotPasswordPage } from '@/features/auth/pages/AuthPages';

// ── Feature Pages ─────────────────────────────────────────────────────────────

import { DashboardPage } from '@/features/dashboard/pages/DashboardPage';
import { CasesListPage, CaseNewPage } from '@/features/cases/pages/CasesPages';
import { CaseDetailPage } from '@/features/cases/pages/CaseDetailPage';
import { DocumentsPage } from '@/features/documents/pages/DocumentsPage';
import { ResearchPage } from '@/features/research/pages/ResearchPage';
import { DraftsListPage, DraftNewPage, DraftDetailPage } from '@/features/drafting/pages/DraftingPages';
import { VerificationPage } from '@/features/verification/pages/VerificationPage';
import { AIWorkspacePage, AgentActivityPage } from '@/features/ai-workspace/pages/AIWorkspacePages';
import { AnalyticsPage } from '@/features/analytics/pages/AnalyticsPage';
import { SettingsPage } from '@/features/settings/pages/SettingsPage';
import {
  TasksPage, HearingsPage, ClientsPage, TeamPage, NotificationsPage,
  EvidencePage, TimelinePage, CalendarPage, CollaborationPage, ReportsPage, AdminPage,
} from '@/features/misc/pages/MiscPages';

// ── Loading Fallback ──────────────────────────────────────────────────────────

function PageLoader() {
  return (
    <div className="space-y-4 p-6">
      <div className="h-8 w-48 bg-primary-100 rounded animate-pulse" />
      <div className="h-4 w-32 bg-surface-overlay rounded animate-pulse" />
      <div className="h-32 w-full bg-surface-overlay rounded-[12px] animate-pulse" />
    </div>
  );
}

// ── Router ────────────────────────────────────────────────────────────────────

const router = createBrowserRouter([
  // ── Public routes ──
  {
    path: ROUTES.LOGIN,
    element: (
      <GuestGuard>
        <LoginPage />
      </GuestGuard>
    ),
  },
  {
    path: ROUTES.REGISTER,
    element: (
      <GuestGuard>
        <RegisterPage />
      </GuestGuard>
    ),
  },
  {
    path: ROUTES.FORGOT_PASSWORD,
    element: (
      <GuestGuard>
        <ForgotPasswordPage />
      </GuestGuard>
    ),
  },

  // ── App routes ──
  {
    path: '/',
    element: (
      <AuthGuard>
        <AppShell />
      </AuthGuard>
    ),
    children: [
      { index: true, element: <Navigate to={ROUTES.DASHBOARD} replace /> },
      { path: ROUTES.DASHBOARD, element: <DashboardPage /> },

      // Cases
      { path: ROUTES.CASES, element: <CasesListPage /> },
      { path: ROUTES.CASE_NEW, element: <CaseNewPage /> },
      { path: ROUTES.CASE_DETAIL(), element: <CaseDetailPage /> },

      // Documents
      { path: ROUTES.DOCUMENTS, element: <DocumentsPage /> },

      // Research
      { path: ROUTES.RESEARCH, element: <ResearchPage /> },

      // Drafts
      { path: ROUTES.DRAFTS, element: <DraftsListPage /> },
      { path: ROUTES.DRAFT_NEW, element: <DraftNewPage /> },
      { path: ROUTES.DRAFT_DETAIL(), element: <DraftDetailPage /> },

      // Evidence, Timeline, Hearings, Calendar
      { path: ROUTES.EVIDENCE, element: <EvidencePage /> },
      { path: ROUTES.TIMELINE, element: <TimelinePage /> },
      { path: ROUTES.HEARINGS, element: <HearingsPage /> },
      { path: ROUTES.CALENDAR, element: <CalendarPage /> },

      // Tasks
      { path: ROUTES.TASKS, element: <TasksPage /> },

      // AI Workspace
      { path: ROUTES.AI_WORKSPACE, element: <AIWorkspacePage /> },
      { path: ROUTES.AGENTS_ACTIVITY, element: <AgentActivityPage /> },

      // Verification
      { path: ROUTES.VERIFICATION, element: <VerificationPage /> },

      // Collaboration
      { path: ROUTES.CLIENTS, element: <ClientsPage /> },
      { path: ROUTES.TEAM, element: <TeamPage /> },
      { path: ROUTES.COLLABORATION, element: <CollaborationPage /> },

      // Insights
      { path: ROUTES.ANALYTICS, element: <AnalyticsPage /> },
      { path: ROUTES.REPORTS, element: <ReportsPage /> },

      // Admin
      { path: ROUTES.ADMIN, element: <AdminPage /> },

      // Settings
      { path: ROUTES.SETTINGS, element: <SettingsPage /> },
      { path: ROUTES.SETTINGS_PROFILE, element: <SettingsPage /> },

      // Notifications
      { path: ROUTES.NOTIFICATIONS, element: <NotificationsPage /> },

      // Catch-all
      { path: '*', element: <Navigate to={ROUTES.DASHBOARD} replace /> },
    ],
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
