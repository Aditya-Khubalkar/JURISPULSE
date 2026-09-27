import type {
  Case, Document, Draft, ResearchResult, Hearing, Task,
  AgentExecution, AIModel, Client, Notification, AnalyticsOverview,
  PaginatedResponse, ApiResponse, User,
} from '@/types';

import {
  mockCases, mockDocuments, mockDrafts, mockResearchResults,
  mockHearings, mockTasks, mockAgentExecutions, mockAIModels,
  mockClients, mockNotifications, mockAnalytics, mockCasesByStatus,
  mockCasesByType, mockMonthlyActivity, mockCurrentUser, mockUsers,
  mockTimelineEvents,
} from './mockData';

// ── Delay simulator ───────────────────────────────────────────────────────────

const delay = (ms = 600) => new Promise((resolve) => setTimeout(resolve, ms));

function paginate<T>(items: T[], page = 1, pageSize = 20): PaginatedResponse<T> {
  const start = (page - 1) * pageSize;
  const data = items.slice(start, start + pageSize);
  return {
    data,
    total: items.length,
    page,
    pageSize,
    totalPages: Math.ceil(items.length / pageSize),
  };
}

// ── Auth API ──────────────────────────────────────────────────────────────────

export const authApi = {
  login: async (email: string, _password: string): Promise<ApiResponse<{ user: User; token: string }>> => {
    await delay(800);
    const user = mockUsers.find((u) => u.email === email) ?? mockCurrentUser;
    return {
      success: true,
      data: { user, token: 'mock-jwt-token-' + Date.now() },
    };
  },

  register: async (_data: unknown): Promise<ApiResponse<{ user: User; token: string }>> => {
    await delay(1000);
    return {
      success: true,
      data: { user: mockCurrentUser, token: 'mock-jwt-token-' + Date.now() },
    };
  },

  logout: async (): Promise<void> => {
    await delay(200);
  },

  me: async (): Promise<ApiResponse<User>> => {
    await delay(300);
    return { success: true, data: mockCurrentUser };
  },

  forgotPassword: async (_email: string): Promise<ApiResponse<null>> => {
    await delay(800);
    return { success: true, data: null, message: 'Password reset email sent.' };
  },

  resetPassword: async (_token: string, _password: string): Promise<ApiResponse<null>> => {
    await delay(800);
    return { success: true, data: null, message: 'Password reset successfully.' };
  },
};

// ── Cases API ─────────────────────────────────────────────────────────────────

