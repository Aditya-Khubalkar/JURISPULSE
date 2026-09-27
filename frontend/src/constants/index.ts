// ── Route Constants ──────────────────────────────────────────────────────────

export const ROUTES = {
  // Public
  LANDING: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  FORGOT_PASSWORD: '/forgot-password',
  RESET_PASSWORD: '/reset-password',
  VERIFY_EMAIL: '/verify-email',

  // App
  DASHBOARD: '/dashboard',

  // Cases
  CASES: '/cases',
  CASE_NEW: '/cases/new',
  CASE_DETAIL: (id: string = ':caseId') => `/cases/${id}`,
  CASE_EDIT: (id: string = ':caseId') => `/cases/${id}/edit`,
  CASE_DOCUMENTS: (id: string = ':caseId') => `/cases/${id}/documents`,
  CASE_HEARINGS: (id: string = ':caseId') => `/cases/${id}/hearings`,
  CASE_TIMELINE: (id: string = ':caseId') => `/cases/${id}/timeline`,

  // Documents
  DOCUMENTS: '/documents',
  DOCUMENT_DETAIL: (id: string = ':documentId') => `/documents/${id}`,

  // Research
  RESEARCH: '/research',
  RESEARCH_RESULT: (id: string = ':resultId') => `/research/${id}`,

  // Drafts
  DRAFTS: '/drafts',
  DRAFT_NEW: '/drafts/new',
  DRAFT_DETAIL: (id: string = ':draftId') => `/drafts/${id}`,

  // Evidence
  EVIDENCE: '/evidence',

  // Timeline
  TIMELINE: '/timeline',

  // Hearings
  HEARINGS: '/hearings',

  // Calendar
  CALENDAR: '/calendar',

  // Tasks
  TASKS: '/tasks',

  // AI Workspace
  AI_WORKSPACE: '/ai',

  // Agents
  AGENTS_ACTIVITY: '/agents/activity',

  // Verification
  VERIFICATION: '/verification',

  // Collaboration
  CLIENTS: '/clients',
  CLIENT_DETAIL: (id: string = ':clientId') => `/clients/${id}`,
  TEAM: '/team',
  COLLABORATION: '/collaboration',

  // Insights
  ANALYTICS: '/analytics',
  REPORTS: '/reports',

  // Admin
  ADMIN: '/admin',
  ADMIN_USERS: '/admin/users',
  ADMIN_ROLES: '/admin/roles',
  ADMIN_CASES: '/admin/cases',
  ADMIN_DOCUMENTS: '/admin/documents',
  ADMIN_AGENTS: '/admin/agents',
  ADMIN_MODELS: '/admin/models',
  ADMIN_DATASETS: '/admin/datasets',
  ADMIN_PROMPTS: '/admin/prompts',
  ADMIN_AUDIT_LOGS: '/admin/audit-logs',
  ADMIN_SYSTEM_HEALTH: '/admin/system-health',
  ADMIN_SETTINGS: '/admin/settings',

  // Settings
  SETTINGS: '/settings',
  SETTINGS_PROFILE: '/settings/profile',
  SETTINGS_ORGANIZATION: '/settings/organization',
  SETTINGS_NOTIFICATIONS: '/settings/notifications',
  SETTINGS_SECURITY: '/settings/security',
  SETTINGS_APPEARANCE: '/settings/appearance',

  // Notifications
  NOTIFICATIONS: '/notifications',
} as const;

// ── Case Constants ────────────────────────────────────────────────────────────

export const CASE_STATUS_LABELS: Record<string, string> = {
  active: 'Active',
  pending: 'Pending',
  closed: 'Closed',
  stayed: 'Stayed',
  disposed: 'Disposed',
  appeal: 'In Appeal',
};

export const CASE_TYPE_LABELS: Record<string, string> = {
  civil: 'Civil',
  criminal: 'Criminal',
  family: 'Family',
  labour: 'Labour',
  consumer: 'Consumer',
  constitutional: 'Constitutional',
  corporate: 'Corporate',
  property: 'Property',
  tax: 'Tax',
  writ: 'Writ',
  other: 'Other',
};

export const PRIORITY_LABELS: Record<string, string> = {
  critical: 'Critical',
  high: 'High',
  medium: 'Medium',
  low: 'Low',
};

