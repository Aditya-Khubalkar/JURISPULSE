import React from 'react';
import { Bell, X, Check, CheckCheck, Briefcase, FileText, FileEdit, ShieldCheck, CheckSquare, MessageSquare } from 'lucide-react';
import { useUIStore } from '@/store/uiStore';
import { useNotificationStore } from '@/store/notificationStore';
import { Drawer } from '@/design-system';
import { Button } from '@/design-system';
import { formatRelativeTime } from '@/lib/utils';
import type { Notification } from '@/types';

function NotificationIcon({ type }: { type: Notification['type'] }) {
  const icons: Record<string, React.ReactNode> = {
    hearing_approaching: <Bell className="w-4 h-4" />,
    deadline_approaching: <Bell className="w-4 h-4 text-orange-500" />,
    document_processed: <FileText className="w-4 h-4 text-blue-500" />,
    draft_ready: <FileEdit className="w-4 h-4 text-purple-500" />,
    verification_warning: <ShieldCheck className="w-4 h-4 text-amber-500" />,
    task_assigned: <CheckSquare className="w-4 h-4 text-green-600" />,
    comment: <MessageSquare className="w-4 h-4 text-gray-500" />,
    case_update: <Briefcase className="w-4 h-4 text-green-600" />,
    system: <Bell className="w-4 h-4" />,
  };
  return <span>{icons[type] ?? <Bell className="w-4 h-4" />}</span>;
}

export function NotificationPanel() {
  const { notificationPanelOpen, setNotificationPanelOpen } = useUIStore();
  const { notifications, markAsRead, markAllAsRead, unreadCount } = useNotificationStore();

  return (
    <Drawer
      open={notificationPanelOpen}
      onClose={() => setNotificationPanelOpen(false)}
      title="Notifications"
      width="max-w-sm"
      footer={
        unreadCount > 0 ? (
          <Button
            variant="ghost"
            size="sm"
            fullWidth
            onClick={markAllAsRead}
            leftIcon={<CheckCheck className="w-4 h-4" />}
          >
            Mark all as read
          </Button>
        ) : undefined
      }
    >
      <div className="space-y-1">
        {notifications.length === 0 ? (
          <div className="py-12 text-center text-sm text-ink-secondary">
            <Bell className="w-8 h-8 mx-auto mb-2 opacity-30" />
            <p>No notifications</p>
          </div>
        ) : (
          notifications.map((n) => (
            <div
              key={n.id}
              className={`flex gap-3 p-3 rounded-[8px] transition-colors cursor-pointer ${
                n.isRead ? 'hover:bg-primary-50' : 'bg-primary-50 hover:bg-primary-100'
              }`}
              onClick={() => markAsRead(n.id)}
              role="button"
              tabIndex={0}
            >
              <div className="mt-0.5 shrink-0 w-8 h-8 rounded-full bg-surface-raised border border-border flex items-center justify-center text-ink-secondary">
                <NotificationIcon type={n.type} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-ink leading-snug">{n.title}</p>
                <p className="text-xs text-ink-secondary mt-0.5 leading-snug">{n.message}</p>
                <p className="text-[10px] text-ink-muted mt-1">{formatRelativeTime(n.createdAt)}</p>
              </div>
              {!n.isRead && (
                <div className="w-2 h-2 bg-primary-400 rounded-full mt-2 shrink-0" aria-label="Unread" />
              )}
            </div>
          ))
        )}
      </div>
    </Drawer>
  );
}
