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

  return (
    <div className="min-h-screen bg-surface">
      {/* Sidebar */}
      <Sidebar />

      {/* Top Header - offset by sidebar width */}
      <div
        className={cn(
          'transition-all duration-200',
          sidebarCollapsed ? 'lg:pl-[56px]' : 'lg:pl-[220px]'
        )}
      >
        <TopHeader />
      </div>

      {/* Main content area */}
      <main
        className={cn(
          'pt-14 transition-all duration-200 min-h-screen',
          sidebarCollapsed ? 'lg:pl-[56px]' : 'lg:pl-[220px]'
        )}
      >
        <div className="p-4 sm:p-6 max-w-[1600px] mx-auto page-enter">
          <Outlet />
        </div>
      </main>

      {/* Global overlays */}
      <CommandPalette />
      <NotificationPanel />
      <ToastContainer />
    </div>
  );
}
