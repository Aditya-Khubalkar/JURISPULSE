// ── User & Auth Types ────────────────────────────────────────────────────────

export type UserRole = 'admin' | 'lawyer' | 'junior' | 'client';

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  organization?: string;
  avatar?: string;
  phone?: string;
  barCouncilId?: string;
  createdAt: string;
  updatedAt: string;
  isActive: boolean;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

// ── Case Types ───────────────────────────────────────────────────────────────

export type CaseStatus = 'active' | 'pending' | 'closed' | 'stayed' | 'disposed' | 'appeal';
export type CasePriority = 'critical' | 'high' | 'medium' | 'low';
export type CaseType =
  | 'civil'
  | 'criminal'
  | 'family'
  | 'labour'
  | 'consumer'
  | 'constitutional'
  | 'corporate'
  | 'property'
  | 'tax'
  | 'writ'
  | 'other';

export interface Party {
  id: string;
  name: string;
  role: 'petitioner' | 'respondent' | 'appellant' | 'defendant' | 'plaintiff' | 'other';
  advocate?: string;
  contact?: string;
}

export interface Case {
  id: string;
  caseNumber: string;
  title: string;
  caseType: CaseType;
  court: string;
  jurisdiction: string;
  filingDate: string;
  status: CaseStatus;
  priority: CasePriority;
  parties: Party[];
  clientId: string;
  clientName: string;
  assignedLawyers: string[];
  description?: string;
  tags?: string[];
  nextHearing?: string;
  deadlineDate?: string;
  riskLevel?: 'low' | 'medium' | 'high';
  createdAt: string;
  updatedAt: string;
}

// ── Document Types ───────────────────────────────────────────────────────────

export type DocumentStatus =
  | 'uploaded'
  | 'processing'
  | 'processed'
  | 'needs_review'
  | 'verified'
  | 'failed';

export type DocumentType =
  | 'petition'
  | 'affidavit'
  | 'notice'
  | 'order'
  | 'judgment'
  | 'evidence'
  | 'reply'
  | 'written_statement'
  | 'bail_application'
  | 'appeal'
  | 'complaint'
  | 'contract'
  | 'other';

export interface DocumentEntity {
  type: 'person' | 'organization' | 'date' | 'act' | 'section' | 'citation' | 'location' | 'amount';
  value: string;
  confidence: number;
  position?: { page: number; x: number; y: number };
}

export interface Document {
  id: string;
  title: string;
  fileName: string;
  fileSize: number;
  fileType: string;
  documentType: DocumentType;
  caseId?: string;
  caseName?: string;
  status: DocumentStatus;
  tags?: string[];
  entities?: DocumentEntity[];
  ocrText?: string;
  uploadedBy: string;
  uploadedAt: string;
  processedAt?: string;
  version: number;
  url?: string;
}

// ── Draft Types ──────────────────────────────────────────────────────────────

export type DraftType =
  | 'petition'
  | 'affidavit'
  | 'legal_notice'
  | 'bail_application'
  | 'reply'
  | 'appeal'
  | 'written_statement'
  | 'consumer_complaint'
  | 'writ_petition'
  | 'other';

export type DraftStatus = 'draft' | 'generated' | 'reviewing' | 'approved' | 'rejected';

export interface DraftVerification {
  claimId: string;
  claim: string;
  status: 'verified' | 'partial' | 'unsupported' | 'contradicted' | 'pending';
  confidence: number;
  evidence?: string[];
  sources?: string[];
  reason?: string;
}

export interface Draft {
  id: string;
  title: string;
  draftType: DraftType;
  caseId?: string;
  caseName?: string;
  content: string;
  status: DraftStatus;
  agentUsed?: string;
  modelUsed?: string;
  verifications?: DraftVerification[];
  overallConfidence?: number;
  createdBy: string;
  approvedBy?: string;
  approvedAt?: string;
  createdAt: string;
  updatedAt: string;
}

// ── Research Types ───────────────────────────────────────────────────────────

export interface ResearchResult {
  id: string;
  caseTitle: string;
  citation: string;
  court: string;
  date: string;
  judges?: string[];
  summary?: string;
  relevantPassage: string;
  similarityScore: number;
  acts?: string[];
  sections?: string[];
  keywords?: string[];
  outcome?: string;
}

