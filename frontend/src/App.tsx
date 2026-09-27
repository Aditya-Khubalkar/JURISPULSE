import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppRouter } from '@/app/router';
import { ToastProvider } from '@/components/feedback/Toast';
import { useAuthStore } from '@/store/authStore';
import { mockCurrentUser } from '@/services/api/mockData';

import { useUIStore } from '@/store/uiStore';

// ── Bootstrap: seed demo user ─────────────────────────────────────────────────

function BootstrapProvider({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, login } = useAuthStore();
  const { theme } = useUIStore();

  React.useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  // Auto-login with demo user in dev mode for convenience
  React.useEffect(() => {
    if (!isAuthenticated && import.meta.env.VITE_AUTO_LOGIN === 'true') {
      login(mockCurrentUser, 'demo-token-' + Date.now());
    }
  }, [isAuthenticated, login]);

  return <>{children}</>;
}

// ── TanStack Query client ─────────────────────────────────────────────────────

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30 * 1000,     // 30s
      gcTime: 5 * 60 * 1000,    // 5min
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// ── Root App ──────────────────────────────────────────────────────────────────

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ToastProvider>
        <BootstrapProvider>
          <AppRouter />
        </BootstrapProvider>
      </ToastProvider>
    </QueryClientProvider>
  );
}
