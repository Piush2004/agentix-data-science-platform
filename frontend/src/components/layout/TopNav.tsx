"use client";

import React, { useState, useEffect, useRef } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { 
  Search, Bell, Command, Database, User, CircleDot, 
  LogOut, Settings, ChevronDown, CheckCircle2, AlertTriangle, Info, ShieldAlert,
  PanelLeft, LayoutDashboard, Upload, Wand2, Layers, BarChart2, Cpu, LineChart, 
  Bot, Workflow, Activity, Play, Sparkles, Server, FileText, Trash2
} from 'lucide-react';
import { useStore } from '@/store/useStore';
import { useSession, signOut } from "next-auth/react";
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { StatusBadge } from '@/components/ui/design-system';

export default function TopNav() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { workspace, setWorkspace, isSidebarOpen, toggleSidebar } = useStore();
  const { data: session } = useSession();
  
  const [profileOpen, setProfileOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [workspaceOpen, setWorkspaceOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);

  const searchInputRef = useRef<HTMLInputElement>(null);

  // Fetch live datasets
  const { data: dbHistoryData } = useQuery({
    queryKey: ['datasetHistory'],
    queryFn: async () => {
      try {
        const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/dataset/history`);
        return res.data.history;
      } catch {
        return [];
      }
    }
  });
  const datasets = Array.isArray(dbHistoryData) ? dbHistoryData : [];

  // Fetch live reports
  const { data: dashboardDataForReports } = useQuery({
    queryKey: ['dashboardDataForReports'],
    queryFn: async () => {
      try {
        const res = await axios.get('/api/dashboard');
        return res.data.data;
      } catch {
        return { recentReports: [] };
      }
    }
  });
  const reports = Array.isArray(dashboardDataForReports?.recentReports) ? dashboardDataForReports.recentReports : [];

  // Fetch live models
  const { data: modelsData } = useQuery({
    queryKey: ['modelsList'],
    queryFn: async () => {
      try {
        const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/model-registry`);
        return res.data.data.registry || [];
      } catch {
        return [];
      }
    }
  });
  const models = Array.isArray(modelsData) ? modelsData : [];

  // Command palette search items dataset
  const searchItems = [
    { category: 'Pages', name: 'Dashboard Workspace', href: '/dashboard', icon: LayoutDashboard },
    { category: 'Pages', name: 'Data Ingestion', href: '/data/ingestion', icon: Upload },
    { category: 'Pages', name: 'Data Cleaning', href: '/data/cleaning', icon: Wand2 },
    { category: 'Pages', name: 'Feature Engineering', href: '/data/feature-engineering', icon: Layers },
    { category: 'Pages', name: 'Advanced EDA Analysis', href: '/analysis/eda', icon: BarChart2 },
    { category: 'Pages', name: 'AutoML Train Suite', href: '/models/automl', icon: Cpu },
    { category: 'Pages', name: 'Model Explainability (SHAP)', href: '/models/explainability', icon: LineChart },
    { category: 'Pages', name: 'AI Analyst Chat', href: '/agents/analyst', icon: Bot },
    { category: 'Pages', name: 'LangGraph Workflow Orchestrator', href: '/agents/workflow', icon: Workflow },
    { category: 'Pages', name: 'Executive Insights Reports', href: '/agents/reports', icon: FileText },
    { category: 'Pages', name: 'MLOps Pipeline Registry', href: '/mlops', icon: Activity },
    { category: 'Pages', name: 'System Settings', href: '/settings', icon: Settings },
    { category: 'Pages', name: 'Admin Command Center', href: '/admin', icon: Server },

    // Dynamic Datasets
    ...(datasets.map((d: any) => ({
      category: 'Datasets',
      name: `Dataset: ${d.name} (${d.rowCount?.toLocaleString()} rows)`,
      href: `/analysis/eda?dataset=${encodeURIComponent(d.name)}`,
      icon: Database
    }))),

    // Dynamic Reports
    ...(reports.map((r: any) => ({
      category: 'Reports',
      name: `Report: ${r.title}`,
      href: r.downloadUrl || `/agents/reports`,
      icon: FileText
    }))),

    // Dynamic Models
    ...(models.map((m: any) => ({
      category: 'Models',
      name: `Model: ${m.name} (${m.algorithm})`,
      href: `/models/explainability?model=${encodeURIComponent(m.id)}`,
      icon: Cpu
    }))),

    // Commands / Actions
    { category: 'Commands', name: 'Run AutoML Hyperparameter Sweep', href: '/models/automl?action=run', icon: Play },
    { category: 'Commands', name: 'Clean Active Workspace Dataset', href: '/data/cleaning?action=start', icon: Sparkles },
    { category: 'Commands', name: 'Extract Feature Vectors', href: '/data/feature-engineering?action=run', icon: Sparkles },
    { category: 'Commands', name: 'Sync Local Ollama Llama-3 Weights', href: '/settings?action=sync_ollama', icon: Server },
    { category: 'Commands', name: 'Invalidate Dashboard Cache', href: '/dashboard?action=invalidate_cache', icon: Activity },
    { category: 'Commands', name: 'Reset Agentix Audit Trail Logs', href: '/settings?action=reset_audit', icon: Trash2 }
  ];

  // Global Ctrl+K / Cmd+K listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsSearchOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Autofocus search input when open
  useEffect(() => {
    if (isSearchOpen) {
      setTimeout(() => searchInputRef.current?.focus(), 50);
      setSearchQuery('');
      setSelectedIndex(0);
    }
  }, [isSearchOpen]);

  // Filter command palette options
  const filteredSearchItems = searchItems.filter(item => 
    item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleNavigate = (href: string) => {
    setIsSearchOpen(false);
    router.push(href);
  };

  const handleSearchKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(prev => (prev + 1) % filteredSearchItems.length);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(prev => (prev - 1 + filteredSearchItems.length) % filteredSearchItems.length);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredSearchItems[selectedIndex]) {
        handleNavigate(filteredSearchItems[selectedIndex].href);
      }
    } else if (e.key === 'Escape') {
      setIsSearchOpen(false);
    }
  };

  // Fetch live notifications
  const { data: notifData } = useQuery({
    queryKey: ['notifications'],
    queryFn: async () => {
      const res = await axios.get('/api/notifications');
      return res.data.notifications;
    },
    refetchInterval: 5000 
  });

  const notifications = notifData || [];
  const unreadCount = notifications.filter((n: any) => !n.read).length;

  // Fetch workspaces
  const { data: wsData } = useQuery({
    queryKey: ['workspaces'],
    queryFn: async () => {
      const res = await axios.get('/api/workspaces');
      return res.data.workspaces;
    }
  });

  const workspaces = wsData || [];

  // Mark single notification read
  const markReadMutation = useMutation({
    mutationFn: async (id: string) => {
      await axios.post('/api/notifications', { action: 'read', id });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    }
  });

  // Clear notifications
  const markAllReadMutation = useMutation({
    mutationFn: async () => {
      await axios.post('/api/notifications', { action: 'read_all' });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    }
  });

  const getNotifIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle2 className="w-4 h-4 text-[#16A34A]" />;
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-[#F59E0B]" />;
      case 'error':
        return <ShieldAlert className="w-4 h-4 text-[#EF4444]" />;
      default:
        return <Info className="w-4 h-4 text-[#5B5CEB]" />;
    }
  };

  return (
    <>
      <header className="h-[72px] bg-[rgba(255,255,255,0.90)] backdrop-blur-[18px] border-b border-[#E7EAF2] shadow-[0_1px_10px_rgba(0,0,0,0.015)] flex items-center justify-between px-4 md:px-8 font-sans relative z-40 w-full select-none">
        
        {/* Left side: Collapse Sidebar + Workspace Switcher */}
        <div className="flex items-center space-x-3">
          {/* Quick sidebar collapse toggle */}
          <button 
            onClick={toggleSidebar}
            className="p-2 hover:bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl text-[#6B7280] hover:text-[#111827] cursor-pointer transition-all mr-1.5"
            title={isSidebarOpen ? "Collapse Sidebar" : "Expand Sidebar"}
            aria-label={isSidebarOpen ? "Collapse Sidebar" : "Expand Sidebar"}
            aria-expanded={isSidebarOpen}
          >
            <PanelLeft className="w-4 h-4" />
          </button>

          <div className="flex items-center space-x-2 text-xs text-[#6B7280] font-bold uppercase tracking-wider">
            <span>Workspace</span>
            <span className="text-[#9CA3AF]">/</span>
            
            <div className="relative">
              <button 
                onClick={() => setWorkspaceOpen(!workspaceOpen)}
                className="flex items-center text-[#111827] font-bold bg-[#F8F9FC] hover:bg-[#EEF2F6] px-3.5 py-2 rounded-xl border border-[#E7EAF2] transition-colors cursor-pointer"
                aria-label="Select active workspace"
                aria-haspopup="listbox"
                aria-expanded={workspaceOpen}
              >
                <Database className="w-3.5 h-3.5 mr-2 text-[#5B5CEB]" />
                <span>{workspace}</span>
                <ChevronDown className="w-3.5 h-3.5 ml-2 text-[#9CA3AF]" />
              </button>

              <AnimatePresence>
                {workspaceOpen && (
                  <>
                    <div className="fixed inset-0 z-30" onClick={() => setWorkspaceOpen(false)} />
                    <motion.div 
                      initial={{ opacity: 0, y: 8, scale: 0.96 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: 8, scale: 0.96 }}
                      transition={{ duration: 0.15, ease: "easeOut" }}
                      className="absolute left-0 mt-2 w-56 bg-white border border-[#E7EAF2] rounded-2xl shadow-xl py-2.5 z-40"
                      role="listbox"
                      aria-label="Workspaces"
                    >
                      <div className="px-3 py-1.5 border-b border-[#E7EAF2] text-[9px] font-bold text-[#9CA3AF] uppercase tracking-wider">
                        Switch Context
                      </div>
                      {workspaces.map((ws: any) => (
                        <button
                          key={ws.id}
                          onClick={() => {
                            setWorkspace(ws.name);
                            setWorkspaceOpen(false);
                          }}
                          className={`w-full text-left px-4 py-2.5 text-xs font-bold hover:bg-[#F8F9FC] transition-colors flex items-center justify-between ${
                            ws.name === workspace ? 'text-[#5B5CEB]' : 'text-[#4B5563]'
                          }`}
                          role="option"
                          aria-selected={ws.name === workspace}
                        >
                          <span>{ws.name}</span>
                          <StatusBadge status={ws.type} type="neutral" />
                        </button>
                      ))}
                      <div className="border-t border-[#E7EAF2] pt-2 px-2">
                        <a href="/settings" onClick={() => setWorkspaceOpen(false)} className="w-full flex items-center justify-center py-2 bg-[#F8F9FC] text-[#111827] hover:bg-[#EEF2F6] rounded-xl text-[10px] font-bold border border-[#E7EAF2] transition-colors">
                          <Settings className="w-3.5 h-3.5 mr-1.5" /> Workspace Members
                        </a>
                      </div>
                    </motion.div>
                  </>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>

        {/* Right side: Search, Status, Notification, Profile */}
        <div className="flex items-center space-x-4">
          
          {/* Spotlight Search Trigger */}
          <div 
            onClick={() => setIsSearchOpen(true)}
            className="hidden md:flex items-center text-xs text-[#9CA3AF] font-bold uppercase tracking-wider bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl px-3 py-2 w-60 justify-between hover:border-[#9CA3AF] transition-colors cursor-pointer"
          >
            <div className="flex items-center">
              <Search className="w-4 h-4 mr-2 text-[#6B7280]" />
              <span>Search platform...</span>
            </div>
            <div className="flex items-center space-x-1 font-mono text-[9px] bg-white border border-[#E7EAF2] px-1.5 py-0.5 rounded-lg text-[#6B7280] font-bold">
              <Command className="w-2.5 h-2.5" />
              <span>K</span>
            </div>
          </div>

          {/* AI Status */}
          <div className="hidden sm:flex items-center px-3.5 py-1.5 bg-[#F0FDF4] border border-[#BBF7D0] rounded-xl shadow-sm shrink-0">
            <CircleDot className="w-3 h-3 text-[#16A34A] mr-1.5 animate-pulse" />
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#14532D]">Agents Ready</span>
          </div>

          {/* Mobile Search Button */}
          <button
            onClick={() => setIsSearchOpen(true)}
            className="flex md:hidden p-2 text-[#6B7280] hover:text-[#111827] hover:bg-[#F8F9FC] rounded-xl border border-[#E7EAF2] bg-white shadow-sm transition-colors cursor-pointer"
            title="Search"
            aria-label="Open search command palette"
            aria-haspopup="dialog"
          >
            <Search className="w-4.5 h-4.5" />
          </button>

          {/* Notifications */}
          <div className="relative">
            <button 
              onClick={() => setNotificationsOpen(!notificationsOpen)}
              className="relative p-2 text-[#6B7280] hover:text-[#111827] hover:bg-[#F8F9FC] rounded-xl border border-[#E7EAF2] bg-white shadow-sm transition-colors cursor-pointer"
              aria-label="View notifications"
              aria-haspopup="true"
              aria-expanded={notificationsOpen}
            >
              <Bell className="w-4.5 h-4.5" />
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 w-4 h-4 bg-[#EF4444] text-[9px] font-extrabold text-white rounded-full flex items-center justify-center ring-2 ring-white">
                  {unreadCount}
                </span>
              )}
            </button>

            <AnimatePresence>
              {notificationsOpen && (
                <>
                  <div className="fixed inset-0 z-30" onClick={() => setNotificationsOpen(false)} />
                  <motion.div 
                    initial={{ opacity: 0, y: 8, scale: 0.96 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 8, scale: 0.96 }}
                    transition={{ duration: 0.15, ease: "easeOut" }}
                    className="absolute right-0 mt-2 w-80 bg-white border border-[#E7EAF2] rounded-2xl shadow-2xl py-2 z-40 overflow-hidden"
                  >
                    <div className="px-4 py-2.5 border-b border-[#E7EAF2] flex justify-between items-center bg-[#F8F9FC]">
                      <span className="text-xs font-bold text-[#111827]">In-App Notifications</span>
                      {unreadCount > 0 && (
                        <button 
                          type="button"
                          onClick={() => markAllReadMutation.mutate()}
                          className="text-[10px] font-extrabold text-[#5B5CEB] hover:underline cursor-pointer"
                        >
                          Clear All
                        </button>
                      )}
                    </div>
                    <div className="max-h-64 overflow-y-auto divide-y divide-[#E7EAF2]">
                      {notifications.length === 0 ? (
                        <div className="px-4 py-8 text-center text-xs text-[#9CA3AF] font-bold uppercase tracking-wider">
                          No new notifications
                        </div>
                      ) : (
                        notifications.map((notif: any) => (
                          <div 
                            key={notif.id} 
                            className={`p-4 text-xs transition-colors flex items-start space-x-3 cursor-pointer ${
                              notif.read ? 'bg-white opacity-70' : 'bg-[#F8F9FC]/40 hover:bg-[#F8F9FC]'
                            }`}
                            onClick={() => {
                              if (!notif.read) markReadMutation.mutate(notif.id);
                            }}
                          >
                            <div className="mt-0.5 shrink-0">{getNotifIcon(notif.type)}</div>
                            <div className="flex-1 space-y-1">
                              <p className="font-bold text-[#111827]">{notif.title}</p>
                              <p className="text-[#6B7280] leading-relaxed text-[11px] font-semibold">{notif.message}</p>
                              <p className="text-[9px] text-[#9CA3AF] font-mono font-bold">{new Date(notif.createdAt).toLocaleTimeString()}</p>
                            </div>
                          </div>
                        ))
                      )}
                    </div>
                  </motion.div>
                </>
              )}
            </AnimatePresence>
          </div>

          {/* Profile Menu */}
          <div className="relative">
            <button 
              onClick={() => setProfileOpen(!profileOpen)}
              className="w-9 h-9 rounded-xl bg-[#F8F9FC] border border-[#E7EAF2] flex items-center justify-center cursor-pointer overflow-hidden ring-2 ring-transparent hover:ring-[#E7EAF2] transition-all shadow-sm"
              aria-label="User profile menu"
              aria-haspopup="menu"
              aria-expanded={profileOpen}
            >
              {session?.user?.image ? (
                <img src={session.user.image} alt="User Avatar" className="w-full h-full object-cover" />
              ) : (
                <User className="w-4.5 h-4.5 text-[#6B7280]" />
              )}
            </button>

            <AnimatePresence>
              {profileOpen && (
                <>
                  <div className="fixed inset-0 z-30" onClick={() => setProfileOpen(false)} />
                  <motion.div 
                    initial={{ opacity: 0, y: 8, scale: 0.96 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 8, scale: 0.96 }}
                    transition={{ duration: 0.15, ease: "easeOut" }}
                    className="absolute right-0 mt-2 w-64 bg-white border border-[#E7EAF2] rounded-2xl shadow-2xl py-2 z-40 overflow-hidden"
                  >
                    <div className="px-4 py-3.5 border-b border-[#E7EAF2] bg-[#F8F9FC]">
                      <p className="text-xs font-extrabold text-[#111827] truncate">{session?.user?.name || 'Enterprise User'}</p>
                      <p className="text-[10px] text-[#6B7280] truncate mt-0.5 font-semibold">{session?.user?.email || 'admin@agentix.com'}</p>
                    </div>
                    <div className="py-1.5">
                      <button 
                        type="button"
                        onClick={() => { setProfileOpen(false); router.push('/settings'); }}
                        className="w-full text-left px-4 py-2 text-xs font-bold text-[#4B5563] hover:bg-[#F8F9FC] hover:text-[#111827] transition-colors flex items-center cursor-pointer"
                      >
                        <Settings className="w-4 h-4 mr-2 text-[#9CA3AF]" /> Settings
                      </button>
                      <button 
                        type="button"
                        onClick={() => { setProfileOpen(false); router.push('/admin'); }}
                        className="w-full text-left px-4 py-2 text-xs font-bold text-[#5B5CEB] hover:bg-[#F8F9FC] transition-colors flex items-center cursor-pointer"
                      >
                        <ShieldAlert className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Admin Command Center
                      </button>
                    </div>
                    <div className="border-t border-[#E7EAF2] py-1.5">
                      <button 
                        type="button"
                        onClick={() => signOut({ callbackUrl: '/' })}
                        className="w-full text-left px-4 py-2 text-xs font-bold text-[#EF4444] hover:bg-[#FEF2F2] transition-colors flex items-center cursor-pointer"
                      >
                        <LogOut className="w-4 h-4 mr-2" /> Log out
                      </button>
                    </div>
                  </motion.div>
                </>
              )}
            </AnimatePresence>
          </div>

        </div>
      </header>

      {/* Spotlight Command Palette Modal */}
      <AnimatePresence>
        {isSearchOpen && (
          <motion.div 
            initial="initial"
            animate="animate"
            exit="exit"
            className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] px-4"
          >
            {/* Backdrop */}
            <motion.div 
              variants={{
                initial: { opacity: 0 },
                animate: { opacity: 1 },
                exit: { opacity: 0 }
              }}
              transition={{ duration: 0.15 }}
              onClick={() => setIsSearchOpen(false)}
              className="absolute inset-0 bg-[#111827]/40 backdrop-blur-md"
            />

            {/* Modal Body */}
            <motion.div
              variants={{
                initial: { opacity: 0, scale: 0.97, y: -8 },
                animate: { opacity: 1, scale: 1, y: 0 },
                exit: { opacity: 0, scale: 0.97, y: -8 }
              }}
              transition={{ duration: 0.15, ease: "easeOut" }}
              className="relative w-full max-w-xl bg-white rounded-2xl border border-[#E7EAF2] shadow-2xl overflow-hidden flex flex-col max-h-[380px] z-50 font-sans text-xs"
              onKeyDown={handleSearchKeyDown}
              role="dialog"
              aria-modal="true"
              aria-label="Command search palette"
            >
              {/* Input block */}
              <div className="h-14 flex items-center px-4 border-b border-[#E7EAF2] shrink-0 bg-white">
                <Search className="w-4.5 h-4.5 text-[#9CA3AF] mr-3" />
                <input 
                  ref={searchInputRef}
                  type="text" 
                  placeholder="Search pages, run commands or ask AI..."
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value);
                    setSelectedIndex(0);
                  }}
                  className="flex-1 bg-transparent border-0 outline-none text-xs font-bold text-[#111827] focus:ring-0 placeholder-[#9CA3AF]"
                  aria-label="Search pages, run commands, or ask AI"
                  aria-autocomplete="list"
                />
                <span className="text-[10px] font-bold text-[#9CA3AF] border border-[#E7EAF2] bg-[#F8F9FC] px-2 py-0.5 rounded-lg">
                  ESC
                </span>
              </div>

              {/* Suggestions results lists */}
              <div className="flex-1 overflow-y-auto p-2 space-y-3 bg-[#F8F9FC]/50 select-none" role="listbox" aria-label="Search results">
                {filteredSearchItems.length === 0 ? (
                  <div className="py-8 text-center text-[#9CA3AF] font-bold uppercase tracking-wider">
                    No results matching query
                  </div>
                ) : (
                  <div>
                    {/* Render grouped items list */}
                    {['Pages', 'Datasets', 'Models', 'Reports', 'Commands'].map((cat) => {
                      const catItems = filteredSearchItems.filter(i => i.category === cat);
                      if (catItems.length === 0) return null;

                      return (
                        <div key={cat} className="space-y-1">
                          <div className="px-3 py-1.5 text-[9px] font-bold text-[#9CA3AF] uppercase tracking-wider">
                            {cat}
                          </div>
                          <div className="space-y-0.5">
                            {catItems.map((item) => {
                              // Find real index inside the overall flat filtered list for hover highlighting
                              const overallIndex = filteredSearchItems.indexOf(item);
                              const isSelected = overallIndex === selectedIndex;

                              return (
                                <div
                                  key={item.name}
                                  onClick={() => handleNavigate(item.href)}
                                  onMouseEnter={() => setSelectedIndex(overallIndex)}
                                  className={`flex items-center px-3.5 py-2.5 rounded-xl transition-all duration-100 cursor-pointer font-bold ${
                                    isSelected 
                                      ? 'bg-[#5B5CEB] text-white' 
                                      : 'text-[#4B5563] hover:bg-[#F8F9FC] hover:text-[#111827]'
                                  }`}
                                  role="option"
                                  aria-selected={isSelected}
                                >
                                  <item.icon className={`w-4 h-4 mr-3 shrink-0 ${isSelected ? 'text-white' : 'text-[#9CA3AF]'}`} />
                                  <span className="flex-1 truncate">{item.name}</span>
                                  {isSelected && (
                                    <span className="text-[10px] bg-white/20 px-2 py-0.5 rounded-md font-sans">
                                      Enter
                                    </span>
                                  )}
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
