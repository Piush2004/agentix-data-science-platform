"use client";

import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Users, Database, Terminal, Cpu, BarChart3, 
  Trash2, UserCheck, Activity, Server, Search
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { 
  PageContainer, 
  SectionHeader, 
  Card, 
  StatusBadge, 
  LoadingSkeleton, 
  FloatingAIButton 
} from '@/components/ui/design-system';

export default function AdminPage() {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState('telemetry');
  const [searchTerm, setSearchTerm] = useState('');
  
  // 1. Fetch Admin Data from Next.js API
  const { data: adminData, isLoading: adminLoading } = useQuery({
    queryKey: ['adminData'],
    queryFn: async () => {
      const res = await axios.get('/api/admin');
      return res.data.data;
    }
  });

  // 2. Fetch System Health from Python FastAPI API
  const { data: healthData, isLoading: healthLoading } = useQuery({
    queryKey: ['systemHealth'],
    queryFn: async () => {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/system-health`);
      return res.data.data;
    },
    refetchInterval: 3000 // Refresh health parameters every 3s
  });

  // 3. User Role Modification Mutation
  const updateRoleMutation = useMutation({
    mutationFn: async ({ userId, role }: { userId: string, role: string }) => {
      const res = await axios.post('/api/admin', { action: 'update_role', userId, role });
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['adminData'] });
    }
  });

  // 4. User Deletion Mutation
  const deleteUserMutation = useMutation({
    mutationFn: async (userId: string) => {
      const res = await axios.post('/api/admin', { action: 'delete_user', userId });
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['adminData'] });
    }
  });

  // Loading state
  if (adminLoading || healthLoading) {
    return (
      <PageContainer>
        <SectionHeader 
          title="Admin Command Center" 
          description="Monitor cluster health, system telemetry, audit trail, and user memberships."
        />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card hover={false} className="h-40 flex flex-col justify-between">
            <LoadingSkeleton className="h-4 w-1/3" />
            <LoadingSkeleton className="h-10 w-full" />
          </Card>
          <Card hover={false} className="h-40 flex flex-col justify-between">
            <LoadingSkeleton className="h-4 w-1/3" />
            <LoadingSkeleton className="h-10 w-full" />
          </Card>
          <Card hover={false} className="h-40 flex flex-col justify-between">
            <LoadingSkeleton className="h-4 w-1/3" />
            <LoadingSkeleton className="h-10 w-full" />
          </Card>
        </div>
        <Card hover={false} className="h-96">
          <LoadingSkeleton className="h-6 w-1/4 mb-4" />
          <LoadingSkeleton className="h-4 w-full mb-3" />
          <LoadingSkeleton className="h-4 w-[95%] mb-3" />
          <LoadingSkeleton className="h-4 w-[90%] mb-3" />
          <LoadingSkeleton className="h-4 w-[85%]" />
        </Card>
      </PageContainer>
    );
  }

  const { users = [], datasets = [], activityLogs = [], stats = {} } = adminData || {};

  // Filtered users
  const filteredUsers = users.filter((u: any) => 
    u.name?.toLowerCase().includes(searchTerm.toLowerCase()) || 
    u.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Formatted usage stats for Recharts
  const barChartData = [
    { name: 'Users', Count: stats.userCount || 0 },
    { name: 'Datasets', Count: stats.datasetCount || 0 },
    { name: 'Reports', Count: stats.reportCount || 0 },
    { name: 'Sessions', Count: stats.sessionCount || 0 }
  ];

  const actionTabs = (
    <div className="flex flex-wrap items-center gap-1.5 bg-[#F8F9FC] border border-[#E7EAF2] p-1 rounded-xl">
      {[
        { id: 'telemetry', label: 'Cluster Telemetry', icon: Cpu },
        { id: 'users', label: 'User Directory', icon: Users },
        { id: 'datasets', label: 'Datasets Registry', icon: Database },
        { id: 'audit', label: 'Security Audit Logs', icon: Terminal },
        { id: 'usage', label: 'Capacity Metrics', icon: BarChart3 },
      ].map((tab) => (
        <button
          key={tab.id}
          onClick={() => setActiveTab(tab.id)}
          className={`flex items-center px-4 py-2 text-xs font-bold rounded-lg transition-all cursor-pointer ${
            activeTab === tab.id 
              ? 'bg-white text-[#5B5CEB] border border-[#E7EAF2] shadow-sm' 
              : 'text-[#6B7280] hover:text-[#111827]'
          }`}
        >
          <tab.icon className="w-3.5 h-3.5 mr-2" />
          {tab.label}
        </button>
      ))}
    </div>
  );

  return (
    <PageContainer>
      <SectionHeader 
        title="Admin Command Center" 
        description="Monitor cluster health, system telemetry, audit trail, and user memberships."
        actions={actionTabs}
      />

      {/* Content Panels */}
      <div className="min-h-[500px]">
        <AnimatePresence mode="wait">
          
          {/* Panel: Cluster Telemetry */}
          {activeTab === 'telemetry' && (
            <motion.div
              key="telemetry"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              className="space-y-6"
            >
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                
                {/* CPU Health */}
                <Card hover={false} className="flex flex-col justify-between h-40">
                  <div className="flex justify-between items-center mb-4">
                    <span className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider">CPU Utilization</span>
                    <div className="w-8 h-8 rounded-lg bg-[#5B5CEB]/5 border border-[#5B5CEB]/10 flex items-center justify-center text-[#5B5CEB]">
                      <Cpu className="w-4 h-4" />
                    </div>
                  </div>
                  <div>
                    <h2 className="text-3xl font-extrabold tracking-tight text-[#111827]">{healthData?.cpu.toFixed(1)}%</h2>
                    <div className="w-full bg-[#F8F9FC] border border-[#E7EAF2] h-2.5 rounded-full mt-3 overflow-hidden">
                      <div 
                        className="bg-[#5B5CEB] h-full rounded-full transition-all duration-1000" 
                        style={{ width: `${healthData?.cpu}%` }}
                      ></div>
                    </div>
                  </div>
                </Card>

                {/* RAM Health */}
                <Card hover={false} className="flex flex-col justify-between h-40">
                  <div className="flex justify-between items-center mb-4">
                    <span className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider">Memory Allocation</span>
                    <div className="w-8 h-8 rounded-lg bg-purple-500/5 border border-purple-500/10 flex items-center justify-center text-purple-500">
                      <Server className="w-4 h-4" />
                    </div>
                  </div>
                  <div>
                    <h2 className="text-3xl font-extrabold tracking-tight text-[#111827]">{healthData?.ram.toFixed(1)}%</h2>
                    <div className="w-full bg-[#F8F9FC] border border-[#E7EAF2] h-2.5 rounded-full mt-3 overflow-hidden">
                      <div 
                        className="bg-[#9333EA] h-full rounded-full transition-all duration-1000" 
                        style={{ width: `${healthData?.ram}%` }}
                      ></div>
                    </div>
                  </div>
                </Card>

                {/* GPU Health */}
                <Card hover={false} className="flex flex-col justify-between h-40">
                  <div className="flex justify-between items-center mb-4">
                    <span className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider">GPU Cores Load</span>
                    <div className="w-8 h-8 rounded-lg bg-[#16A34A]/5 border border-[#16A34A]/10 flex items-center justify-center text-[#16A34A]">
                      <Activity className="w-4 h-4" />
                    </div>
                  </div>
                  <div>
                    <h2 className="text-3xl font-extrabold tracking-tight text-[#111827]">{healthData?.gpu.toFixed(1)}%</h2>
                    <p className="text-[9px] text-[#9CA3AF] mt-1 font-mono font-bold truncate" title={healthData?.gpu_name}>{healthData?.gpu_name || 'No GPU Active'}</p>
                    <div className="w-full bg-[#F8F9FC] border border-[#E7EAF2] h-2.5 rounded-full mt-2 overflow-hidden">
                      <div 
                        className="bg-[#16A34A] h-full rounded-full transition-all duration-1000" 
                        style={{ width: `${healthData?.gpu}%` }}
                      ></div>
                    </div>
                  </div>
                </Card>

              </div>

              {/* Status Connections */}
              <Card hover={false}>
                <div className="flex justify-between items-center mb-6 pb-3 border-b border-[#E7EAF2]">
                  <h3 className="text-sm font-bold text-[#111827]">SaaS Router Integrity</h3>
                  <StatusBadge status="All Systems Operational" type="success" />
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                  
                  <div className="flex items-center space-x-3.5 p-4 rounded-2xl bg-[#F8F9FC] border border-[#E7EAF2]">
                    <div className="w-2.5 h-2.5 rounded-full bg-[#16A34A] animate-pulse ring-4 ring-[#16A34A]/15"></div>
                    <div>
                      <h4 className="text-xs font-bold text-[#111827]">API Router Swarm</h4>
                      <p className="text-[10px] text-[#6B7280] font-semibold mt-0.5">{healthData?.api_status}</p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3.5 p-4 rounded-2xl bg-[#F8F9FC] border border-[#E7EAF2]">
                    <div className={`w-2.5 h-2.5 rounded-full ring-4 ${healthData?.db_status === 'Online' ? 'bg-[#16A34A] animate-pulse ring-[#16A34A]/15' : 'bg-red-500 ring-red-500/15'}`}></div>
                    <div>
                      <h4 className="text-xs font-bold text-[#111827]">PostgreSQL Schema</h4>
                      <p className="text-[10px] text-[#6B7280] font-semibold mt-0.5">{healthData?.db_status}</p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3.5 p-4 rounded-2xl bg-[#F8F9FC] border border-[#E7EAF2]">
                    <div className="w-2.5 h-2.5 rounded-full bg-[#16A34A] ring-4 ring-[#16A34A]/10"></div>
                    <div>
                      <h4 className="text-xs font-bold text-[#111827]">Queue Swarm Broker</h4>
                      <p className="text-[10px] text-[#6B7280] font-semibold mt-0.5">{healthData?.queue_status}</p>
                    </div>
                  </div>

                </div>
              </Card>
            </motion.div>
          )}

          {/* Panel: Users */}
          {activeTab === 'users' && (
            <motion.div
              key="users"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              className="space-y-6"
            >
              <div className="flex justify-between items-center gap-4">
                <div className="relative w-full max-w-md">
                  <Search className="w-4 h-4 text-[#9CA3AF] absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    placeholder="Search User Directory..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl text-xs font-semibold text-[#111827] focus:outline-none focus:border-[#5B5CEB] focus:ring-1 focus:ring-[#5B5CEB] transition-all"
                  />
                </div>
              </div>

              <Card hover={false} className="p-0 overflow-hidden">
                <table className="w-full text-xs text-left border-collapse">
                  <thead>
                    <tr className="bg-[#F8F9FC] border-b border-[#E7EAF2]">
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">User Profile</th>
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">Role Assignment</th>
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">Authentication Count</th>
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">Last Activity timestamp</th>
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider text-right">Operations</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#E7EAF2] font-semibold text-[#4B5563]">
                    {filteredUsers.map((user: any) => (
                      <tr key={user.id} className="hover:bg-[#F8F9FC]/40 transition-colors">
                        <td className="px-6 py-4 flex items-center space-x-3">
                          <div className="w-8 h-8 rounded-xl bg-[#F8F9FC] border border-[#E7EAF2] flex items-center justify-center font-bold text-[#5B5CEB] overflow-hidden shadow-sm">
                            {user.image ? <img src={user.image} alt={user.name} /> : user.name?.charAt(0) || user.email?.charAt(0)}
                          </div>
                          <div>
                            <p className="font-bold text-[#111827]">{user.name || 'Enterprise User'}</p>
                            <p className="text-[10px] text-[#6B7280] font-medium">{user.email}</p>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <StatusBadge 
                            status={user.role} 
                            type={user.role === 'ADMIN' ? 'error' : 'neutral'} 
                          />
                        </td>
                        <td className="px-6 py-4 font-mono font-bold text-[#111827]">{user.loginCount}</td>
                        <td className="px-6 py-4 text-[#6B7280]">{user.lastLogin ? new Date(user.lastLogin).toLocaleString() : 'Never'}</td>
                        <td className="px-6 py-4 text-right space-x-1 whitespace-nowrap">
                          <button
                            onClick={() => updateRoleMutation.mutate({ userId: user.id, role: user.role === 'ADMIN' ? 'USER' : 'ADMIN' })}
                            className="p-2 text-[#6B7280] hover:text-[#5B5CEB] hover:bg-[#F8F9FC] rounded-xl transition-all border border-transparent hover:border-[#E7EAF2]"
                            title="Toggle Admin Privilege"
                          >
                            <UserCheck className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => {
                              if (confirm('Are you sure you want to delete this user?')) {
                                deleteUserMutation.mutate(user.id);
                              }
                            }}
                            className="p-2 text-[#EF4444] hover:bg-[#FEF2F2] rounded-xl transition-all border border-transparent hover:border-[#EF4444]/10"
                            title="Delete User"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </Card>
            </motion.div>
          )}

          {/* Panel: Datasets Registry */}
          {activeTab === 'datasets' && (
            <motion.div
              key="datasets"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              className="space-y-6"
            >
              <Card hover={false} className="p-0 overflow-hidden">
                <table className="w-full text-xs text-left border-collapse">
                  <thead>
                    <tr className="bg-[#F8F9FC] border-b border-[#E7EAF2]">
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">Dataset Name</th>
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">Uploaded By</th>
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">Dimensions (R / C)</th>
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">Storage size</th>
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">Disk storage URI</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#E7EAF2] font-semibold text-[#4B5563]">
                    {datasets.map((ds: any) => (
                      <tr key={ds.id} className="hover:bg-[#F8F9FC]/40 transition-colors">
                        <td className="px-6 py-4 font-bold text-[#111827]">{ds.name}</td>
                        <td className="px-6 py-4">
                          <p className="font-bold text-[#111827]">{ds.user?.name || 'Owner'}</p>
                          <p className="text-[10px] text-[#6B7280] font-medium">{ds.user?.email}</p>
                        </td>
                        <td className="px-6 py-4 font-mono font-bold text-[#5B5CEB]">
                          {ds.rowCount ?? 'N/A'} R <span className="text-[#9CA3AF]">x</span> {ds.colCount ?? 'N/A'} C
                        </td>
                        <td className="px-6 py-4 font-mono font-bold text-[#111827]">{(ds.sizeBytes / 1024).toFixed(1)} KB</td>
                        <td className="px-6 py-4 font-mono text-[#6B7280] max-w-[220px] truncate" title={ds.storageUrl}>{ds.storageUrl}</td>
                      </tr>
                    ))}
                    {datasets.length === 0 && (
                      <tr>
                        <td colSpan={5} className="px-6 py-12 text-center text-[#9CA3AF] font-bold">No datasets cataloged in storage pools.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </Card>
            </motion.div>
          )}

          {/* Panel: Security Audit Logs */}
          {activeTab === 'audit' && (
            <motion.div
              key="audit"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              className="space-y-6"
            >
              <Card hover={false} className="p-0 overflow-hidden">
                <table className="w-full text-xs text-left border-collapse">
                  <thead>
                    <tr className="bg-[#F8F9FC] border-b border-[#E7EAF2]">
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">Timestamp</th>
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">Action Code</th>
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">User ID</th>
                      <th className="px-6 py-4 font-bold text-[#6B7280] uppercase tracking-wider">Details Payload</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#E7EAF2] font-semibold text-[#4B5563]">
                    {activityLogs.map((log: any) => (
                      <tr key={log.id} className="hover:bg-[#F8F9FC]/40 transition-colors">
                        <td className="px-6 py-4 text-[#6B7280] whitespace-nowrap">{new Date(log.createdAt).toLocaleString()}</td>
                        <td className="px-6 py-4">
                          <StatusBadge 
                            status={log.action} 
                            type={log.action.includes('ERR') || log.action.includes('WARN') ? 'error' : 'success'} 
                          />
                        </td>
                        <td className="px-6 py-4 font-mono text-[#6B7280]">{log.userId}</td>
                        <td className="px-6 py-4 max-w-[320px] truncate text-[#4B5563] font-mono font-medium" title={JSON.stringify(log.metadata)}>
                          {JSON.stringify(log.metadata)}
                        </td>
                      </tr>
                    ))}
                    {activityLogs.length === 0 && (
                      <tr>
                        <td colSpan={4} className="px-6 py-12 text-center text-[#9CA3AF] font-bold">No security audit activity recorded.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </Card>
            </motion.div>
          )}

          {/* Panel: Usage */}
          {activeTab === 'usage' && (
            <motion.div
              key="usage"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
            >
              <Card hover={false}>
                <div className="flex justify-between items-center mb-6 pb-3 border-b border-[#E7EAF2]">
                  <h3 className="text-sm font-bold text-[#111827] flex items-center">
                    <BarChart3 className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Platform Allocation Inventory
                  </h3>
                  <StatusBadge status="All Entities Cataloged" type="neutral" />
                </div>
                <div className="h-96 w-full font-mono text-xs">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={barChartData} margin={{ top: 20, right: 30, left: 10, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E7EAF2" />
                      <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#6B7280', fontSize: 11, fontWeight: 'bold' }} />
                      <YAxis axisLine={false} tickLine={false} tick={{ fill: '#6B7280', fontSize: 11, fontWeight: 'bold' }} />
                      <Tooltip 
                        contentStyle={{ 
                          borderRadius: '12px', 
                          border: '1px solid #E7EAF2', 
                          boxShadow: '0 8px 30px rgba(0,0,0,0.02)',
                          fontSize: '11px',
                          fontWeight: 'bold'
                        }}
                      />
                      <Bar dataKey="Count" fill="#5B5CEB" radius={[6, 6, 0, 0]} maxBarSize={50} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </Card>
            </motion.div>
          )}

        </AnimatePresence>
      </div>

      <FloatingAIButton />
    </PageContainer>
  );
}
