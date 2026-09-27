import React, { useState } from 'react';
import { Bot, Briefcase, FileText, Search, Send, Clock, Scale } from 'lucide-react';
import { Card, Badge, Breadcrumb, Button, ConfidenceBadge, AgentStatusBadge, Alert } from '@/design-system';
import { mockCases, mockDocuments, mockAgentExecutions } from '@/services/api/mockData';
import { formatDate } from '@/lib/utils';

// ── Agent Activity Page ───────────────────────────────────────────────────────

export function AgentActivityPage() {
  return (
    <div className="space-y-5 max-w-3xl">
      <div>
        <Breadcrumb items={[{ label: 'AI Workspace' }, { label: 'Agent Activity' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">Agent Activity</h1>
        <p className="text-sm text-ink-secondary">Real-time multi-agent workflow execution</p>
      </div>

      {/* Workflow header */}
      <Card className="border-primary-200 bg-primary-50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-[8px] bg-primary-100 flex items-center justify-center">
            <Briefcase className="w-5 h-5 text-primary-700" />
          </div>
          <div>
            <p className="font-semibold text-ink">State vs. Vikas Nair</p>
            <p className="text-sm text-ink-secondary">CRL.REV.P/2024/0089 · Bail Application Workflow</p>
          </div>
        </div>
      </Card>

      {/* Timeline */}
      <div className="relative">
        <div className="absolute left-5 top-0 bottom-0 w-px bg-border" />
        <div className="space-y-3 ml-12">
          {mockAgentExecutions.map((ex, idx) => (
            <div key={ex.id} className="relative">
              {/* Status indicator */}
              <div
                className={`absolute -left-9 w-4 h-4 rounded-full border-2 border-white flex items-center justify-center ${
                  ex.status === 'completed' ? 'bg-primary-400' :
                  ex.status === 'running' ? 'bg-blue-400 animate-pulse' :
                  ex.status === 'failed' ? 'bg-red-400' :
                  'bg-border'
                }`}
                style={{ top: '12px' }}
              >
                {ex.status === 'completed' && <span className="text-white text-[8px]">✓</span>}
              </div>

              <Card className={ex.status === 'running' ? 'border-blue-200 bg-blue-50' : ''}>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-semibold text-ink text-sm">{ex.agentName}</span>
                      <AgentStatusBadge status={ex.status} />
                    </div>

                    {ex.status === 'running' && (
                      <div className="flex items-center gap-1.5 text-xs text-blue-600 mb-2">
                        <div className="w-3 h-3 border-2 border-blue-400 border-t-transparent rounded-full animate-spin" />
                        Processing...
                      </div>
                    )}

                    {ex.output && (
                      <div className="text-xs text-ink-secondary space-y-0.5">
                        {Object.entries(ex.output).map(([k, v]) => (
                          <div key={k} className="flex items-center gap-1.5">
                            <span className="text-ink-muted">{k}:</span>
                            <span className="text-ink font-medium">{String(v)}</span>
                          </div>
                        ))}
                      </div>
                    )}

                    {ex.sources && ex.sources.length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1">
                        {ex.sources.map((s) => (
                          <Badge key={s} variant="success" size="sm">{s}</Badge>
                        ))}
                      </div>
                    )}
                  </div>

                  <div className="flex flex-col items-end gap-1 shrink-0 ml-3">
                    {ex.confidence && <ConfidenceBadge score={ex.confidence} />}
                    {ex.durationMs && (
                      <span className="text-xs text-ink-muted">
                        <Clock className="w-3 h-3 inline mr-0.5" />
                        {(ex.durationMs / 1000).toFixed(1)}s
                      </span>
                    )}
                  </div>
                </div>
              </Card>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── AI Workspace Page ─────────────────────────────────────────────────────────

interface AIMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  agent?: string;
  sources?: string[];
  confidence?: number;
  timestamp: Date;
}

export function AIWorkspacePage() {
  const [selectedCase, setSelectedCase] = useState(mockCases[0].id);
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<AIMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!query.trim()) return;
    const userMsg: AIMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: query,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setQuery('');
    setLoading(true);

    await new Promise((r) => setTimeout(r, 1800));

    const aiMsg: AIMessage = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: `Based on the case context for ${mockCases.find((c) => c.id === selectedCase)?.title}, here is my analysis:\n\nThe case involves ${mockCases.find((c) => c.id === selectedCase)?.description ?? 'the selected legal matter'}.\n\nBased on retrieved precedents, particularly Satender Kumar Antil vs CBI (2022 SCC OnLine SC 825), the court's approach to bail in similar matters suggests a liberal approach where the accused has no prior criminal antecedents.\n\nKey considerations:\n1. Duration of custody\n2. Nature of allegations\n3. Risk of flight or tampering\n\nThis analysis is grounded in retrieved legal precedents and should be verified against current case facts.`,
      agent: 'Research + Analysis Agent',
      sources: ['Satender Kumar Antil (2022)', 'Arnesh Kumar (2014)', 'Case documents'],
      confidence: 0.84,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, aiMsg]);
    setLoading(false);
  };

  const suggestions = [
    'Summarize this case',
    'Find relevant precedents for bail application',
    'Identify contradictions in the evidence',
    'Draft a summary of arguments',
    'What documents are missing?',
  ];

  return (
    <div className="space-y-4 max-w-4xl">
      <div>
        <Breadcrumb items={[{ label: 'AI Workspace' }, { label: 'AI Assistant' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">AI Workspace</h1>
        <p className="text-sm text-ink-secondary">Contextual AI assistance grounded in your case data</p>
      </div>

      <Alert variant="info">
        <p className="font-medium">This is not a generic chatbot</p>
        <p>All AI responses are grounded in your case documents, selected precedents, and retrieved legal evidence.</p>
      </Alert>

      {/* Context selectors */}
      <Card padding="sm">
        <div className="flex flex-wrap gap-3 items-center">
          <div className="flex items-center gap-2 text-sm font-medium text-ink">
            <Briefcase className="w-4 h-4 text-primary-700" />
            Context:
          </div>
          <select
            value={selectedCase}
            onChange={(e) => setSelectedCase(e.target.value)}
            className="h-8 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400"
            aria-label="Select case context"
          >
            {mockCases.map((c) => (
              <option key={c.id} value={c.id}>{c.title}</option>
            ))}
          </select>
          <Badge variant="success" size="sm">
            <Scale className="w-3 h-3 inline mr-1" />
            {mockDocuments.filter((d) => d.caseId === selectedCase).length} documents
          </Badge>
        </div>
      </Card>

      {/* Message thread */}
      <div className="min-h-[300px] space-y-4">
        {messages.length === 0 && (
          <Card className="text-center py-10">
            <Bot className="w-10 h-10 text-border-strong mx-auto mb-3" />
            <h3 className="font-semibold text-ink">Ask anything about this case</h3>
            <p className="text-sm text-ink-secondary mt-1 mb-4">
              AI responses are grounded in case documents and legal precedents
            </p>
            <div className="flex flex-wrap gap-2 justify-center max-w-lg mx-auto">
              {suggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => setQuery(s)}
                  className="px-3 py-1.5 text-xs border border-border rounded-full hover:border-primary-400 hover:bg-primary-50 transition-colors text-ink-secondary hover:text-primary-700"
                >
                  {s}
                </button>
              ))}
            </div>
          </Card>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-2xl ${msg.role === 'user' ? 'order-2' : ''}`}>
              {msg.role === 'assistant' && (
                <div className="flex items-center gap-1.5 mb-1.5">
                  <div className="w-5 h-5 rounded-full bg-primary-100 flex items-center justify-center">
                    <Bot className="w-3 h-3 text-primary-700" />
                  </div>
                  <span className="text-xs text-ink-secondary">{msg.agent}</span>
                  {msg.confidence && <ConfidenceBadge score={msg.confidence} />}
                </div>
              )}
              <div
                className={`px-4 py-3 rounded-[10px] text-sm leading-relaxed whitespace-pre-line ${
                  msg.role === 'user'
                    ? 'bg-primary-700 text-white'
                    : 'bg-surface-raised border border-border text-ink'
                }`}
              >
                {msg.content}
              </div>
              {msg.sources && (
                <div className="flex flex-wrap gap-1.5 mt-2">
                  <span className="text-xs text-ink-muted">Sources:</span>
                  {msg.sources.map((s) => (
                    <Badge key={s} variant="success" size="sm">{s}</Badge>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2 text-sm text-ink-secondary">
            <div className="w-4 h-4 border-2 border-border border-t-primary-400 rounded-full animate-spin" />
            AI is analyzing case context and retrieving precedents...
          </div>
        )}
      </div>

      {/* Input */}
      <div className="flex gap-2 items-end">
        <div className="flex-1 relative">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Ask about this case... (Shift+Enter for new line)"
            rows={2}
            className="w-full px-4 py-3 text-sm border border-border rounded-[10px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent resize-none"
            aria-label="AI query input"
          />
        </div>
        <Button
          onClick={handleSend}
          disabled={!query.trim() || loading}
          loading={loading}
          leftIcon={<Send className="w-4 h-4" />}
        >
          Send
        </Button>
      </div>
    </div>
  );
}
