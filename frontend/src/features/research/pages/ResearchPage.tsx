import React, { useState } from 'react';
import { Search, Filter, BookOpen, Scale, ExternalLink, BookmarkPlus, FileEdit, ArrowRight } from 'lucide-react';
import { Card, Badge, Breadcrumb, Button, EmptyState, Skeleton } from '@/design-system';
import { formatDate, truncate } from '@/lib/utils';
import { ROUTES } from '@/constants';
import { mockResearchResults } from '@/services/api/mockData';

// ── Similarity Score Bar ──────────────────────────────────────────────────────

function SimilarityBar({ score }: { score: number }) {
  const pct = Math.round(score * 100);
  const color = score >= 0.8 ? '#1f6b45' : score >= 0.6 ? '#f4a261' : '#e76f51';
  return (
    <div className="flex items-center gap-2 text-xs">
      <div className="flex-1 h-1.5 bg-primary-100 rounded-full overflow-hidden w-16">
        <div className="h-full rounded-full" style={{ width: `${pct}%`, background: color }} />
      </div>
      <span className="font-medium" style={{ color }}>{pct}% match</span>
    </div>
  );
}

// ── Research Result Card ──────────────────────────────────────────────────────

function ResearchResultCard({ result, onOpen }: { result: typeof mockResearchResults[0]; onOpen: () => void }) {
  return (
    <Card hoverable className="cursor-pointer" onClick={onOpen}>
      <div className="flex items-start gap-3">
        <div className="w-9 h-9 rounded-[8px] bg-primary-100 flex items-center justify-center shrink-0">
          <Scale className="w-4 h-4 text-primary-700" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h3 className="font-semibold text-ink leading-snug">{result.caseTitle}</h3>
              <p className="text-xs text-ink-secondary mt-0.5">
                {result.citation} · {result.court} · {formatDate(result.date)}
              </p>
            </div>
            <SimilarityBar score={result.similarityScore} />
          </div>

          {result.summary && (
            <p className="text-sm text-ink-secondary mt-2 leading-relaxed">
              {truncate(result.summary, 180)}
            </p>
          )}

          {/* Relevant passage */}
          <blockquote className="mt-3 pl-3 border-l-2 border-primary-400 text-sm text-ink italic leading-relaxed">
            "{truncate(result.relevantPassage, 200)}"
          </blockquote>

          {/* Tags */}
          <div className="flex items-center gap-2 mt-3 flex-wrap">
            {result.sections?.map((s) => (
              <Badge key={s} variant="success" size="sm">{s}</Badge>
            ))}
            {result.acts?.map((a) => (
              <Badge key={a} variant="neutral" size="sm">{a}</Badge>
            ))}
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2 mt-3">
            <Button size="xs" variant="ghost" leftIcon={<ExternalLink className="w-3 h-3" />} onClick={(e) => e.stopPropagation()}>
              Open
            </Button>
            <Button size="xs" variant="ghost" leftIcon={<BookmarkPlus className="w-3 h-3" />} onClick={(e) => e.stopPropagation()}>
              Save
            </Button>
            <Button size="xs" variant="ghost" leftIcon={<FileEdit className="w-3 h-3" />} onClick={(e) => e.stopPropagation()}>
              Add to Draft
            </Button>
          </div>
        </div>
      </div>
    </Card>
  );
}

// ── Research Page ─────────────────────────────────────────────────────────────

