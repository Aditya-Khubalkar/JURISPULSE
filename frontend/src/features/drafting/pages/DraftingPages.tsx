import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileEdit, Plus, Download, CheckCircle, X, RotateCcw, Loader2, Wand2, ShieldCheck } from 'lucide-react';
import {
  Card, StatusBadge, Badge, EmptyState, Breadcrumb, Button,
  VerificationBadge, ConfidenceBadge, Alert,
} from '@/design-system';
import { formatDate, truncate } from '@/lib/utils';
import { ROUTES, DRAFT_TYPE_LABELS } from '@/constants';
import { mockDrafts, mockCases } from '@/services/api/mockData';

// ── Drafts List ───────────────────────────────────────────────────────────────

export function DraftsListPage() {
  const navigate = useNavigate();

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <Breadcrumb items={[{ label: 'Workspace' }, { label: 'Drafts' }]} />
          <h1 className="text-2xl font-bold text-ink mt-1">Drafts</h1>
          <p className="text-sm text-ink-secondary">{mockDrafts.length} drafts</p>
        </div>
        <Button variant="primary" leftIcon={<Plus className="w-4 h-4" />} onClick={() => navigate(ROUTES.DRAFT_NEW)}>
          New Draft
        </Button>
      </div>

      <div className="space-y-3">
        {mockDrafts.map((d) => (
          <Card key={d.id} hoverable clickable onClick={() => navigate(ROUTES.DRAFT_DETAIL(d.id))}>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-[8px] bg-purple-50 flex items-center justify-center shrink-0">
                <FileEdit className="w-5 h-5 text-purple-500" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-ink">{d.title}</p>
                <div className="flex items-center gap-2 mt-0.5 flex-wrap">
                  <Badge variant="neutral" size="sm">{DRAFT_TYPE_LABELS[d.draftType] ?? d.draftType}</Badge>
                  {d.caseName && <span className="text-xs text-ink-secondary">{d.caseName}</span>}
                  <span className="text-xs text-ink-muted">{formatDate(d.updatedAt)}</span>
                </div>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                {d.overallConfidence && <ConfidenceBadge score={d.overallConfidence} />}
                <StatusBadge status={d.status} />
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// ── Draft New Page ────────────────────────────────────────────────────────────

export function DraftNewPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState<'select' | 'generating' | 'workspace'>('select');
  const [draftType, setDraftType] = useState('');
  const [caseId, setCaseId] = useState('');

  const handleGenerate = async () => {
    if (!draftType) return;
    setStep('generating');
    await new Promise((r) => setTimeout(r, 3000));
    navigate(ROUTES.DRAFT_DETAIL('dr1'));
  };

  return (
    <div className="max-w-lg">
      <Breadcrumb
        items={[
          { label: 'Drafts', onClick: () => navigate(ROUTES.DRAFTS) },
          { label: 'New Draft' },
        ]}
        className="mb-4"
      />
      <h1 className="text-2xl font-bold text-ink mb-6">Create Draft</h1>

      {step === 'generating' ? (
        <Card className="text-center py-12">
          <Loader2 className="w-10 h-10 text-primary-400 mx-auto mb-4 animate-spin" />
          <h3 className="font-semibold text-ink">Generating Draft...</h3>
          <p className="text-sm text-ink-secondary mt-1">
            Llama 3.1 Legal Drafter is generating your document.
          </p>
          <div className="mt-4 space-y-1.5 text-xs text-ink-secondary">
            {['Retrieving case context...', 'Finding relevant precedents...', 'Generating document content...'].map((s, i) => (
              <div key={i} className="flex items-center justify-center gap-1.5">
                <CheckCircle className="w-3 h-3 text-primary-400" />
                {s}
              </div>
            ))}
          </div>
        </Card>
      ) : (
        <Card>
          <div className="space-y-4">
            <Alert variant="info">
              <p className="font-medium">AI Drafting powered by Llama 3.1 Legal Drafter</p>
              <p>The model will generate a draft based on your case context and retrieved precedents.</p>
            </Alert>

            <div>
              <label htmlFor="draft-type" className="block text-sm font-medium text-ink mb-1">
                Document Type <span className="text-red-500">*</span>
              </label>
              <select
                id="draft-type"
                value={draftType}
                onChange={(e) => setDraftType(e.target.value)}
                className="w-full h-9 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
              >
                <option value="">Select document type</option>
                {Object.entries(DRAFT_TYPE_LABELS).map(([v, l]) => (
                  <option key={v} value={v}>{l}</option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="draft-case" className="block text-sm font-medium text-ink mb-1">
                Related Case
              </label>
              <select
                id="draft-case"
                value={caseId}
                onChange={(e) => setCaseId(e.target.value)}
                className="w-full h-9 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
              >
                <option value="">Select case (optional)</option>
                {mockCases.map((c) => (
                  <option key={c.id} value={c.id}>{c.title}</option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="draft-instructions" className="block text-sm font-medium text-ink mb-1">
                Instructions (optional)
              </label>
              <textarea
                id="draft-instructions"
                rows={3}
                placeholder="e.g. Emphasize the applicant's clean criminal record and employment status..."
                className="w-full px-3 py-2 text-sm border border-border rounded-[6px] resize-none focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
              />
            </div>

            <div className="flex gap-3 pt-2">
              <Button variant="secondary" onClick={() => navigate(ROUTES.DRAFTS)}>
                Cancel
              </Button>
              <Button
                onClick={handleGenerate}
                disabled={!draftType}
                leftIcon={<Wand2 className="w-4 h-4" />}
              >
                Generate Draft
              </Button>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}

// ── Draft Detail / Workspace ──────────────────────────────────────────────────

export function DraftDetailPage() {
  const navigate = useNavigate();
  const draft = mockDrafts[0];
  const [content, setContent] = useState(draft.content);
  const [approving, setApproving] = useState(false);

  const handleApprove = async () => {
    setApproving(true);
    await new Promise((r) => setTimeout(r, 1000));
    setApproving(false);
    navigate(ROUTES.DRAFTS);
  };

  return (
    <div className="space-y-4">
      <Breadcrumb
        items={[
          { label: 'Drafts', onClick: () => navigate(ROUTES.DRAFTS) },
          { label: draft.title },
        ]}
      />

      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-xl font-bold text-ink">{draft.title}</h1>
          <div className="flex items-center gap-2 mt-1">
            <StatusBadge status={draft.status} />
            <Badge variant="neutral" size="sm">{DRAFT_TYPE_LABELS[draft.draftType]}</Badge>
            {draft.modelUsed && <Badge variant="info" size="sm">{draft.modelUsed}</Badge>}
            {draft.overallConfidence && <ConfidenceBadge score={draft.overallConfidence} />}
          </div>
        </div>
        <div className="flex gap-2">
          <Button size="sm" variant="secondary" leftIcon={<Download className="w-3.5 h-3.5" />}>
            Export
          </Button>
          <Button size="sm" variant="danger" leftIcon={<X className="w-3.5 h-3.5" />}>
            Reject
          </Button>
          <Button size="sm" variant="warning" leftIcon={<RotateCcw className="w-3.5 h-3.5" />}>
            Request Changes
          </Button>
          <Button
            size="sm"
            variant="primary"
            leftIcon={<CheckCircle className="w-3.5 h-3.5" />}
            loading={approving}
            onClick={handleApprove}
          >
            Approve
          </Button>
        </div>
      </div>

      {/* Human approval notice */}
      <Alert variant="info">
        <p className="font-medium">Human Review Required</p>
        <p>This draft was generated by {draft.agentUsed}. Please review all claims before approving.</p>
      </Alert>

      {/* Workspace: Editor + Verification Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Editor */}
        <div className="lg:col-span-2">
          <Card padding="none">
            <div className="flex items-center gap-2 px-4 py-2.5 border-b border-border">
              <FileEdit className="w-4 h-4 text-ink-secondary" />
              <span className="text-sm font-medium text-ink">Draft Editor</span>
              <span className="ml-auto text-xs text-ink-muted">Auto-saved</span>
            </div>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="w-full min-h-[500px] p-6 text-sm font-mono text-ink leading-relaxed focus:outline-none resize-none"
              aria-label="Draft content editor"
            />
          </Card>
        </div>

        {/* Verification Panel */}
        <div className="space-y-4">
          <Card>
            <div className="flex items-center gap-2 mb-3">
              <ShieldCheck className="w-4 h-4 text-primary-700" />
              <h3 className="font-semibold text-ink text-sm">Verification Status</h3>
            </div>

            {draft.verifications?.map((v) => (
              <div key={v.claimId} className="mb-3 p-3 bg-surface rounded-[8px]">
                <div className="flex items-center justify-between mb-1.5">
                  <VerificationBadge status={v.status} />
                  <span className="text-xs text-ink-secondary">{Math.round(v.confidence * 100)}%</span>
                </div>
                <p className="text-xs text-ink leading-relaxed">{v.claim}</p>
                {v.reason && (
                  <p className="text-xs text-amber-600 mt-1">{v.reason}</p>
                )}
                {v.sources && (
                  <div className="mt-1.5 flex flex-wrap gap-1">
                    {v.sources.map((s) => (
                      <Badge key={s} variant="neutral" size="sm">{s}</Badge>
                    ))}
                  </div>
                )}
              </div>
            ))}

            {!draft.verifications?.length && (
              <div className="text-center py-4 text-sm text-ink-secondary">
                <div className="w-6 h-6 border-2 border-border border-t-primary-400 rounded-full animate-spin mx-auto mb-2" />
                Verification in progress...
              </div>
            )}
          </Card>

          {/* AI Actions */}
          <Card>
            <h3 className="font-semibold text-ink text-sm mb-3">AI Actions</h3>
            <div className="space-y-2">
              {['Improve Draft', 'Shorten', 'Expand', 'Add Citations', 'Rewrite Formal'].map((action) => (
                <button
                  key={action}
                  className="w-full text-left px-3 py-2 text-sm text-ink hover:bg-primary-100 rounded-[6px] transition-colors flex items-center gap-2"
                >
                  <Wand2 className="w-3.5 h-3.5 text-ink-secondary" />
                  {action}
                </button>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
