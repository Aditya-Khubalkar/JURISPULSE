import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Briefcase, FileText, FileEdit, Calendar, CheckSquare, Bot, X, ArrowRight } from 'lucide-react';
import { createPortal } from 'react-dom';
import { cn } from '@/lib/utils';
import { useUIStore } from '@/store/uiStore';
import { ROUTES } from '@/constants';
import { mockCases, mockDocuments, mockDrafts } from '@/services/api/mockData';

interface CommandItem {
  id: string;
  label: string;
  description?: string;
  icon: React.ReactNode;
  action: () => void;
  category: string;
}

export function CommandPalette() {
  const { commandPaletteOpen, setCommandPaletteOpen } = useUIStore();
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const go = useCallback(
    (route: string) => {
      navigate(route);
      setCommandPaletteOpen(false);
      setQuery('');
    },
    [navigate, setCommandPaletteOpen]
  );

  // Static items
  const staticItems: CommandItem[] = [
    { id: 'nav-dashboard', label: 'Dashboard', icon: <Search className="w-4 h-4" />, action: () => go(ROUTES.DASHBOARD), category: 'Navigation' },
    { id: 'nav-cases', label: 'All Cases', icon: <Briefcase className="w-4 h-4" />, action: () => go(ROUTES.CASES), category: 'Navigation' },
    { id: 'nav-docs', label: 'Documents', icon: <FileText className="w-4 h-4" />, action: () => go(ROUTES.DOCUMENTS), category: 'Navigation' },
    { id: 'nav-research', label: 'Legal Research', icon: <Search className="w-4 h-4" />, action: () => go(ROUTES.RESEARCH), category: 'Navigation' },
    { id: 'nav-drafts', label: 'Drafts', icon: <FileEdit className="w-4 h-4" />, action: () => go(ROUTES.DRAFTS), category: 'Navigation' },
    { id: 'nav-hearings', label: 'Hearings', icon: <Calendar className="w-4 h-4" />, action: () => go(ROUTES.HEARINGS), category: 'Navigation' },
    { id: 'nav-tasks', label: 'Tasks', icon: <CheckSquare className="w-4 h-4" />, action: () => go(ROUTES.TASKS), category: 'Navigation' },
    { id: 'nav-ai', label: 'AI Workspace', icon: <Bot className="w-4 h-4" />, action: () => go(ROUTES.AI_WORKSPACE), category: 'Navigation' },
    { id: 'action-new-case', label: 'New Case', description: 'Create a new case', icon: <Briefcase className="w-4 h-4" />, action: () => go(ROUTES.CASE_NEW), category: 'Quick Actions' },
    { id: 'action-new-draft', label: 'New Draft', description: 'Create a new draft document', icon: <FileEdit className="w-4 h-4" />, action: () => go(ROUTES.DRAFT_NEW), category: 'Quick Actions' },
  ];

  // Dynamic case items
  const caseItems: CommandItem[] = mockCases.map((c) => ({
    id: `case-${c.id}`,
    label: c.title,
    description: `${c.caseNumber} · ${c.court}`,
    icon: <Briefcase className="w-4 h-4" />,
    action: () => go(ROUTES.CASE_DETAIL(c.id)),
    category: 'Cases',
  }));

  const docItems: CommandItem[] = mockDocuments.slice(0, 5).map((d) => ({
    id: `doc-${d.id}`,
    label: d.title,
    description: d.caseName,
    icon: <FileText className="w-4 h-4" />,
    action: () => go(ROUTES.DOCUMENTS),
    category: 'Documents',
  }));

  const allItems = [...staticItems, ...caseItems, ...docItems];

  const filtered = query.trim()
    ? allItems.filter(
        (item) =>
          item.label.toLowerCase().includes(query.toLowerCase()) ||
          item.description?.toLowerCase().includes(query.toLowerCase())
      )
    : staticItems;

  const grouped = filtered.reduce<Record<string, CommandItem[]>>((acc, item) => {
    if (!acc[item.category]) acc[item.category] = [];
    acc[item.category].push(item);
    return acc;
  }, {});

  useEffect(() => {
    if (commandPaletteOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setSelected(0);
    } else {
      setQuery('');
    }
  }, [commandPaletteOpen]);

  useEffect(() => {
    setSelected(0);
  }, [query]);

  const flatItems = Object.values(grouped).flat();

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelected((s) => Math.min(s + 1, flatItems.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelected((s) => Math.max(s - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      flatItems[selected]?.action();
    } else if (e.key === 'Escape') {
      setCommandPaletteOpen(false);
    }
  };

  if (!commandPaletteOpen) return null;

  return createPortal(
    <div className="fixed inset-0 z-[60] flex items-start justify-center pt-[15vh] px-4">
      <div
        className="absolute inset-0 bg-black/30 backdrop-blur-[2px]"
        onClick={() => setCommandPaletteOpen(false)}
      />
      <div className="relative w-full max-w-lg bg-surface-raised rounded-[12px] shadow-xl border border-border overflow-hidden">
        {/* Search Input */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-border">
          <Search className="w-4 h-4 text-ink-secondary shrink-0" />
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search cases, documents, pages..."
            className="flex-1 text-sm text-ink placeholder:text-ink-muted focus:outline-none bg-transparent"
            aria-label="Command palette search"
          />
          {query && (
            <button
              onClick={() => setQuery('')}
              className="text-ink-secondary hover:text-ink"
              aria-label="Clear search"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
          <kbd className="px-1.5 py-0.5 text-[10px] text-ink-secondary bg-surface-overlay border border-border rounded font-mono">
            ESC
          </kbd>
        </div>

        {/* Results */}
        <div className="max-h-80 overflow-y-auto py-2">
          {Object.entries(grouped).length === 0 ? (
            <div className="py-8 text-center text-sm text-ink-secondary">No results found</div>
          ) : (
            Object.entries(grouped).map(([category, items]) => {
              const startIdx = flatItems.indexOf(items[0]);
              return (
                <div key={category}>
                  <p className="px-4 py-1.5 text-[10px] font-semibold text-ink-muted uppercase tracking-wider">
                    {category}
                  </p>
                  {items.map((item, i) => {
                    const globalIdx = startIdx + i;
                    return (
                      <button
                        key={item.id}
                        onClick={item.action}
                        className={cn(
                          'w-full flex items-center gap-3 px-4 py-2.5 text-left transition-colors',
                          globalIdx === selected
                            ? 'bg-primary-100 text-ink'
                            : 'text-ink hover:bg-primary-50'
                        )}
                      >
                        <span className="text-ink-secondary shrink-0">{item.icon}</span>
                        <div className="flex-1 min-w-0">
                          <span className="text-sm font-medium truncate block">{item.label}</span>
                          {item.description && (
                            <span className="text-xs text-ink-secondary truncate block">{item.description}</span>
                          )}
                        </div>
                        <ArrowRight className="w-3 h-3 text-ink-muted shrink-0" />
                      </button>
                    );
                  })}
                </div>
              );
            })
          )}
        </div>

        {/* Footer hint */}
        <div className="px-4 py-2 border-t border-border flex gap-3 text-[10px] text-ink-muted">
          <span><kbd className="font-mono">↑↓</kbd> navigate</span>
          <span><kbd className="font-mono">Enter</kbd> select</span>
          <span><kbd className="font-mono">Esc</kbd> close</span>
        </div>
      </div>
    </div>,
    document.body
  );
}