export function ResearchPage() {
  const [query, setQuery] = useState('');
  const [searching, setSearching] = useState(false);
  const [results, setResults] = useState(mockResearchResults);
  const [hasSearched, setHasSearched] = useState(false);
  const [selectedResult, setSelectedResult] = useState<typeof mockResearchResults[0] | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setSearching(true);
    setHasSearched(false);
    await new Promise((r) => setTimeout(r, 1200));
    setResults(mockResearchResults);
    setHasSearched(true);
    setSearching(false);
  };

  return (
    <div className="space-y-5">
      <div>
        <Breadcrumb items={[{ label: 'Workspace' }, { label: 'Research' }]} />
        <h1 className="text-2xl font-bold text-ink mt-1">Legal Research</h1>
        <p className="text-sm text-ink-secondary">
          Search across 14,544 indexed Indian legal precedents using semantic AI retrieval
        </p>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch}>
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-ink-secondary pointer-events-none" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder='e.g. "bail application first time offender criminal revision petition"'
            className="w-full h-12 pl-12 pr-32 text-sm border border-border rounded-[10px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent shadow-sm"
          />
          <Button
            type="submit"
            loading={searching}
            className="absolute right-2 top-1/2 -translate-y-1/2"
            size="sm"
          >
            Search
          </Button>
        </div>

        {/* Example queries */}
        <div className="flex flex-wrap gap-2 mt-2">
          <span className="text-xs text-ink-secondary">Try:</span>
          {[
            'tenant eviction without notice',
            'anticipatory bail anticipation of arrest',
            'consumer forum delay in possession',
          ].map((q) => (
            <button
              key={q}
              type="button"
              onClick={() => setQuery(q)}
              className="text-xs text-primary-700 hover:underline"
            >
              "{q}"
            </button>
          ))}
        </div>
      </form>

      {/* Filters */}
      <Card padding="sm">
        <div className="flex flex-wrap gap-3">
          <select className="h-8 px-3 text-xs border border-border rounded-[6px] bg-surface-raised" aria-label="Filter by court">
            <option value="">All Courts</option>
            <option>Supreme Court</option>
            <option>High Court</option>
            <option>District Court</option>
          </select>
          <select className="h-8 px-3 text-xs border border-border rounded-[6px] bg-surface-raised" aria-label="Filter by year">
            <option value="">All Years</option>
            <option>2024</option><option>2023</option><option>2022</option><option>2021</option><option>2020</option>
            <option>Before 2020</option>
          </select>
          <select className="h-8 px-3 text-xs border border-border rounded-[6px] bg-surface-raised" aria-label="Filter by act">
            <option value="">All Acts</option>
            <option>IPC</option><option>CrPC</option><option>CPC</option>
            <option>Constitution of India</option>
            <option>Consumer Protection Act</option>
          </select>
        </div>
      </Card>

      {/* Loading state */}
      {searching && (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Card key={i}>
              <div className="space-y-2">
                <div className="h-4 bg-primary-100 rounded animate-pulse w-2/3" />
                <div className="h-3 bg-surface-overlay rounded animate-pulse w-full" />
                <div className="h-3 bg-surface-overlay rounded animate-pulse w-5/6" />
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Results */}
      {!searching && hasSearched && (
        <div>
          <p className="text-sm text-ink-secondary mb-3">
            Found <strong className="text-ink">{results.length}</strong> relevant judgments for "{query}"
          </p>
          <div className="space-y-3">
            {results.map((r) => (
              <ResearchResultCard
                key={r.id}
                result={r}
                onOpen={() => setSelectedResult(r)}
              />
            ))}
          </div>
        </div>
      )}

      {/* Initial state */}
      {!searching && !hasSearched && (
        <Card className="text-center py-12">
          <BookOpen className="w-12 h-12 mx-auto mb-3 text-border-strong" />
          <h3 className="font-semibold text-ink">Search Indian Legal Precedents</h3>
          <p className="text-sm text-ink-secondary mt-1 max-w-sm mx-auto">
            Using semantic search powered by bge-small embeddings across 14,544 indexed legal chunks.
          </p>
        </Card>
      )}

      {/* Result Detail Modal */}
      {selectedResult && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/30" onClick={() => setSelectedResult(null)} />
          <div className="relative bg-surface-raised rounded-[12px] shadow-xl max-w-2xl w-full max-h-[85vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="text-lg font-bold text-ink">{selectedResult.caseTitle}</h2>
                  <p className="text-sm text-ink-secondary mt-0.5">{selectedResult.citation} · {selectedResult.court}</p>
                </div>
                <button onClick={() => setSelectedResult(null)} className="p-1 text-ink-secondary hover:text-ink">✕</button>
              </div>

              <div className="space-y-4">
                {selectedResult.summary && (
                  <div>
                    <h4 className="text-sm font-semibold text-ink mb-1">Summary</h4>
                    <p className="text-sm text-ink-secondary leading-relaxed">{selectedResult.summary}</p>
                  </div>
                )}
                <div>
                  <h4 className="text-sm font-semibold text-ink mb-1">Relevant Passage</h4>
                  <blockquote className="pl-3 border-l-2 border-primary-400 text-sm text-ink italic leading-relaxed">
                    "{selectedResult.relevantPassage}"
                  </blockquote>
                </div>
                <div className="flex flex-wrap gap-2">
                  {selectedResult.sections?.map((s) => <Badge key={s} variant="success" size="sm">{s}</Badge>)}
                  {selectedResult.acts?.map((a) => <Badge key={a} variant="neutral" size="sm">{a}</Badge>)}
                </div>
                <div className="flex gap-2">
                  <Button variant="primary" size="sm" leftIcon={<FileEdit className="w-3.5 h-3.5" />}>
                    Add to Draft
                  </Button>
                  <Button variant="secondary" size="sm" leftIcon={<BookmarkPlus className="w-3.5 h-3.5" />}>
                    Save to Case
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
