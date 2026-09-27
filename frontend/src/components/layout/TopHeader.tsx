import React, { useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bell, Search, Menu, Plus, Settings, Sun, Moon } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useUIStore } from '@/store/uiStore';
import { useAuthStore } from '@/store/authStore';
import { useNotificationStore } from '@/store/notificationStore';
import { IconButton } from '@/design-system';
import { ROUTES } from '@/constants';

export function TopHeader() {
  const { toggleSidebar, setCommandPaletteOpen, setNotificationPanelOpen, theme, setTheme } = useUIStore();
  const { user } = useAuthStore();
  const { unreadCount } = useNotificationStore();
  const navigate = useNavigate();

  // Global keyboard shortcut: Ctrl+K for command palette
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen(true);
      }
    },
    [setCommandPaletteOpen]
  );

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  return (
    <header className="fixed top-0 right-0 left-0 h-14 bg-surface-raised border-b border-border z-20 flex items-center px-4 gap-3">
      {/* Mobile menu toggle */}
      <button
        onClick={toggleSidebar}
        className="lg:hidden p-1.5 text-ink-secondary hover:text-ink hover:bg-surface-overlay rounded-[6px] transition-colors"
        aria-label="Toggle menu"
      >
        <Menu className="w-4 h-4" />
      </button>

      {/* Greeting (desktop) */}
      <div className="hidden md:block flex-1">
        <span className="text-sm text-ink-secondary">
          {getGreeting()},{' '}
          <span className="font-semibold text-ink">{user?.name?.split(' ')[0]}</span>
        </span>
      </div>

      {/* Right actions */}
      <div className="ml-auto flex items-center gap-1.5">
        {/* Global search button */}
        <button
          onClick={() => setCommandPaletteOpen(true)}
          className={cn(
            'hidden sm:flex items-center gap-2 h-8 px-3 text-sm text-ink-secondary',
            'bg-surface border border-border rounded-[6px] hover:border-border-strong',
            'transition-colors duration-150'
          )}
          aria-label="Open search (Ctrl+K)"
        >
          <Search className="w-3.5 h-3.5" />
          <span className="hidden md:block">Search...</span>
          <kbd className="hidden md:inline-flex items-center gap-0.5 ml-1 px-1.5 py-0.5 text-[10px] bg-surface-raised border border-border rounded font-mono">
            ⌘K
          </kbd>
        </button>

        {/* Quick add */}
        <IconButton
          label="Quick actions"
          variant="ghost"
          size="sm"
          onClick={() => setCommandPaletteOpen(true)}
          className="hidden sm:inline-flex"
        >
          <Plus className="w-4 h-4" />
        </IconButton>

        {/* Theme toggle */}
        <IconButton
          label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          variant="ghost"
          size="sm"
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
        >
          {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </IconButton>

        {/* Settings */}
        <IconButton
          label="Settings"
          variant="ghost"
          size="sm"
          onClick={() => navigate(ROUTES.SETTINGS)}
        >
          <Settings className="w-4 h-4" />
        </IconButton>

        {/* Notifications */}
        <button
          onClick={() => setNotificationPanelOpen(true)}
          className={cn(
            'relative p-2 text-ink-secondary hover:text-ink hover:bg-surface-overlay rounded-[6px]',
            'transition-colors duration-150',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-400'
          )}
          aria-label={`Notifications${unreadCount > 0 ? ` (${unreadCount} unread)` : ''}`}
        >
          <Bell className="w-4 h-4" />
          {unreadCount > 0 && (
            <span className="absolute top-1 right-1 w-2 h-2 bg-[#e76f51] rounded-full" aria-hidden="true" />
          )}
        </button>
      </div>
    </header>
  );
}
