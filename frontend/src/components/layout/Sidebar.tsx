import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { useUIStore } from '@/store/uiStore';
import { useAuthStore } from '@/store/authStore';
import { ROUTES } from '@/constants';
import {
  LayoutDashboard,
  Briefcase,
  FileText,
  Search,
  FileEdit,
  Scale,
  Clock,
  Calendar,
  CheckSquare,
  Bot,
  Activity,
  ShieldCheck,
  Users,
  UserCheck,
  MessageSquare,
  BarChart3,
  FileBarChart,
  Settings,
  Bell,
  HelpCircle,
  ChevronLeft,
  ChevronRight,
  User,
} from 'lucide-react';
import { Avatar } from '@/design-system';
import { useNotificationStore } from '@/store/notificationStore';

// ── Navigation Groups ─────────────────────────────────────────────────────────

interface NavItem {
  label: string;
  to: string;
  icon: React.ReactNode;
  badge?: number;
  roles?: string[];
}

interface NavGroup {
  title?: string;
  items: NavItem[];
}

function useNavGroups(): NavGroup[] {
  const { unreadCount } = useNotificationStore();
  return [
    {
      title: 'Overview',
      items: [
        { label: 'Dashboard', to: ROUTES.DASHBOARD, icon: <LayoutDashboard className="w-4 h-4" /> },
      ],
    },
    {
      title: 'Workspace',
      items: [
        { label: 'Cases', to: ROUTES.CASES, icon: <Briefcase className="w-4 h-4" /> },
        { label: 'Documents', to: ROUTES.DOCUMENTS, icon: <FileText className="w-4 h-4" /> },
        { label: 'Research', to: ROUTES.RESEARCH, icon: <Search className="w-4 h-4" /> },
        { label: 'Drafts', to: ROUTES.DRAFTS, icon: <FileEdit className="w-4 h-4" /> },
        { label: 'Evidence', to: ROUTES.EVIDENCE, icon: <Scale className="w-4 h-4" /> },
        { label: 'Timeline', to: ROUTES.TIMELINE, icon: <Clock className="w-4 h-4" /> },
        { label: 'Hearings', to: ROUTES.HEARINGS, icon: <Calendar className="w-4 h-4" /> },
        { label: 'Calendar', to: ROUTES.CALENDAR, icon: <Calendar className="w-4 h-4" /> },
        { label: 'Tasks', to: ROUTES.TASKS, icon: <CheckSquare className="w-4 h-4" /> },
      ],
    },
    {
      title: 'AI Workspace',
      items: [
        { label: 'AI Assistant', to: ROUTES.AI_WORKSPACE, icon: <Bot className="w-4 h-4" /> },
        { label: 'Agent Activity', to: ROUTES.AGENTS_ACTIVITY, icon: <Activity className="w-4 h-4" /> },
        { label: 'Verification', to: ROUTES.VERIFICATION, icon: <ShieldCheck className="w-4 h-4" /> },
      ],
    },
    {
      title: 'Collaboration',
      items: [
        { label: 'Clients', to: ROUTES.CLIENTS, icon: <UserCheck className="w-4 h-4" /> },
        { label: 'Team', to: ROUTES.TEAM, icon: <Users className="w-4 h-4" /> },
        { label: 'Comments', to: ROUTES.COLLABORATION, icon: <MessageSquare className="w-4 h-4" /> },
      ],
    },
    {
      title: 'Insights',
      items: [
        { label: 'Analytics', to: ROUTES.ANALYTICS, icon: <BarChart3 className="w-4 h-4" /> },
        { label: 'Reports', to: ROUTES.REPORTS, icon: <FileBarChart className="w-4 h-4" /> },
      ],
    },
    {
      title: 'Administration',
      items: [
        { label: 'Admin Panel', to: ROUTES.ADMIN, icon: <Settings className="w-4 h-4" />, roles: ['admin'] },
      ],
    },
    {
      items: [
        { label: 'Notifications', to: ROUTES.NOTIFICATIONS, icon: <Bell className="w-4 h-4" />, badge: unreadCount || undefined },
        { label: 'Help', to: '/help', icon: <HelpCircle className="w-4 h-4" /> },
        { label: 'Settings', to: ROUTES.SETTINGS, icon: <Settings className="w-4 h-4" /> },
      ],
    },
  ];
}

// ── Sidebar Logo ──────────────────────────────────────────────────────────────