export interface ResearchSession {
  id: string;
  query: string;
  filters?: Record<string, string>;
  results: ResearchResult[];
  caseId?: string;
  createdAt: string;
  savedAt?: string;
}

// ── Hearing Types ────────────────────────────────────────────────────────────

export type HearingStatus = 'scheduled' | 'completed' | 'adjourned' | 'cancelled';

export interface Hearing {
  id: string;
  caseId: string;
  caseName: string;
  caseNumber: string;
  court: string;
  date: string;
  time: string;
  purpose: string;
  judge?: string;
  status: HearingStatus;
  notes?: string;
  outcome?: string;
  nextAction?: string;
  nextHearingDate?: string;
  createdAt: string;
}

// ── Task Types ───────────────────────────────────────────────────────────────

export type TaskStatus = 'todo' | 'in_progress' | 'waiting' | 'completed';
export type TaskPriority = 'critical' | 'high' | 'medium' | 'low';

export interface Task {
  id: string;
  title: string;
  description?: string;
  caseId?: string;
  caseName?: string;
  assigneeId: string;
  assigneeName: string;
  priority: TaskPriority;
  dueDate?: string;
  status: TaskStatus;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
}

// ── Timeline Types ───────────────────────────────────────────────────────────

export type TimelineEventType =
  | 'complaint'
  | 'filing'
  | 'notice'
  | 'reply'
  | 'evidence'
  | 'hearing'
  | 'order'
  | 'judgment'
  | 'appeal'
  | 'other';

export interface TimelineEvent {
  id: string;
  caseId: string;
  type: TimelineEventType;
  title: string;
  description?: string;
  date: string;
  documentId?: string;
  documentName?: string;
  source?: string;
  createdBy: string;
  createdAt: string;
}

// ── Agent & AI Types ─────────────────────────────────────────────────────────

export type AgentStatus = 'running' | 'completed' | 'queued' | 'waiting' | 'failed' | 'paused';

export interface Agent {
  id: string;
  name: string;
  description: string;
  type: 'intake' | 'research' | 'drafting' | 'verification' | 'review' | 'analysis';
  status: AgentStatus;
}

export interface AgentExecution {
  id: string;
  agentId: string;
  agentName: string;
  caseId?: string;
  input?: Record<string, unknown>;
  output?: Record<string, unknown>;
  status: AgentStatus;
  startedAt: string;
  completedAt?: string;
  durationMs?: number;
  sources?: string[];
  errors?: string[];
  confidence?: number;
}

export interface AIModel {
  id: string;
  name: string;
  purpose: string;
  version?: string;
  provider?: string;
  status: 'available' | 'unavailable' | 'coming_soon' | 'degraded';
  latencyMs?: number;
  usageCount?: number;
  lastUpdated?: string;
  description?: string;
}

// ── Client Types ─────────────────────────────────────────────────────────────

export interface Client {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  type: 'individual' | 'organization';
  organization?: string;
  address?: string;
  activeCases: number;
  totalCases: number;
  createdAt: string;
}

// ── Notification Types ───────────────────────────────────────────────────────

export type NotificationType =
  | 'hearing_approaching'
  | 'deadline_approaching'
  | 'document_processed'
  | 'draft_ready'
  | 'verification_warning'
  | 'task_assigned'
  | 'comment'
  | 'case_update'
  | 'system';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  caseId?: string;
  caseName?: string;
  isRead: boolean;
  createdAt: string;
  actionUrl?: string;
}

// ── Analytics Types ──────────────────────────────────────────────────────────

export interface AnalyticsOverview {
  activeCases: number;
  completedCases: number;
  researchRequests: number;
  draftsGenerated: number;
  documentsProcessed: number;
  avgProcessingTimeMs: number;
  verificationAlerts: number;
}

export interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
}

// ── API Response Types ───────────────────────────────────────────────────────

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface ApiError {
  code: number;
  message: string;
  details?: Record<string, string[]>;
}

// ── UI Types ─────────────────────────────────────────────────────────────────

export interface SelectOption {
  value: string;
  label: string;
  icon?: string;
  disabled?: boolean;
}

export type SortDirection = 'asc' | 'desc';

export interface SortConfig {
  field: string;
  direction: SortDirection;
}

export interface FilterConfig {
  field: string;
  value: string | string[];
  operator?: 'eq' | 'contains' | 'gte' | 'lte' | 'in';
}
