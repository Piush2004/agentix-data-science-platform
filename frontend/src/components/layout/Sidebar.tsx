"use client";

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard, Upload, Wand2, Layers, 
  BarChart2, Cpu, LineChart, Bot, Workflow, 
  Activity, Settings, BrainCircuit,
  PanelLeftClose, PanelLeft, ChevronLeft
} from 'lucide-react';
import { useStore } from '@/store/useStore';

// Sidebar Navigation Configuration
const navGroups = [
  {
    title: 'Core',
    items: [
      { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard }
    ]
  },
  {
    title: 'Data',
    items: [
      { name: 'Ingestion', href: '/data/ingestion', icon: Upload },
      { name: 'Cleaning', href: '/data/cleaning', icon: Wand2 },
      { name: 'Feature Engineering', href: '/data/feature-engineering', icon: Layers }
    ]
  },
  {
    title: 'Analysis',
    items: [
      { name: 'Advanced EDA', href: '/analysis/eda', icon: BarChart2 }
    ]
  },
  {
    title: 'Models',
    items: [
      { name: 'AutoML', href: '/models/automl', icon: Cpu },
      { name: 'Explainability', href: '/models/explainability', icon: LineChart }
    ]
  },
  {
    title: 'AI',
    items: [
      { name: 'AI Analyst', href: '/agents/analyst', icon: Bot },
      { name: 'Workflow', href: '/agents/workflow', icon: Workflow }
    ]
  },
  {
    title: 'Management',
    items: [
      { name: 'Reports', href: '/agents/reports', icon: FileTextIcon },
      { name: 'MLOps', href: '/mlops', icon: Activity }
    ]
  }
];

// Helper wrapper for lucide FileText (lucide-react has FileText, let's make sure it imports/maps correctly)
function FileTextIcon(props: any) {
  return <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>;
}

// Reusable CSS Tooltip Wrapper for Collapsed State
function SidebarTooltip({ text, children }: { text: string; children: React.ReactNode }) {
  return (
    <div className="group relative flex items-center w-full">
      {children}
      <div className="absolute left-full ml-3 px-3 py-1.5 bg-[#111827] text-white text-[10px] font-bold uppercase tracking-wider rounded-lg shadow-xl opacity-0 scale-95 pointer-events-none group-hover:opacity-100 group-hover:scale-100 group-hover:pointer-events-auto transition-all duration-150 whitespace-nowrap z-50">
        {text}
        <div className="absolute right-full top-1/2 -translate-y-1/2 border-[4px] border-transparent border-r-[#111827]" />
      </div>
    </div>
  );
}

