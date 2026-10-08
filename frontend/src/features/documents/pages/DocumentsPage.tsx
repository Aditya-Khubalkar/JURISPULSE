/**\n * Documents list and upload interface.\n */\nimport React, { useState, useRef, useCallback } from 'react';
import { Search, Upload, FileText, Download, Eye, MoreHorizontal, Cloud, X, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import {
  Card, StatusBadge, Badge, EmptyState, Breadcrumb, Button,
} from '@/design-system';
import { formatDate, formatFileSize } from '@/lib/utils';
import { DOCUMENT_TYPE_LABELS } from '@/constants';
import { mockDocuments } from '@/services/api/mockData';
import { documentsApi } from '@/services/api/mockApi';
import type { Document, DocumentType } from '@/types';

// ── Upload item state ─────────────────────────────────────────────────────────
interface UploadItem {
  id: string;
  file: File;
  status: 'pending' | 'uploading' | 'done' | 'error';
  progress: number;
  error?: string;
  result?: Document;
}

const ACCEPTED_TYPES = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/plain', 'image/png', 'image/jpeg'];
const MAX_SIZE_BYTES = 50 * 1024 * 1024; // 50 MB

function getFileIcon(fileType: string) {
  if (fileType.includes('pdf')) return { bg: 'bg-red-50', text: 'text-red-400' };
  if (fileType.includes('word') || fileType.includes('document')) return { bg: 'bg-blue-50', text: 'text-blue-400' };
  if (fileType.includes('image')) return { bg: 'bg-green-50', text: 'text-green-400' };
  return { bg: 'bg-gray-50', text: 'text-gray-400' };
}

export function DocumentsPage() {
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const [documents, setDocuments] = useState<Document[]>(mockDocuments);
  const [uploads, setUploads] = useState<UploadItem[]>([]);
  const [viewDoc, setViewDoc] = useState<Document | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const dragCounter = useRef(0);

  // ── Filtering ───────────────────────────────────────────────────────────────
  const filtered = documents.filter((d) => {
    const matchSearch = !search || d.title.toLowerCase().includes(search.toLowerCase())
      || d.fileName.toLowerCase().includes(search.toLowerCase());
    const matchType = !typeFilter || d.documentType === typeFilter;
    return matchSearch && matchType;
  });

  // ── Upload logic ─────────────────────────────────────────────────────────────
  const processFiles = useCallback((files: FileList | File[]) => {
    const fileArray = Array.from(files);
    const newItems: UploadItem[] = fileArray.map((file) => {
      const id = 'upload-' + Date.now() + '-' + Math.random().toString(36).slice(2);
      let error: string | undefined;
      if (!ACCEPTED_TYPES.includes(file.type)) {
        error = `Unsupported file type: ${file.type || 'unknown'}`;
      } else if (file.size > MAX_SIZE_BYTES) {
        error = `File exceeds 50 MB limit`;
      }
      return { id, file, status: error ? 'error' : 'pending', progress: 0, error };
    });

    setUploads((prev) => [...newItems, ...prev]);

    // Upload valid files
    newItems.filter((item) => !item.error).forEach((item) => {
      uploadFile(item);
    });
  }, []);

  const uploadFile = (item: UploadItem) => {
    // Mark as uploading
    setUploads((prev) =>
      prev.map((u) => u.id === item.id ? { ...u, status: 'uploading', progress: 10 } : u)
    );

    // Simulate progress ticks then call mock API
    const tick = (progress: number) => {
      if (progress < 80) {
        setTimeout(() => {
          setUploads((prev) =>
            prev.map((u) => u.id === item.id ? { ...u, progress } : u)
          );
          tick(Math.min(progress + Math.floor(Math.random() * 20 + 10), 80));
        }, 300);
      }
    };
    tick(20);

    documentsApi.upload(item.file, {
      title: item.file.name.replace(/\.[^.]+$/, '').replace(/[_-]/g, ' '),
      fileName: item.file.name,
      fileSize: item.file.size,
      fileType: item.file.type,
      documentType: guessDocumentType(item.file.name),
    }).then((res) => {
      const newDoc: Document = {
        ...res.data,
        title: item.file.name.replace(/\.[^.]+$/, '').replace(/[_-]/g, ' '),
        fileName: item.file.name,
        fileSize: item.file.size,
        fileType: item.file.type,
        documentType: guessDocumentType(item.file.name),
        url: URL.createObjectURL(item.file),
      };
      setDocuments((prev) => [newDoc, ...prev]);
      setUploads((prev) =>
        prev.map((u) => u.id === item.id ? { ...u, status: 'done', progress: 100, result: newDoc } : u)
      );
      // Auto-dismiss after 4 s
      setTimeout(() => {
        setUploads((prev) => prev.filter((u) => u.id !== item.id));
      }, 4000);
    }).catch((err) => {
      setUploads((prev) =>
        prev.map((u) => u.id === item.id ? { ...u, status: 'error', progress: 0, error: err.message ?? 'Upload failed' } : u)
      );
    });
  };

  // ── Drag handlers ────────────────────────────────────────────────────────────
  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    dragCounter.current++;
    if (dragCounter.current === 1) setDragOver(true);
  };
  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    dragCounter.current--;
    if (dragCounter.current === 0) setDragOver(false);
  };
  const handleDragOver = (e: React.DragEvent) => { e.preventDefault(); };
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    dragCounter.current = 0;
    setDragOver(false);
    if (e.dataTransfer.files.length) processFiles(e.dataTransfer.files);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) {
      processFiles(e.target.files);
      e.target.value = '';
    }
  };

  const openFilePicker = () => fileInputRef.current?.click();

  // ── Download handler ─────────────────────────────────────────────────────────
  const handleDownload = (doc: Document) => {
    if (doc.url) {
      const a = document.createElement('a');
      a.href = doc.url;
      a.download = doc.fileName;
      a.click();
    } else {
      // For mock data without a real URL, show a toast/alert
      alert(`Download not available for mock document: ${doc.fileName}`);
    }
  };

  return (
    <div className="space-y-5">
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".pdf,.docx,.txt,.png,.jpg,.jpeg"
        className="hidden"
        onChange={handleFileInput}
        aria-label="Upload files"
        id="file-upload-input"
      />

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <Breadcrumb items={[{ label: 'Workspace' }, { label: 'Documents' }]} />
          <h1 className="text-2xl font-bold text-ink mt-1">Documents</h1>
          <p className="text-sm text-ink-secondary">{documents.length} documents</p>
        </div>
        <Button variant="primary" leftIcon={<Upload className="w-4 h-4" />} onClick={openFilePicker}>
          Upload
        </Button>
      </div>

      {/* Upload Drop Zone */}
      <div
        role="button"
        tabIndex={0}
        aria-label="Drop zone for file upload"
        className={`border-2 border-dashed rounded-[12px] p-8 text-center transition-all cursor-pointer select-none ${
          dragOver
            ? 'border-primary-400 bg-primary-50 scale-[1.01]'
            : 'border-border bg-surface-raised hover:border-primary-300 hover:bg-surface-overlay'
        }`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={openFilePicker}
        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') openFilePicker(); }}
      >
        <Cloud className={`w-10 h-10 mx-auto mb-3 transition-colors ${dragOver ? 'text-primary-500' : 'text-border-strong'}`} />
        <p className="font-medium text-ink">Drop files to upload</p>
        <p className="text-sm text-ink-secondary mt-1">
          or{' '}
          <span
            className="text-primary-700 underline cursor-pointer"
            onClick={(e) => { e.stopPropagation(); openFilePicker(); }}
          >
            browse files
          </span>
        </p>
        <p className="text-xs text-ink-muted mt-2">PDF, DOCX, TXT, PNG, JPEG up to 50MB</p>
      </div>

      {/* Active uploads panel */}
      {uploads.length > 0 && (
        <div className="space-y-2">
          {uploads.map((item) => (
            <div
              key={item.id}
              className="flex items-center gap-3 p-3 rounded-[10px] border border-border bg-surface-raised"
            >
              {/* Icon */}
              <div className={`w-9 h-9 rounded-[6px] flex items-center justify-center shrink-0 ${getFileIcon(item.file.type).bg}`}>
                <FileText className={`w-4 h-4 ${getFileIcon(item.file.type).text}`} />
              </div>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-ink truncate">{item.file.name}</p>
                <div className="flex items-center gap-2 mt-1">
                  {item.status === 'uploading' && (
                    <>
                      <div className="flex-1 h-1.5 bg-border rounded-full overflow-hidden">
                        <div
                          className="h-full bg-primary-500 rounded-full transition-all duration-300"
                          style={{ width: `${item.progress}%` }}
                        />
                      </div>
                      <span className="text-xs text-ink-muted shrink-0">{item.progress}%</span>
                    </>
                  )}
                  {item.status === 'pending' && (
                    <span className="text-xs text-ink-muted">Waiting...</span>
                  )}
                  {item.status === 'done' && (
                    <span className="text-xs text-emerald-600 flex items-center gap-1">
                      <CheckCircle className="w-3 h-3" /> Uploaded successfully
                    </span>
                  )}
                  {item.status === 'error' && (
                    <span className="text-xs text-red-500 flex items-center gap-1">
                      <AlertCircle className="w-3 h-3" /> {item.error}
                    </span>
                  )}
                </div>
              </div>

              {/* Status icon + dismiss */}
              <div className="flex items-center gap-1 shrink-0">
                {item.status === 'uploading' && (
                  <Loader2 className="w-4 h-4 text-primary-500 animate-spin" />
                )}
                {item.status === 'done' && (
                  <CheckCircle className="w-4 h-4 text-emerald-500" />
                )}
                {item.status === 'error' && (
                  <AlertCircle className="w-4 h-4 text-red-500" />
                )}
                <button
                  className="p-1 text-ink-muted hover:text-ink hover:bg-surface-overlay rounded-[4px] transition-colors"
                  onClick={() => setUploads((prev) => prev.filter((u) => u.id !== item.id))}
                  aria-label="Dismiss upload"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Filters */}
      <Card padding="sm">
        <div className="flex flex-wrap gap-3">
          <div className="flex-1 min-w-[180px] relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-secondary pointer-events-none" />
            <input
              type="search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search documents..."
              className="w-full h-9 pl-9 pr-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
            />
          </div>
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="h-9 px-3 text-sm border border-border rounded-[6px] bg-surface-raised focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent"
            aria-label="Filter by document type"
          >
            <option value="">All Types</option>
            {Object.entries(DOCUMENT_TYPE_LABELS).map(([v, l]) => (
              <option key={v} value={v}>{l}</option>
            ))}
          </select>
        </div>
      </Card>

      {/* Documents List */}
      <div className="space-y-2">
        {filtered.length === 0 ? (
          <EmptyState
            icon={<FileText className="w-6 h-6" />}
            title="No documents found"
            description="Upload a document or adjust your filters."
            action={<Button variant="primary" leftIcon={<Upload className="w-4 h-4" />} onClick={openFilePicker}>Upload Document</Button>}
          />
        ) : (
          filtered.map((doc) => {
            const icon = getFileIcon(doc.fileType);
            return (
              <Card key={doc.id} hoverable>
                <div className="flex items-center gap-3">
                  {/* File icon */}
                  <div className={`w-10 h-10 rounded-[8px] flex items-center justify-center shrink-0 ${icon.bg}`}>
                    <FileText className={`w-5 h-5 ${icon.text}`} />
                  </div>

                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-ink truncate">{doc.title}</p>
                    <div className="flex items-center gap-2 mt-0.5 flex-wrap">
                      <span className="text-xs text-ink-secondary">{doc.fileName}</span>
                      <span className="text-xs text-ink-muted">·</span>
                      <span className="text-xs text-ink-secondary">{formatFileSize(doc.fileSize)}</span>
                      <span className="text-xs text-ink-muted">·</span>
                      <span className="text-xs text-ink-secondary">{formatDate(doc.uploadedAt)}</span>
                      {doc.caseName && (
                        <>
                          <span className="text-xs text-ink-muted">·</span>
                          <span className="text-xs text-primary-700">{doc.caseName}</span>
                        </>
                      )}
                    </div>
                  </div>

                  {/* Badges */}
                  <div className="hidden sm:flex items-center gap-2 shrink-0">
                    <Badge variant="neutral" size="sm">
                      {DOCUMENT_TYPE_LABELS[doc.documentType] ?? doc.documentType}
                    </Badge>
                    <StatusBadge status={doc.status} />
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-1">
                    <button
                      className="p-1.5 text-ink-secondary hover:text-ink hover:bg-surface-overlay rounded-[4px] transition-colors"
                      aria-label="View document"
                      title="View"
                      onClick={() => {
                        if (doc.url) window.open(doc.url, '_blank');
                        else setViewDoc(doc);
                      }}
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      className="p-1.5 text-ink-secondary hover:text-ink hover:bg-surface-overlay rounded-[4px] transition-colors"
                      aria-label="Download document"
                      title="Download"
                      onClick={() => handleDownload(doc)}
                    >
                      <Download className="w-4 h-4" />
                    </button>
                    <button
                      className="p-1.5 text-ink-secondary hover:text-ink hover:bg-surface-overlay rounded-[4px] transition-colors"
                      aria-label="More options"
                      title="More"
                    >
                      <MoreHorizontal className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Processing status bar */}
                {doc.status === 'processing' && (
                  <div className="mt-2 ml-13">
                    <div className="flex items-center gap-2 text-xs text-amber-600">
                      <div className="w-3 h-3 border-2 border-amber-400 border-t-transparent rounded-full animate-spin" />
                      Processing: OCR, classification, entity extraction...
                    </div>
                  </div>
                )}
              </Card>
            );
          })
        )}
      </div>

      {/* Document Preview Modal */}
      {viewDoc && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
          onClick={() => setViewDoc(null)}
        >
          <div
            className="bg-surface rounded-[16px] shadow-2xl max-w-lg w-full p-6 space-y-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-lg font-bold text-ink">{viewDoc.title}</h2>
                <p className="text-sm text-ink-secondary mt-0.5">{viewDoc.fileName} · {formatFileSize(viewDoc.fileSize)}</p>
              </div>
              <button
                className="p-1.5 text-ink-muted hover:text-ink hover:bg-surface-overlay rounded-[6px] transition-colors"
                onClick={() => setViewDoc(null)}
                aria-label="Close preview"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div><span className="text-ink-muted">Type</span><p className="font-medium text-ink mt-0.5">{DOCUMENT_TYPE_LABELS[viewDoc.documentType] ?? viewDoc.documentType}</p></div>
              <div><span className="text-ink-muted">Status</span><div className="mt-0.5"><StatusBadge status={viewDoc.status} /></div></div>
              <div><span className="text-ink-muted">Uploaded</span><p className="font-medium text-ink mt-0.5">{formatDate(viewDoc.uploadedAt)}</p></div>
              <div><span className="text-ink-muted">Version</span><p className="font-medium text-ink mt-0.5">v{viewDoc.version}</p></div>
              {viewDoc.caseName && (
                <div className="col-span-2"><span className="text-ink-muted">Case</span><p className="font-medium text-ink mt-0.5">{viewDoc.caseName}</p></div>
              )}
            </div>
            {viewDoc.ocrText && (
              <div>
                <p className="text-xs text-ink-muted mb-1">Extracted Text (preview)</p>
                <p className="text-xs text-ink bg-surface-raised rounded-[6px] p-3 max-h-32 overflow-y-auto leading-relaxed">{viewDoc.ocrText.slice(0, 400)}…</p>
              </div>
            )}
            <div className="flex gap-2 pt-1">
              <Button variant="primary" leftIcon={<Download className="w-3.5 h-3.5" />} className="flex-1" onClick={() => { handleDownload(viewDoc); setViewDoc(null); }}>
                Download
              </Button>
              <Button variant="secondary" className="flex-1" onClick={() => setViewDoc(null)}>
                Close
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function guessDocumentType(fileName: string): DocumentType {
  const name = fileName.toLowerCase();
  if (name.includes('petition') || name.includes('writ')) return 'petition';
  if (name.includes('affidavit')) return 'affidavit';
  if (name.includes('notice')) return 'notice';
  if (name.includes('order')) return 'order';
  if (name.includes('judgment') || name.includes('judgement')) return 'judgment';
  if (name.includes('evidence') || name.includes('exhibit')) return 'evidence';
  if (name.includes('reply')) return 'reply';
  if (name.includes('bail')) return 'bail_application';
  if (name.includes('appeal')) return 'appeal';
  if (name.includes('complaint')) return 'complaint';
  if (name.includes('contract') || name.includes('agreement')) return 'contract';
  return 'other';
}
\n// Add document detail view\n\n// Add document upload surface\n\n// Add upload progress state\n