"use client";

import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { 
  User, Palette, Shield, Terminal, Download, Trash2, 
  Database, Monitor, Moon, Plus, Trash, Globe, AlertTriangle, ChevronRight
} from 'lucide-react';
import { useStore } from '@/store/useStore';
import { useSession } from 'next-auth/react';
import { 
  PageContainer, 
  SectionHeader, 
  Card, 
  StatusBadge, 
  GradientButton, 
  FloatingAIButton,
  LoadingSkeleton 
} from '@/components/ui/design-system';

export default function SettingsPage() {
  const queryClient = useQueryClient();
  const { data: session } = useSession();
  const { theme, toggleTheme } = useStore();
  const [activeTab, setActiveTab] = useState('profile');
  
  // States for Workspace Management
  const [wsName, setWsName] = useState('');
  const [wsType, setWsType] = useState('TEAM');
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState('VIEWER');
  
  // 1. Query workspaces and members
  const { data: workspaces = [] } = useQuery({
    queryKey: ['workspaces'],
    queryFn: async () => {
      const res = await axios.get('/api/workspaces');
      return res.data.workspaces;
    }
  });

  const activeWs = workspaces[0] || null;

  // 2. Query active sessions
  const { data: sessionHistory = [], isLoading: sessionsLoading } = useQuery({
    queryKey: ['sessions'],
    queryFn: async () => {
      const res = await axios.get('/api/sessions');
      return res.data.sessions;
    }
  });

  // 3. Query audit logs
  const { data: auditLogs = [], isLoading: auditLoading } = useQuery({
    queryKey: ['auditLogs'],
    queryFn: async () => {
      const res = await axios.get('/api/activity-logs');
      return res.data.logs;
    }
  });

  // Workspace Mutations
  const createWsMutation = useMutation({
    mutationFn: async () => {
      await axios.post('/api/workspaces', { action: 'create', name: wsName, type: wsType });
    },
    onSuccess: () => {
      setWsName('');
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
    }
  });

  const inviteMemberMutation = useMutation({
    mutationFn: async () => {
      await axios.post('/api/workspaces', { 
        action: 'add_member', 
        workspaceId: activeWs.id, 
        email: inviteEmail, 
        role: inviteRole 
      });
    },
    onSuccess: () => {
      setInviteEmail('');
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
    }
  });

  const updateMemberRoleMutation = useMutation({
    mutationFn: async ({ memberId, role }: { memberId: string, role: string }) => {
      await axios.post('/api/workspaces', { action: 'update_role', memberId, role });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
    }
  });

  const removeMemberMutation = useMutation({
    mutationFn: async (memberId: string) => {
      await axios.post('/api/workspaces', { action: 'remove_member', memberId });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
    }
  });

  // Session Revocation Mutation
  const revokeSessionMutation = useMutation({
    mutationFn: async (sessionId: string) => {
      await axios.delete('/api/sessions', { data: { sessionId } });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sessions'] });
    }
  });

  const tabs = [
    { id: 'profile', label: 'Account & Profile', icon: User },
    { id: 'workspace', label: 'Workspace & RBAC', icon: Database },
    { id: 'appearance', label: 'Appearance & Language', icon: Palette },
    { id: 'security', label: 'Active Sessions', icon: Shield },
    { id: 'audit', label: 'Audit Logs', icon: Terminal },
    { id: 'danger', label: 'Data Management', icon: AlertTriangle },
  ];

  return (
    <PageContainer>
      <SectionHeader 
        title="System Settings" 
        description="Configure personal settings, organization roles, visual aesthetics, and active session logins."
      />

      <div className="flex flex-col lg:flex-row gap-8 items-start">
        
        {/* Navigation Sidebar */}
        <div className="w-full lg:w-64 flex-shrink-0 space-y-1 bg-white border border-[#E7EAF2] p-2.5 rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.005)]">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`w-full flex items-center px-4 py-3 rounded-xl transition-all text-xs font-bold cursor-pointer border ${
                activeTab === tab.id 
                  ? 'bg-[#F8F9FC] text-[#5B5CEB] border-[#E7EAF2] shadow-sm' 
                  : 'text-[#6B7280] hover:bg-[#F8F9FC] hover:text-[#111827] border-transparent'
              }`}
            >
              <tab.icon className={`w-4 h-4 mr-3 ${activeTab === tab.id ? 'text-[#5B5CEB]' : 'text-[#9CA3AF]'}`} />
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Content View */}
        <div className="flex-1 w-full">
          <Card hover={false} className="min-h-[550px] p-6 md:p-8">
            
            {/* Tab: Profile */}
            {activeTab === 'profile' && (
              <div className="space-y-8 animate-in fade-in duration-200">
                <div className="border-b border-[#E7EAF2] pb-4">
                  <h2 className="text-base font-bold text-[#111827]">Profile Settings</h2>
                  <p className="text-xs text-[#6B7280] font-medium">Update metadata regarding your user profile.</p>
                </div>
                
                <div className="flex items-center space-x-6">
                  <div className="w-16 h-16 rounded-2xl bg-[#F8F9FC] flex items-center justify-center border border-[#E7EAF2] overflow-hidden shadow-sm">
                    {session?.user?.image ? (
                      <img src={session.user.image} alt="Avatar" className="w-full h-full object-cover" />
                    ) : (
                      <User className="w-6 h-6 text-[#9CA3AF]" />
                    )}
                  </div>
                  <div className="space-y-1">
                    <button className="px-4 py-2 bg-white hover:bg-[#F8F9FC] text-[#111827] rounded-xl text-xs font-bold transition-all border border-[#E7EAF2] shadow-sm cursor-pointer">
                      Upload Avatar Image
                    </button>
                    <p className="text-[10px] text-[#9CA3AF] font-semibold uppercase tracking-wider">JPG, PNG or GIF. Max 2MB.</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
                  <div className="space-y-2">
                    <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider">Account Name</label>
                    <input 
                      type="text" 
                      defaultValue={session?.user?.name || 'Enterprise User'} 
                      className="w-full bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl px-4 py-3 text-xs font-bold text-[#111827] focus:outline-none focus:border-[#5B5CEB] focus:ring-1 focus:ring-[#5B5CEB] transition-all" 
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider">Primary Email Address</label>
                    <input 
                      type="email" 
                      defaultValue={session?.user?.email || 'admin@agentix.com'} 
                      className="w-full bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl px-4 py-3 text-xs font-bold text-[#111827] focus:outline-none focus:border-[#5B5CEB] focus:ring-1 focus:ring-[#5B5CEB] transition-all" 
                    />
                  </div>
                </div>

                <GradientButton className="px-6 py-3">
                  Save Profile Configuration
                </GradientButton>
              </div>
            )}

            {/* Tab: Workspace & RBAC */}
            {activeTab === 'workspace' && (
              <div className="space-y-8 animate-in fade-in duration-200">
                <div className="border-b border-[#E7EAF2] pb-4">
                  <h2 className="text-base font-bold text-[#111827]">Workspace & RBAC</h2>
                  <p className="text-xs text-[#6B7280] font-medium">Switch workspace types and define member roles (Admin, Editor, Viewer).</p>
                </div>

                {/* Members Registry */}
                {activeWs && (
                  <div className="space-y-4">
                    <h3 className="text-xs font-bold text-[#111827]">Members in "{activeWs.name}" ({activeWs.members.length})</h3>

                    <div className="border border-[#E7EAF2] rounded-2xl overflow-hidden divide-y divide-[#E7EAF2] shadow-[0_4px_20px_rgba(0,0,0,0.005)]">
                      {activeWs.members.map((member: any) => (
                        <div key={member.id} className="p-4 flex items-center justify-between bg-white text-xs">
                          <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 rounded-xl bg-[#F8F9FC] border border-[#E7EAF2] flex items-center justify-center font-bold text-[#5B5CEB] shadow-sm">
                              {member.name.charAt(0)}
                            </div>
                            <div>
                              <p className="font-bold text-[#111827]">{member.name}</p>
                              <p className="text-[10px] text-[#6B7280] font-medium">{member.email}</p>
                            </div>
                          </div>

                          <div className="flex items-center space-x-3">
                            <div className="relative flex items-center">
                              <select
                                value={member.role}
                                onChange={(e) => updateMemberRoleMutation.mutate({ memberId: member.id, role: e.target.value })}
                                className="bg-[#F8F9FC] border border-[#E7EAF2] rounded-lg px-2.5 py-1.5 focus:outline-none text-[11px] font-bold text-[#4B5563] appearance-none pr-6 cursor-pointer"
                                disabled={member.userId === session?.user?.id} // disable modifying self role
                              >
                                <option value="ADMIN">Admin</option>
                                <option value="EDITOR">Editor</option>
                                <option value="VIEWER">Viewer</option>
                              </select>
                              <ChevronRight className="w-3.5 h-3.5 text-[#9CA3AF] pointer-events-none absolute right-1 rotate-90" />
                            </div>

                            {member.userId !== session?.user?.id && (
                              <button 
                                onClick={() => removeMemberMutation.mutate(member.id)}
                                className="p-2 text-[#EF4444] hover:bg-[#FEF2F2] rounded-xl transition-all cursor-pointer border border-transparent hover:border-[#EF4444]/10"
                                title="Revoke Membership"
                              >
                                <Trash className="w-3.5 h-3.5" />
                              </button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Invite User */}
                <div className="p-6 rounded-2xl bg-[#F8F9FC] border border-[#E7EAF2] space-y-4">
                  <h3 className="text-[10px] font-bold text-[#111827] uppercase tracking-wider">Invite Colleague to Workspace</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
                    <div className="space-y-1.5">
                      <label className="text-[9px] font-bold text-[#6B7280] uppercase tracking-wider">Email Address</label>
                      <input
                        type="email"
                        placeholder="colleague@company.com"
                        value={inviteEmail}
                        onChange={(e) => setInviteEmail(e.target.value)}
                        className="w-full bg-white border border-[#E7EAF2] rounded-xl px-3 py-2.5 text-xs font-medium focus:outline-none focus:border-[#5B5CEB]"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-[9px] font-bold text-[#6B7280] uppercase tracking-wider">Role Assignment</label>
                      <div className="relative">
                        <select
                          value={inviteRole}
                          onChange={(e) => setInviteRole(e.target.value)}
                          className="w-full bg-white border border-[#E7EAF2] rounded-xl px-3 py-2.5 text-xs font-bold text-[#4B5563] appearance-none pr-6 focus:outline-none"
                        >
                          <option value="ADMIN">Admin</option>
                          <option value="EDITOR">Editor</option>
                          <option value="VIEWER">Viewer</option>
                        </select>
                        <ChevronRight className="w-3.5 h-3.5 text-[#9CA3AF] pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 rotate-90" />
                      </div>
                    </div>
                    <button
                      onClick={() => inviteMemberMutation.mutate()}
                      className="px-4 py-2.5 bg-[#5B5CEB] text-white rounded-xl text-xs font-bold hover:bg-[#4E4FD6] active:scale-98 flex items-center justify-center space-x-1.5 cursor-pointer shadow-sm h-[38px] transition-all"
                    >
                      <Plus className="w-4 h-4" /> <span>Invite User</span>
                    </button>
                  </div>
                </div>

                {/* Create Workspace */}
                <div className="p-6 rounded-2xl bg-white border border-[#E7EAF2] space-y-4">
                  <h3 className="text-[10px] font-bold text-[#111827] uppercase tracking-wider">Provision New Workspace</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
                    <div className="space-y-1.5">
                      <label className="text-[9px] font-bold text-[#6B7280] uppercase tracking-wider">Workspace Name</label>
                      <input
                        type="text"
                        placeholder="Workspace Name (e.g. Sales Team)"
                        value={wsName}
                        onChange={(e) => setWsName(e.target.value)}
                        className="w-full bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl px-3 py-2.5 text-xs font-medium focus:outline-none focus:border-[#5B5CEB]"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-[9px] font-bold text-[#6B7280] uppercase tracking-wider">Scope Type</label>
                      <div className="relative">
                        <select
                          value={wsType}
                          onChange={(e) => setWsType(e.target.value)}
                          className="w-full bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl px-3 py-2.5 text-xs font-bold text-[#4B5563] appearance-none pr-6 focus:outline-none"
                        >
                          <option value="PERSONAL">Personal Workspace</option>
                          <option value="TEAM">Team Workspace</option>
                          <option value="ORGANIZATION">Organization Workspace</option>
                        </select>
                        <ChevronRight className="w-3.5 h-3.5 text-[#9CA3AF] pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 rotate-90" />
                      </div>
                    </div>
                    <button
                      onClick={() => createWsMutation.mutate()}
                      className="px-4 py-2.5 bg-[#111827] text-white rounded-xl text-xs font-bold hover:bg-[#1f2937] active:scale-98 flex items-center justify-center space-x-1.5 cursor-pointer shadow-sm h-[38px] transition-all"
                    >
                      <Plus className="w-4 h-4" /> <span>Create Workspace</span>
                    </button>
                  </div>
                </div>

              </div>
            )}

            {/* Tab: Appearance & Language */}
            {activeTab === 'appearance' && (
              <div className="space-y-8 animate-in fade-in duration-200">
                <div className="border-b border-[#E7EAF2] pb-4">
                  <h2 className="text-base font-bold text-[#111827]">Visual Aesthetics & Localizations</h2>
                  <p className="text-xs text-[#6B7280] font-medium">Manage styling theme configurations and local language selections.</p>
                </div>

                {/* Theme Settings */}
                <div className="space-y-4">
                  <h3 className="text-xs font-bold text-[#111827] uppercase tracking-wider">Theme Mode Selection</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <button 
                      onClick={toggleTheme}
                      className={`p-5 rounded-2xl border flex flex-col items-center justify-center space-y-2.5 transition-all cursor-pointer ${
                        theme === 'light' 
                          ? 'bg-[#F8F9FC] border-[#5B5CEB] text-[#5B5CEB] shadow-sm font-extrabold' 
                          : 'bg-white border-[#E7EAF2] text-[#6B7280] hover:bg-[#F8F9FC]'
                      }`}
                    >
                      <Monitor className="w-5 h-5" />
                      <span className="text-xs font-bold">Light Aesthetic</span>
                    </button>
                    <button 
                      onClick={toggleTheme}
                      className={`p-5 rounded-2xl border flex flex-col items-center justify-center space-y-2.5 transition-all cursor-pointer ${
                        theme === 'dark' 
                          ? 'bg-[#F8F9FC] border-[#5B5CEB] text-[#5B5CEB] shadow-sm font-extrabold' 
                          : 'bg-white border-[#E7EAF2] text-[#6B7280] hover:bg-[#F8F9FC]'
                      }`}
                    >
                      <Moon className="w-5 h-5" />
                      <span className="text-xs font-bold">Dark Mode (Beta)</span>
                    </button>
                  </div>
                </div>

                {/* Language Selection */}
                <div className="space-y-2">
                  <h3 className="text-xs font-bold text-[#111827] uppercase tracking-wider flex items-center"><Globe className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Language Localization</h3>
                  <div className="relative">
                    <select className="w-full bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl px-4 py-3 text-xs font-bold text-[#4B5563] appearance-none pr-8 cursor-pointer focus:outline-none focus:border-[#5B5CEB]">
                      <option value="en">English (US) - Primary</option>
                      <option value="es">Español</option>
                      <option value="de">Deutsch</option>
                      <option value="fr">Français</option>
                    </select>
                    <ChevronRight className="w-4 h-4 text-[#9CA3AF] pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 rotate-90" />
                  </div>
                </div>

              </div>
            )}

            {/* Tab: Active Sessions */}
            {activeTab === 'security' && (
              <div className="space-y-8 animate-in fade-in duration-200">
                <div className="border-b border-[#E7EAF2] pb-4">
                  <h2 className="text-base font-bold text-[#111827]">Active Login Sessions</h2>
                  <p className="text-xs text-[#6B7280] font-medium">View currently logged-in sessions and terminate active authorization grants.</p>
                </div>

                <div className="space-y-4">
                  {sessionsLoading ? (
                    <div className="space-y-3">
                      <LoadingSkeleton className="h-16 w-full" />
                      <LoadingSkeleton className="h-16 w-full" />
                    </div>
                  ) : (
                    <div className="border border-[#E7EAF2] rounded-2xl overflow-hidden divide-y divide-[#E7EAF2] shadow-[0_4px_20px_rgba(0,0,0,0.002)]">
                      {sessionHistory.map((s: any) => (
                        <div key={s.id} className="p-5 flex justify-between items-center bg-white text-xs">
                          <div className="space-y-1">
                            <div className="flex items-center space-x-2">
                              <span className="font-bold text-[#111827]">{s.deviceType || 'Unknown Device'}</span>
                              {s.ipAddress === '127.0.0.1' && (
                                <StatusBadge status="CURRENT SESSION" type="success" />
                              )}
                            </div>
                            <p className="text-[10px] text-[#6B7280] font-mono font-semibold">IP Address: {s.ipAddress || 'Unknown'}</p>
                            <p className="text-[9px] text-[#9CA3AF] max-w-sm truncate font-semibold">{s.userAgent}</p>
                          </div>

                          <div className="flex items-center space-x-3">
                            <span className="text-[10px] text-[#6B7280] font-bold uppercase tracking-wider">Active: {new Date(s.lastActive).toLocaleTimeString()}</span>
                            {s.ipAddress !== '127.0.0.1' && (
                              <button
                                onClick={() => revokeSessionMutation.mutate(s.id)}
                                className="px-3 py-1.5 text-[#EF4444] border border-[#EF4444]/20 hover:bg-[#FEF2F2] rounded-lg text-[10px] font-bold transition-all cursor-pointer"
                              >
                                Terminate
                              </button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Tab: Security Audit Logs */}
            {activeTab === 'audit' && (
              <div className="space-y-8 animate-in fade-in duration-200">
                <div className="border-b border-[#E7EAF2] pb-4">
                  <h2 className="text-base font-bold text-[#111827]">Security Audit Timeline</h2>
                  <p className="text-xs text-[#6B7280] font-medium">Full audit trail recording actions taken in this account context.</p>
                </div>

                <div className="space-y-6">
                  {auditLoading ? (
                    <div className="space-y-4">
                      <LoadingSkeleton className="h-8 w-full" />
                      <LoadingSkeleton className="h-8 w-[90%]" />
                      <LoadingSkeleton className="h-8 w-[80%]" />
                    </div>
                  ) : (
                    <div className="space-y-6 relative pl-4">
                      {/* Vertical line connecting logs */}
                      <div className="absolute top-2 bottom-2 left-[5px] border-l-2 border-[#E7EAF2] z-0" />
                      
                      {auditLogs.map((log: any) => (
                        <div key={log.id} className="relative z-10 space-y-1.5">
                          <div className="absolute w-2.5 h-2.5 bg-[#5B5CEB] rounded-full -left-[15px] top-1 border-2 border-white ring-4 ring-[#5B5CEB]/10 animate-pulse" />
                          <div className="flex items-center space-x-2">
                            <span className="text-[9px] text-[#9CA3AF] font-mono font-bold">{new Date(log.createdAt).toLocaleString()}</span>
                            <StatusBadge status="AUDIT" type="neutral" />
                          </div>
                          <p className="text-xs font-bold text-[#111827]">{log.action}</p>
                          <p className="text-[10px] text-[#6B7280] font-mono font-medium leading-relaxed bg-[#F8F9FC] border border-[#E7EAF2] p-2.5 rounded-xl max-w-2xl">{JSON.stringify(log.metadata)}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Tab: Data Management */}
            {activeTab === 'danger' && (
              <div className="space-y-8 animate-in fade-in duration-200">
                <div className="border-b border-[#E7EAF2] pb-4">
                  <h2 className="text-base font-bold text-[#111827]">Data Portability & Management</h2>
                  <p className="text-xs text-[#6B7280] font-medium">Download your datasets/metadata, or permanently delete your user account.</p>
                </div>

                <div className="space-y-6">
                  
                  <div className="p-5 rounded-2xl border border-[#E7EAF2] flex flex-col sm:flex-row justify-between sm:items-center gap-4 bg-[#F8F9FC]">
                    <div className="space-y-1">
                      <h3 className="text-xs font-bold text-[#111827] uppercase tracking-wider flex items-center"><Download className="w-4 h-4 mr-1.5 text-[#5B5CEB]" /> Download Account Data</h3>
                      <p className="text-xs text-[#6B7280] font-medium max-w-md leading-relaxed">Request a full archive containing your uploaded datasets, SQL models, hyperparameter leaderboards, and AI agent chat history.</p>
                    </div>
                    <button className="px-4 py-2.5 bg-white border border-[#E7EAF2] hover:bg-[#F8F9FC] rounded-xl text-xs font-bold text-[#111827] shadow-sm flex items-center justify-center space-x-1.5 cursor-pointer shrink-0 transition-all">
                      <Download className="w-3.5 h-3.5 text-[#5B5CEB]" /> <span>Request Archive</span>
                    </button>
                  </div>

                  <div className="p-5 rounded-2xl border border-[#EF4444]/20 flex flex-col sm:flex-row justify-between sm:items-center gap-4 bg-[#FEF2F2]/30">
                    <div className="space-y-1">
                      <h3 className="text-xs font-bold text-[#EF4444] uppercase tracking-wider flex items-center"><Trash2 className="w-4 h-4 mr-1.5 text-[#EF4444]" /> Delete User Account</h3>
                      <p className="text-xs text-red-700/80 font-medium max-w-md leading-relaxed">Permanently delete your profile workspace, neural weights, and configurations. This operation is absolute and cannot be recovered.</p>
                    </div>
                    <button className="px-4 py-2.5 bg-[#EF4444] hover:bg-[#DC2626] text-white rounded-xl text-xs font-bold shadow-sm flex items-center justify-center space-x-1.5 cursor-pointer shrink-0 active:scale-98 transition-all">
                      <Trash2 className="w-3.5 h-3.5" /> <span>Delete Account</span>
                    </button>
                  </div>

                </div>
              </div>
            )}

          </Card>
        </div>
      </div>

      <FloatingAIButton />
    </PageContainer>
  );
}