export default function Sidebar() {
  const pathname = usePathname();
  const { isSidebarOpen, toggleSidebar, workspace } = useStore();
  const [hoveredIdx, setHoveredIdx] = React.useState<string | null>(null);
  const [isMobile, setIsMobile] = React.useState(false);

  React.useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 1024); // lg breakpoint is 1024px
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Active status checker
  const checkActive = (href: string) => {
    return pathname === href;
  };

  const showExpanded = isMobile ? true : isSidebarOpen;

  return (
    <>
      <AnimatePresence>
        {isMobile && isSidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={toggleSidebar}
            className="fixed inset-0 bg-[#111827]/40 backdrop-blur-sm z-40"
          />
        )}
      </AnimatePresence>

      <motion.div
        animate={isMobile ? { x: isSidebarOpen ? 0 : -256 } : { width: isSidebarOpen ? 256 : 72 }}
        initial={isMobile ? { x: -256 } : { width: 256 }}
        transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
        className={`bg-white border-r border-[#E7EAF2] h-full flex flex-col font-sans select-none shadow-[4px_0_24px_rgba(0,0,0,0.003)] ${
          isMobile 
            ? 'fixed left-0 top-0 bottom-0 w-[256px] z-50' 
            : 'relative shrink-0 z-30'
        }`}
      >
        {/* Brand Header */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-[#E7EAF2] flex-shrink-0 overflow-hidden">
          <div className="flex items-center">
            <div className="w-8 h-8 rounded-xl bg-[#5B5CEB] flex items-center justify-center shadow-sm text-white shrink-0">
              <BrainCircuit className="w-4 h-4" />
            </div>
            {showExpanded && (
              <motion.div
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex flex-col ml-3"
              >
                <span className="font-extrabold text-[#111827] text-sm tracking-tight leading-none">Agentix OS</span>
                <span className="text-[9px] text-[#9CA3AF] font-bold uppercase tracking-wider mt-1 leading-none">Data Science System</span>
              </motion.div>
            )}
          </div>

          {/* Collapsible toggle */}
          {showExpanded && (
            <button 
              onClick={toggleSidebar}
              className="p-1.5 hover:bg-[#F8F9FC] border border-transparent hover:border-[#E7EAF2] rounded-lg text-[#6B7280] hover:text-[#111827] cursor-pointer transition-all shrink-0"
              title="Collapse Sidebar"
              aria-label="Collapse Sidebar"
              aria-expanded={isSidebarOpen}
            >
              <PanelLeftClose className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Navigation Scrollable Panel */}
        <div className="flex-1 overflow-y-auto py-4 px-3 space-y-5 scrollbar-thin scrollbar-thumb-[#E7EAF2]">
          
          {/* Render grouped accordion list when expanded */}
          {showExpanded ? (
            navGroups.map((group, idx) => (
              <div key={idx} className="space-y-1.5 text-left">
                <h4 className="px-3 text-[9px] font-bold text-[#9CA3AF] uppercase tracking-wider mb-2 select-none">
                  {group.title}
                </h4>
                <div className="space-y-0.5 relative pl-1">
                  {/* Thin vertical connecting line for groups with multiple items */}
                  {group.items.length > 1 && (
                    <div className="absolute left-[13px] top-2 bottom-2 w-[1px] bg-[#E7EAF2] z-0" />
                  )}
                  
                  {group.items.map((item) => {
                    const isActive = checkActive(item.href);
                    return (
                      <Link key={item.name} href={item.href} onClick={isMobile ? toggleSidebar : undefined} aria-current={isActive ? "page" : undefined}>
                        <div 
                          onMouseEnter={() => setHoveredIdx(item.name)}
                          onMouseLeave={() => setHoveredIdx(null)}
                          className={`flex items-center px-3.5 py-2.5 rounded-xl text-xs group relative overflow-hidden font-bold cursor-pointer z-10 border transition-colors duration-150 ${
                            isActive 
                              ? 'bg-[#F8F9FC] text-[#5B5CEB] border-[#E7EAF2] shadow-[0_2px_8px_rgba(91,92,235,0.03)]' 
                              : 'text-[#6B7280] hover:text-[#111827] border-transparent'
                          }`}
                        >
                          {!isActive && hoveredIdx === item.name && (
                            <motion.div
                              layoutId="sidebarHover"
                              className="absolute inset-0 bg-[#F8F9FC] rounded-xl z-0"
                              initial={{ opacity: 0 }}
                              animate={{ opacity: 1 }}
                              exit={{ opacity: 0 }}
                              transition={{ duration: 0.15, ease: "easeInOut" }}
                            />
                          )}
                          {isActive && (
                            <motion.div 
                              layoutId="activeTabGlow"
                              className="absolute left-0 w-1 h-4 bg-[#5B5CEB] rounded-r-full z-10"
                              initial={false}
                              transition={{ duration: 0.2, ease: "easeOut" }}
                            />
                          )}
                          <item.icon className={`w-4 h-4 mr-3 shrink-0 transition-colors z-10 ${isActive ? 'text-[#5B5CEB]' : 'text-[#9CA3AF] group-hover:text-[#6B7280]'}`} />
                          <span className="z-10">{item.name}</span>
                        </div>
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))
          ) : (
            /* Render simple tool-tipped icon list when collapsed */
            <div className="flex flex-col items-center space-y-2">
              {navGroups.flatMap(g => g.items).map((item) => {
                const isActive = checkActive(item.href);
                return (
                  <SidebarTooltip key={item.name} text={item.name}>
                    <Link href={item.href} className="w-full flex justify-center" aria-current={isActive ? "page" : undefined} aria-label={item.name}>
                      <div 
                        onMouseEnter={() => setHoveredIdx(item.name)}
                        onMouseLeave={() => setHoveredIdx(null)}
                        className={`w-10 h-10 rounded-xl flex items-center justify-center transition-colors duration-150 relative border cursor-pointer ${
                          isActive 
                            ? 'bg-[#F8F9FC] text-[#5B5CEB] border-[#E7EAF2] shadow-sm' 
                            : 'text-[#6B7280] hover:text-[#111827] border-transparent'
                        }`}
                      >
                        {!isActive && hoveredIdx === item.name && (
                          <motion.div
                            layoutId="sidebarHoverCollapsed"
                            className="absolute inset-0 bg-[#F8F9FC] rounded-xl z-0"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.15, ease: "easeInOut" }}
                          />
                        )}
                        {isActive && (
                          <motion.div 
                            layoutId="activeTabGlowCollapsed"
                            className="absolute left-0 w-0.5 h-3 bg-[#5B5CEB] rounded-r-full z-10"
                            transition={{ duration: 0.2, ease: "easeOut" }}
                          />
                        )}
                        <item.icon className={`w-4 h-4 shrink-0 z-10 ${isActive ? 'text-[#5B5CEB]' : 'text-[#9CA3AF]'}`} />
                      </div>
                    </Link>
                  </SidebarTooltip>
                );
              })}
            </div>
          )}
        </div>

        {/* Bottom Section */}
        <div className="p-3 border-t border-[#E7EAF2] flex-shrink-0 space-y-2.5 bg-white">
          
          {/* Settings trigger */}
          {showExpanded ? (
            <Link href="/settings" onClick={isMobile ? toggleSidebar : undefined} aria-current={checkActive('/settings') ? "page" : undefined}>
              <div 
                onMouseEnter={() => setHoveredIdx('settings')}
                onMouseLeave={() => setHoveredIdx(null)}
                className={`flex items-center px-3.5 py-2.5 rounded-xl text-xs font-bold relative group cursor-pointer border transition-colors duration-150 ${
                  checkActive('/settings') 
                    ? 'bg-[#F8F9FC] text-[#5B5CEB] border-[#E7EAF2] shadow-sm' 
                    : 'text-[#6B7280] hover:text-[#111827] border-transparent'
                }`}
              >
                {!checkActive('/settings') && hoveredIdx === 'settings' && (
                  <motion.div
                    layoutId="sidebarHover"
                    className="absolute inset-0 bg-[#F8F9FC] rounded-xl z-0"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.15, ease: "easeInOut" }}
                  />
                )}
                {checkActive('/settings') && (
                  <motion.div 
                    layoutId="activeTabGlow"
                    className="absolute left-0 w-1 h-4 bg-[#5B5CEB] rounded-r-full z-10"
                    transition={{ duration: 0.2, ease: "easeOut" }}
                  />
                )}
                <Settings className={`w-4 h-4 mr-3 shrink-0 z-10 ${checkActive('/settings') ? 'text-[#5B5CEB]' : 'text-[#9CA3AF] group-hover:text-[#6B7280]'}`} />
                <span className="z-10">Settings</span>
              </div>
            </Link>
          ) : (
            <SidebarTooltip text="Settings">
              <Link href="/settings" className="w-full flex justify-center" aria-current={checkActive('/settings') ? "page" : undefined} aria-label="Settings">
                <div 
                  onMouseEnter={() => setHoveredIdx('settings')}
                  onMouseLeave={() => setHoveredIdx(null)}
                  className={`w-10 h-10 rounded-xl flex items-center justify-center relative border cursor-pointer transition-colors duration-150 ${
                    checkActive('/settings') 
                      ? 'bg-[#F8F9FC] text-[#5B5CEB] border-[#E7EAF2]' 
                      : 'text-[#6B7280] hover:text-[#111827] border-transparent'
                  }`}
                >
                  {!checkActive('/settings') && hoveredIdx === 'settings' && (
                    <motion.div
                      layoutId="sidebarHoverCollapsed"
                      className="absolute inset-0 bg-[#F8F9FC] rounded-xl z-0"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      transition={{ duration: 0.15, ease: "easeInOut" }}
                    />
                  )}
                  {checkActive('/settings') && (
                    <motion.div 
                      layoutId="activeTabGlowCollapsed"
                      className="absolute left-0 w-0.5 h-3 bg-[#5B5CEB] rounded-r-full z-10"
                      transition={{ duration: 0.2, ease: "easeOut" }}
                    />
                  )}
                  <Settings className={`w-4 h-4 shrink-0 z-10 ${checkActive('/settings') ? 'text-[#5B5CEB]' : 'text-[#9CA3AF]'}`} />
                </div>
              </Link>
            </SidebarTooltip>
          )}

          {/* Expand Trigger / Workspace selection */}
          {showExpanded ? (
            <div className="flex items-center justify-between px-3 py-2 bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl shadow-[0_2px_8px_rgba(0,0,0,0.002)] hover:border-[#9CA3AF] transition-colors cursor-pointer">
              <div className="flex items-center min-w-0">
                <div className="w-6 h-6 rounded-lg bg-[#5B5CEB] border border-[#5B5CEB]/10 flex items-center justify-center mr-2 shadow-sm shrink-0">
                  <span className="text-[10px] font-extrabold text-white uppercase">{workspace.charAt(0)}</span>
                </div>
                <div className="flex flex-col min-w-0 text-left">
                  <span className="text-[10px] font-extrabold text-[#111827] truncate leading-tight">{workspace}</span>
                  <span className="text-[8px] text-[#9CA3AF] font-bold uppercase mt-0.5 leading-none">v2.1.0-prod</span>
                </div>
              </div>
              <button 
                onClick={toggleSidebar}
                className="p-1 hover:bg-white border border-transparent hover:border-[#E7EAF2] rounded-md text-[#6B7280] cursor-pointer"
                title="Collapse"
                aria-label="Collapse Workspace Selector"
                aria-expanded={isSidebarOpen}
              >
                <ChevronLeft className="w-3.5 h-3.5" />
              </button>
            </div>
          ) : (
            <div className="flex flex-col items-center">
              <SidebarTooltip text={`Workspace: ${workspace}`}>
                <button 
                  onClick={toggleSidebar}
                  className="w-10 h-10 rounded-xl bg-[#F8F9FC] border border-[#E7EAF2] flex items-center justify-center hover:border-[#9CA3AF] transition-all cursor-pointer shadow-sm text-[#5B5CEB]"
                  aria-label="Expand Sidebar"
                  aria-expanded={isSidebarOpen}
                >
                  <PanelLeft className="w-4 h-4" />
                </button>
              </SidebarTooltip>
            </div>
          )}
        </div>
      </motion.div>
    </>
  );
}