export const casesApi = {
  list: async (params?: { page?: number; pageSize?: number; search?: string; status?: string }): Promise<PaginatedResponse<Case>> => {
    await delay(500);
    let filtered = [...mockCases];
    if (params?.search) {
      const q = params.search.toLowerCase();
      filtered = filtered.filter(
        (c) => c.title.toLowerCase().includes(q) || c.caseNumber.toLowerCase().includes(q) || c.clientName.toLowerCase().includes(q)
      );
    }
    if (params?.status) {
      filtered = filtered.filter((c) => c.status === params.status);
    }
    return paginate(filtered, params?.page, params?.pageSize);
  },

  get: async (id: string): Promise<ApiResponse<Case>> => {
    await delay(400);
    const c = mockCases.find((c) => c.id === id);
    if (!c) throw new Error('Case not found');
    return { success: true, data: c };
  },

  create: async (data: Partial<Case>): Promise<ApiResponse<Case>> => {
    await delay(900);
    const newCase: Case = {
      id: 'c' + Date.now(),
      caseNumber: 'MOCK/2024/' + Math.floor(Math.random() * 9999),
      title: data.title ?? 'New Case',
      caseType: data.caseType ?? 'civil',
      court: data.court ?? '',
      jurisdiction: data.jurisdiction ?? '',
      filingDate: new Date().toISOString(),
      status: 'active',
      priority: data.priority ?? 'medium',
      parties: data.parties ?? [],
      clientId: data.clientId ?? '',
      clientName: data.clientName ?? '',
      assignedLawyers: data.assignedLawyers ?? [],
      description: data.description,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    return { success: true, data: newCase };
  },

  update: async (id: string, data: Partial<Case>): Promise<ApiResponse<Case>> => {
    await delay(700);
    const existing = mockCases.find((c) => c.id === id);
    if (!existing) throw new Error('Case not found');
    return { success: true, data: { ...existing, ...data, updatedAt: new Date().toISOString() } };
  },

  delete: async (_id: string): Promise<ApiResponse<null>> => {
    await delay(600);
    return { success: true, data: null };
  },

  getTimeline: async (caseId: string) => {
    await delay(400);
    return { success: true, data: mockTimelineEvents.filter((e) => e.caseId === caseId) };
  },

  getSummary: async (_caseId: string) => {
    await delay(600);
    return {
      success: true,
      data: {
        summary: 'This is a writ petition challenging arbitrary transfer orders. The petitioner, a railway employee, alleges violation of service rules. Notice has been issued and counter affidavit received. Arguments are scheduled.',
        riskFactors: ['Upcoming hearing in 5 days', 'Bail application pending in related matter'],
        recommendations: ['Prepare counter arguments to UoI response', 'File additional documents before next hearing'],
      },
    };
  },
};

// ── Documents API ─────────────────────────────────────────────────────────────

export const documentsApi = {
  list: async (params?: { caseId?: string; page?: number; search?: string }): Promise<PaginatedResponse<Document>> => {
    await delay(500);
    let filtered = [...mockDocuments];
    if (params?.caseId) {
      filtered = filtered.filter((d) => d.caseId === params.caseId);
    }
    if (params?.search) {
      const q = params.search.toLowerCase();
      filtered = filtered.filter((d) => d.title.toLowerCase().includes(q));
    }
    return paginate(filtered, params?.page);
  },

  get: async (id: string): Promise<ApiResponse<Document>> => {
    await delay(400);
    const d = mockDocuments.find((d) => d.id === id);
    if (!d) throw new Error('Document not found');
    return { success: true, data: d };
  },

  upload: async (_file: File, _meta: Partial<Document>): Promise<ApiResponse<Document>> => {
    await delay(1500);
    return {
      success: true,
      data: {
        id: 'doc-' + Date.now(),
        title: 'New Document',
        fileName: 'new_document.pdf',
        fileSize: 100000,
        fileType: 'application/pdf',
        documentType: 'other',
        status: 'processing',
        uploadedBy: 'u1',
        uploadedAt: new Date().toISOString(),
        version: 1,
      },
    };
  },

  delete: async (_id: string): Promise<ApiResponse<null>> => {
    await delay(500);
    return { success: true, data: null };
  },
};

// ── Research API ──────────────────────────────────────────────────────────────

export const researchApi = {
  search: async (_query: string, _filters?: Record<string, string>): Promise<ApiResponse<ResearchResult[]>> => {
    await delay(1200);
    return { success: true, data: mockResearchResults };
  },

  get: async (id: string): Promise<ApiResponse<ResearchResult>> => {
    await delay(400);
    const r = mockResearchResults.find((r) => r.id === id);
    if (!r) throw new Error('Result not found');
    return { success: true, data: r };
  },
};

// ── Drafts API ────────────────────────────────────────────────────────────────

export const draftsApi = {
  list: async (): Promise<PaginatedResponse<Draft>> => {
    await delay(500);
    return paginate(mockDrafts);
  },

  get: async (id: string): Promise<ApiResponse<Draft>> => {
    await delay(400);
    const d = mockDrafts.find((d) => d.id === id);
    if (!d) throw new Error('Draft not found');
    return { success: true, data: d };
  },

  generate: async (_params: { caseId: string; draftType: string; instructions?: string }): Promise<ApiResponse<Draft>> => {
    await delay(3000);
    return { success: true, data: mockDrafts[0] };
  },

  update: async (id: string, data: Partial<Draft>): Promise<ApiResponse<Draft>> => {
    await delay(600);
    const existing = mockDrafts.find((d) => d.id === id);
    if (!existing) throw new Error('Draft not found');
    return { success: true, data: { ...existing, ...data, updatedAt: new Date().toISOString() } };
  },

  approve: async (id: string): Promise<ApiResponse<Draft>> => {
    await delay(700);
    const existing = mockDrafts.find((d) => d.id === id);
    if (!existing) throw new Error('Draft not found');
    return {
      success: true,
      data: {
        ...existing,
        status: 'approved',
        approvedBy: 'u1',
        approvedAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      },
    };
  },
};

// ── Hearings API ──────────────────────────────────────────────────────────────

export const hearingsApi = {
  list: async (params?: { caseId?: string }): Promise<PaginatedResponse<Hearing>> => {
    await delay(500);
    let data = [...mockHearings];
    if (params?.caseId) data = data.filter((h) => h.caseId === params.caseId);
    return paginate(data);
  },

  get: async (id: string): Promise<ApiResponse<Hearing>> => {
    await delay(400);
    const h = mockHearings.find((h) => h.id === id);
    if (!h) throw new Error('Hearing not found');
    return { success: true, data: h };
  },

  create: async (data: Partial<Hearing>): Promise<ApiResponse<Hearing>> => {
    await delay(800);
    return {
      success: true,
      data: {
        id: 'h-' + Date.now(),
        caseId: data.caseId ?? '',
        caseName: data.caseName ?? '',
        caseNumber: data.caseNumber ?? '',
        court: data.court ?? '',
        date: data.date ?? new Date().toISOString(),
        time: data.time ?? '10:00',
        purpose: data.purpose ?? '',
        status: 'scheduled',
        createdAt: new Date().toISOString(),
      },
    };
  },
};

// ── Tasks API ─────────────────────────────────────────────────────────────────

export const tasksApi = {
  list: async (): Promise<PaginatedResponse<Task>> => {
    await delay(500);
    return paginate(mockTasks);
  },

  get: async (id: string): Promise<ApiResponse<Task>> => {
    await delay(400);
    const t = mockTasks.find((t) => t.id === id);
    if (!t) throw new Error('Task not found');
    return { success: true, data: t };
  },

  create: async (data: Partial<Task>): Promise<ApiResponse<Task>> => {
    await delay(700);
    return {
      success: true,
      data: {
        id: 't-' + Date.now(),
        title: data.title ?? 'New Task',
        caseId: data.caseId,
        caseName: data.caseName,
        assigneeId: data.assigneeId ?? 'u1',
        assigneeName: data.assigneeName ?? 'Arjun Sharma',
        priority: data.priority ?? 'medium',
        status: 'todo',
        createdBy: 'u1',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      },
    };
  },

  updateStatus: async (id: string, status: Task['status']): Promise<ApiResponse<Task>> => {
    await delay(400);
    const t = mockTasks.find((t) => t.id === id);
    if (!t) throw new Error('Task not found');
    return { success: true, data: { ...t, status, updatedAt: new Date().toISOString() } };
  },
};

// ── Notifications API ─────────────────────────────────────────────────────────

export const notificationsApi = {
  list: async (): Promise<PaginatedResponse<Notification>> => {
    await delay(300);
    return paginate(mockNotifications);
  },

  markRead: async (_id: string): Promise<ApiResponse<null>> => {
    await delay(200);
    return { success: true, data: null };
  },

  markAllRead: async (): Promise<ApiResponse<null>> => {
    await delay(300);
    return { success: true, data: null };
  },
};

// ── Agents API ────────────────────────────────────────────────────────────────

export const agentsApi = {
  listExecutions: async (params?: { caseId?: string }): Promise<PaginatedResponse<AgentExecution>> => {
    await delay(600);
    let data = [...mockAgentExecutions];
    if (params?.caseId) data = data.filter((e) => e.caseId === params.caseId);
    return paginate(data);
  },

  getExecution: async (id: string): Promise<ApiResponse<AgentExecution>> => {
    await delay(400);
    const e = mockAgentExecutions.find((e) => e.id === id);
    if (!e) throw new Error('Execution not found');
    return { success: true, data: e };
  },
};

// ── Admin API ─────────────────────────────────────────────────────────────────

export const adminApi = {
  listModels: async (): Promise<ApiResponse<AIModel[]>> => {
    await delay(500);
    return { success: true, data: mockAIModels };
  },

  listUsers: async (): Promise<PaginatedResponse<User>> => {
    await delay(500);
    return paginate(mockUsers);
  },

  updateUserStatus: async (id: string, isActive: boolean): Promise<ApiResponse<User>> => {
    await delay(600);
    const u = mockUsers.find((u) => u.id === id);
    if (!u) throw new Error('User not found');
    return { success: true, data: { ...u, isActive } };
  },
};

// ── Analytics API ─────────────────────────────────────────────────────────────

export const analyticsApi = {
  getOverview: async (): Promise<ApiResponse<AnalyticsOverview>> => {
    await delay(600);
    return { success: true, data: mockAnalytics };
  },

  getCasesByStatus: async () => {
    await delay(400);
    return { success: true, data: mockCasesByStatus };
  },

  getCasesByType: async () => {
    await delay(400);
    return { success: true, data: mockCasesByType };
  },

  getMonthlyActivity: async () => {
    await delay(500);
    return { success: true, data: mockMonthlyActivity };
  },
};

// ── Clients API ───────────────────────────────────────────────────────────────

export const clientsApi = {
  list: async (): Promise<PaginatedResponse<Client>> => {
    await delay(500);
    return paginate(mockClients);
  },

  get: async (id: string): Promise<ApiResponse<Client>> => {
    await delay(400);
    const c = mockClients.find((c) => c.id === id);
    if (!c) throw new Error('Client not found');
    return { success: true, data: c };
  },
};