function SidebarLogo({ collapsed }: { collapsed: boolean }) {
  return (
    <div className={cn('flex items-center h-16 px-4 border-b border-primary-100', collapsed && 'justify-center px-2')}>
      <div className="flex items-center gap-2.5">
        <div className="w-8 h-8 rounded-[8px] bg-primary-400 flex items-center justify-center shrink-0">
          <Scale className="w-4.5 h-4.5 text-primary-900" strokeWidth={2.5} />
        </div>
        {!collapsed && (
          <div>
            <span className="text-base font-bold text-ink tracking-tight">JurisPulse</span>
            <div className="text-[10px] text-ink-secondary font-medium -mt-0.5">Legal Workspace</div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Nav Item ──────────────────────────────────────────────────────────────────

function SidebarNavItem({ item, collapsed }: { item: NavItem; collapsed: boolean }) {
  const location = useLocation();
  const isActive = location.pathname === item.to || location.pathname.startsWith(item.to + '/');

  return (
    <NavLink
      to={item.to}
      title={collapsed ? item.label : undefined}
      className={cn(
        'group flex items-center gap-2.5 px-3 py-2 rounded-[6px] text-sm font-medium transition-all duration-100',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-400',
        isActive
          ? 'bg-primary-400 text-primary-900 shadow-sm'
          : 'text-ink-secondary hover:bg-primary-100 hover:text-ink',
        collapsed && 'justify-center px-2'
      )}
    >
      <span className={cn('shrink-0', isActive ? 'text-primary-900' : 'text-ink-secondary group-hover:text-ink')}>
        {item.icon}
      </span>
      {!collapsed && (
        <>
          <span className="flex-1 truncate">{item.label}</span>
          {item.badge && item.badge > 0 && (
            <span className="ml-auto min-w-[18px] h-[18px] px-1 text-[10px] font-bold bg-primary-700 text-white rounded-full flex items-center justify-center">
              {item.badge > 99 ? '99+' : item.badge}
            </span>
          )}
        </>
      )}
    </NavLink>
  );
}

// ── Main Sidebar ──────────────────────────────────────────────────────────────

export function Sidebar() {
  const { sidebarCollapsed, toggleSidebar } = useUIStore();
  const { user } = useAuthStore();
  const navGroups = useNavGroups();

  return (
    <aside
      className={cn(
        'fixed top-0 left-0 h-full bg-surface border-r border-border flex flex-col z-30',
        'sidebar-transition',
        sidebarCollapsed ? 'w-[56px]' : 'w-[220px]'
      )}
    >
      {/* Logo */}
      <SidebarLogo collapsed={sidebarCollapsed} />

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
        {navGroups.map((group, gi) => (
          <div key={gi} className={gi > 0 ? 'mt-3' : ''}>
            {group.title && !sidebarCollapsed && (
              <p className="px-3 py-1 text-[10px] font-semibold text-ink-muted uppercase tracking-wider">
                {group.title}
              </p>
            )}
            {group.items.map((item) => (
              <SidebarNavItem key={item.to} item={item} collapsed={sidebarCollapsed} />
            ))}
          </div>
        ))}
      </nav>

      {/* Profile Footer */}
      <div className="p-2 border-t border-border">
        <NavLink
          to={ROUTES.SETTINGS_PROFILE}
          className={cn(
            'flex items-center gap-2.5 px-2 py-2 rounded-[6px] hover:bg-primary-100 transition-colors',
            sidebarCollapsed && 'justify-center'
          )}
        >
          <Avatar name={user?.name ?? 'User'} size="sm" />
          {!sidebarCollapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-ink truncate">{user?.name ?? 'User'}</p>
              <p className="text-[10px] text-ink-secondary capitalize">{user?.role}</p>
            </div>
          )}
          {!sidebarCollapsed && <User className="w-3.5 h-3.5 text-ink-secondary shrink-0" />}
        </NavLink>
      </div>

      {/* Collapse Toggle */}
      <button
        onClick={toggleSidebar}
        aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        className={cn(
          'absolute -right-3 top-20 w-6 h-6 bg-surface-raised border border-border rounded-full',
          'flex items-center justify-center shadow-sm text-ink-secondary hover:text-ink',
          'transition-colors hover:border-primary-400 hover:text-primary-700',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-400'
        )}
      >
        {sidebarCollapsed ? (
          <ChevronRight className="w-3 h-3" />
        ) : (
          <ChevronLeft className="w-3 h-3" />
        )}
      </button>
    </aside>
  );
}
