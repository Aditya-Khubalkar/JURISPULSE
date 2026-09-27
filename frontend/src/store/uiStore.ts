import { create } from 'zustand';
import { persist } from 'zustand/middleware';

type Theme = 'light' | 'dark';

interface UIStore {
  // Sidebar
  sidebarCollapsed: boolean;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;

  // Theme
  theme: Theme;
  setTheme: (theme: Theme) => void;

  // Command palette
  commandPaletteOpen: boolean;
  setCommandPaletteOpen: (open: boolean) => void;
  toggleCommandPalette: () => void;

  // Right panel
  rightPanelOpen: boolean;
  rightPanelContent: string | null;
  setRightPanel: (open: boolean, content?: string | null) => void;

  // Mobile nav drawer
  mobileNavOpen: boolean;
  setMobileNavOpen: (open: boolean) => void;

  // Notification panel
  notificationPanelOpen: boolean;
  setNotificationPanelOpen: (open: boolean) => void;
}

export const useUIStore = create<UIStore>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      toggleSidebar: () =>
        set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setSidebarCollapsed: (collapsed) =>
        set({ sidebarCollapsed: collapsed }),

      theme: 'light',
      setTheme: (theme) => set({ theme }),

      commandPaletteOpen: false,
      setCommandPaletteOpen: (commandPaletteOpen) =>
        set({ commandPaletteOpen }),
      toggleCommandPalette: () =>
        set((state) => ({ commandPaletteOpen: !state.commandPaletteOpen })),

      rightPanelOpen: false,
      rightPanelContent: null,
      setRightPanel: (open, content = null) =>
        set({ rightPanelOpen: open, rightPanelContent: content }),

      mobileNavOpen: false,
      setMobileNavOpen: (mobileNavOpen) => set({ mobileNavOpen }),

      notificationPanelOpen: false,
      setNotificationPanelOpen: (notificationPanelOpen) =>
        set({ notificationPanelOpen }),
    }),
    {
      name: 'juris-ui',
      partialize: (state) => ({
        sidebarCollapsed: state.sidebarCollapsed,
        theme: state.theme,
      }),
    }
  )
);