export const COURTS = [
  'Supreme Court of India',
  'Delhi High Court',
  'Bombay High Court',
  'Calcutta High Court',
  'Madras High Court',
  'Allahabad High Court',
  'Rajasthan High Court',
  'Gujarat High Court',
  'Kerala High Court',
  'Karnataka High Court',
  'Andhra Pradesh High Court',
  'Telangana High Court',
  'Patna High Court',
  'Orissa High Court',
  'Punjab and Haryana High Court',
  'Gauhati High Court',
  'Himachal Pradesh High Court',
  'Jammu and Kashmir High Court',
  'Jharkhand High Court',
  'Madhya Pradesh High Court',
  'Chhattisgarh High Court',
  'Uttarakhand High Court',
  'District Court',
  'Sessions Court',
  'Magistrate Court',
  'Consumer Forum',
  'Labour Court',
  'Family Court',
  'Other',
];

// ── Document Constants ────────────────────────────────────────────────────────

export const DOCUMENT_STATUS_LABELS: Record<string, string> = {
  uploaded: 'Uploaded',
  processing: 'Processing',
  processed: 'Processed',
  needs_review: 'Needs Review',
  verified: 'Verified',
  failed: 'Failed',
};

export const DOCUMENT_TYPE_LABELS: Record<string, string> = {
  petition: 'Petition',
  affidavit: 'Affidavit',
  notice: 'Legal Notice',
  order: 'Court Order',
  judgment: 'Judgment',
  evidence: 'Evidence',
  reply: 'Reply',
  written_statement: 'Written Statement',
  bail_application: 'Bail Application',
  appeal: 'Appeal',
  complaint: 'Complaint',
  contract: 'Contract',
  other: 'Other',
};

// ── Draft Constants ───────────────────────────────────────────────────────────

export const DRAFT_TYPE_LABELS: Record<string, string> = {
  petition: 'Petition',
  affidavit: 'Affidavit',
  legal_notice: 'Legal Notice',
  bail_application: 'Bail Application',
  reply: 'Reply',
  appeal: 'Appeal',
  written_statement: 'Written Statement',
  consumer_complaint: 'Consumer Complaint',
  writ_petition: 'Writ Petition',
  other: 'Other',
};

// ── Verification Constants ────────────────────────────────────────────────────

export const VERIFICATION_STATUS_LABELS: Record<string, string> = {
  verified: 'Verified',
  partial: 'Partially Supported',
  unsupported: 'Unsupported',
  contradicted: 'Contradicted',
  pending: 'Pending Verification',
};

// ── Task Constants ────────────────────────────────────────────────────────────

export const TASK_STATUS_LABELS: Record<string, string> = {
  todo: 'To Do',
  in_progress: 'In Progress',
  waiting: 'Waiting',
  completed: 'Completed',
};

// ── Agent Constants ───────────────────────────────────────────────────────────

export const AGENT_STATUS_LABELS: Record<string, string> = {
  running: 'Running',
  completed: 'Completed',
  queued: 'Queued',
  waiting: 'Waiting',
  failed: 'Failed',
  paused: 'Paused',
};

// ── Pagination ────────────────────────────────────────────────────────────────

export const DEFAULT_PAGE_SIZE = 20;
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];

// ── File Upload ───────────────────────────────────────────────────────────────

export const ALLOWED_FILE_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/msword',
  'text/plain',
  'image/png',
  'image/jpeg',
  'image/jpg',
];

export const ALLOWED_FILE_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt', '.png', '.jpg', '.jpeg'];

export const MAX_FILE_SIZE_MB = 50;
export const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

// ── AI Model Registry ─────────────────────────────────────────────────────────

export const KNOWN_AI_MODELS = [
  {
    id: 'llama-3-1-legal',
    name: 'Llama 3.1 Legal Drafter',
    purpose: 'Legal document drafting',
    version: '3.1',
    status: 'available' as const,
    description: 'Fine-tuned with LoRA/Unsloth for generating petitions, affidavits, notices, bail applications and similar legal documents.',
  },
  {
    id: 'bge-small',
    name: 'bge-small (Retrieval)',
    purpose: 'Semantic legal retrieval',
    version: 'v1.5',
    status: 'available' as const,
    description: 'Pre-trained embedding model for semantic search across 14,544 indexed legal chunks.',
  },
  {
    id: 'hallucination-classifier',
    name: 'Hallucination Classifier',
    purpose: 'Fact-check & verification',
    status: 'coming_soon' as const,
    description: 'Will verify generated claims against retrieved evidence using the legal retrieval database.',
  },
];
