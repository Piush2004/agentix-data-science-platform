import { create } from 'zustand';

interface AppState {
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
  workspace: string;
  setWorkspace: (ws: string) => void;
  theme: 'dark' | 'light';
  toggleTheme: () => void;
}

export const useStore = create<AppState>((set) => ({
  isSidebarOpen: true,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  workspace: 'Production',
  setWorkspace: (ws) => set({ workspace: ws }),
  theme: 'light',
  toggleTheme: () => set((state) => ({ theme: state.theme === 'dark' ? 'light' : 'dark' })),
}));
