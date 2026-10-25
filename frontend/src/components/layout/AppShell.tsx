import React from 'react';
import { Outlet } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { useUIStore } from '@/store/uiStore';
import { Sidebar } from './Sidebar';
import { TopHeader } from './TopHeader';
import { CommandPalette } from '@/components/navigation/CommandPalette';
import { NotificationPanel } from '@/components/navigation/NotificationPanel';
import { ToastContainer } from '@/components/feedback/Toast';

export function AppShell() {
  const { sidebarCollapsed } = useUIStore();
  const sidebarWidth = sidebarCollapsed ? 56 : 220;

  return (
    <div className="min-h-screen bg-surface flex">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content column offset cleanly by sidebar */}
      <div
        className="flex-1 flex flex-col min-w-0 transition-all duration-200"
        style={{ marginLeft: `${sidebarWidth}px` }}
      >
        <TopHeader />

        <main className="flex-1 min-h-[calc(100vh-3.5rem)]">
          <div className="p-4 sm:p-6 max-w-[1600px] w-full mx-auto page-enter">
            <Outlet />
          </div>
        </main>
      </div>

      {/* Global overlays */}
      <CommandPalette />
      <NotificationPanel />
      <ToastContainer />
    </div>
  );
}
