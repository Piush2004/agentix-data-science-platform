"use client";

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, ShieldCheck, TrendingUp, GitBranch, ShieldAlert, 
  ClipboardList, Flame, BarChart3, Clock
} from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { 
  PageContainer, 
  SectionHeader, 
  Card, 
  StatCard, 
  StatusBadge, 
  LoadingSkeleton, 
  FloatingAIButton 
} from '@/components/ui/design-system';

export default function MLOpsPage() {
  const [activeTab, setActiveTab] = useState('registry');

  // 1. Fetch general MLOps metrics
  const { data: mlopsData, isLoading: metricsLoading } = useQuery({
    queryKey: ['mlopsStatus'],
    queryFn: async () => {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/mlops`);
      return res.data.data;
    }
  });

  // 2. Fetch Model Registry
  const { data: registryData, isLoading: registryLoading } = useQuery({
    queryKey: ['modelRegistry'],
    queryFn: async () => {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/model-registry`);
      return res.data.data;
    }
  });

  // 3. Fetch Experiment Runs
  const { data: experimentData, isLoading: experimentLoading } = useQuery({
    queryKey: ['experimentRuns'],
    queryFn: async () => {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/experiment-runs`);
      return res.data.data;
    }
  });

  const isLoading = metricsLoading || registryLoading || experimentLoading;

  const formatChartData = () => {
    if (!mlopsData?.accuracy_trend) return [];
    return mlopsData.accuracy_trend.map((val: number, i: number) => ({
      version: `v${1 + i}.0`,
      accuracy: val
    }));
  };

  const chartData = formatChartData();

  if (isLoading) {
    return (
      <PageContainer>
        <SectionHeader 
          title="MLOps Center" 
          description="Continuous model deployment registry, drift detection, and experiment tracking."
        />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <LoadingSkeleton className="h-40 w-full" />
          <LoadingSkeleton className="h-40 w-full" />
          <LoadingSkeleton className="h-40 w-full" />
          <LoadingSkeleton className="h-40 w-full" />
        </div>
        <Card hover={false} className="h-96">
          <LoadingSkeleton className="h-6 w-1/4 mb-4" />
          <LoadingSkeleton className="h-4 w-full mb-3" />
          <LoadingSkeleton className="h-4 w-[95%] mb-3" />
          <LoadingSkeleton className="h-4 w-[90%] mb-3" />
        </Card>
      </PageContainer>
    );
  }

  const actionTabs = (
    <div className="flex flex-wrap items-center gap-1.5 bg-[#F8F9FC] border border-[#E7EAF2] p-1 rounded-xl">
      <button
        onClick={() => setActiveTab('registry')}
        className={`flex items-center px-4 py-2 text-xs font-bold rounded-lg transition-all cursor-pointer ${
          activeTab === 'registry' ? 'bg-white text-[#5B5CEB] border border-[#E7EAF2] shadow-sm' : 'text-[#6B7280] hover:text-[#111827]'
        }`}
      >
        <GitBranch className="w-3.5 h-3.5 mr-2" />
        Model Registry
      </button>
      <button
        onClick={() => setActiveTab('tracking')}
        className={`flex items-center px-4 py-2 text-xs font-bold rounded-lg transition-all cursor-pointer ${
          activeTab === 'tracking' ? 'bg-white text-[#5B5CEB] border border-[#E7EAF2] shadow-sm' : 'text-[#6B7280] hover:text-[#111827]'
        }`}
      >
        <ClipboardList className="w-3.5 h-3.5 mr-2" />
        Experiment Tracking
      </button>
      <button
        onClick={() => setActiveTab('telemetry')}
        className={`flex items-center px-4 py-2 text-xs font-bold rounded-lg transition-all cursor-pointer ${
          activeTab === 'telemetry' ? 'bg-white text-[#5B5CEB] border border-[#E7EAF2] shadow-sm' : 'text-[#6B7280] hover:text-[#111827]'
        }`}
      >
        <BarChart3 className="w-3.5 h-3.5 mr-2" />
        Accuracy Evolution
      </button>
    </div>
  );

  return (
    <PageContainer>
      <SectionHeader 
        title="MLOps Center" 
        description="Continuous model deployment registry, drift detection, and experiment tracking."
        actions={actionTabs}
      />

      {/* Primary Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <StatCard 
          title="Pipeline Health"
          value={mlopsData?.status || 'Unknown'}
          icon={mlopsData?.status === 'Optimal' ? <ShieldCheck className="w-5 h-5 text-[#16A34A]" /> : <ShieldAlert className="w-5 h-5 text-[#F59E0B]" />}
          trend="Operational Stability"
          trendType={mlopsData?.status === 'Optimal' ? 'success' : 'warning'}
        />

        <StatCard 
          title="Concept Drift"
          value={mlopsData?.drift ? 'Detected' : 'No Drift'}
          icon={<Activity className="w-5 h-5" />}
          trend="Probability Vector"
          trendType={mlopsData?.drift ? 'error' : 'success'}
        />

        <StatCard 
          title="Active Endpoints"
          value={mlopsData?.deployments || 0}
          icon={<GitBranch className="w-5 h-5" />}
          trend="Deployed to Prod"
          trendType="neutral"
        />

        <StatCard 
          title="Peak Accuracy"
          value={mlopsData?.accuracy_trend ? (mlopsData.accuracy_trend[mlopsData.accuracy_trend.length - 1] * 100).toFixed(1) + '%' : 'N/A'}
          icon={<TrendingUp className="w-5 h-5" />}
          trend="Test Validation"
          trendType="success"
        />

      </div>

      {/* Panels */}
      <div className="min-h-[400px]">
        <AnimatePresence mode="wait">
          
          {/* Tab: Model Registry */}
          {activeTab === 'registry' && (
            <motion.div
              key="registry"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              className="space-y-6"
            >
              <Card hover={false} className="p-0 overflow-hidden">
                <div className="p-5 border-b border-[#E7EAF2] flex justify-between items-center bg-[#F8F9FC]">
                  <h3 className="text-sm font-bold text-[#111827] flex items-center">
                    <GitBranch className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Registered Core Models
                  </h3>
                  <StatusBadge status={`${registryData?.length || 0} Models`} type="neutral" />
                </div>
                <div className="divide-y divide-[#E7EAF2]">
                  {registryData?.map((model: any) => (
                    <div key={model.id} className="p-6 space-y-4">
                      <div className="flex justify-between items-center">
                        <div>
                          <h3 className="text-sm font-bold text-[#111827]">{model.name}</h3>
                          <p className="text-[10px] text-[#6B7280] font-bold uppercase tracking-wider mt-0.5">Algorithm: <span className="text-[#111827] font-extrabold">{model.algorithm}</span></p>
                        </div>
                        <span className="px-2.5 py-1 rounded-lg text-[10px] font-mono font-bold bg-[#F8F9FC] text-[#4B5563] border border-[#E7EAF2]">
                          {model.id}
                        </span>
                      </div>

                      {/* Versions List */}
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {model.versions.map((ver: any, vIdx: number) => {
                          const isProd = ver.deploymentStatus === 'Production';
                          const isStaging = ver.deploymentStatus === 'Staging';
                          
                          return (
                            <div key={vIdx} className="p-4 rounded-2xl bg-[#F8F9FC] border border-[#E7EAF2] space-y-3 hover:border-[#5B5CEB]/30 hover:bg-white transition-all relative shadow-[0_4px_20px_rgba(0,0,0,0.002)]">
                              <div className="flex justify-between items-center">
                                <span className="text-xs font-bold text-[#111827]">{ver.version}</span>
                                <StatusBadge 
                                  status={ver.deploymentStatus} 
                                  type={isProd ? 'success' : isStaging ? 'warning' : 'neutral'} 
                                />
                              </div>
                              
                              <div className="space-y-1.5 pt-1">
                                {Object.entries(ver.metrics).map(([mName, mVal]: any) => (
                                  <div key={mName} className="flex justify-between text-[11px] font-mono font-medium">
                                    <span className="text-[#6B7280]">{mName}:</span>
                                    <span className="font-bold text-[#111827]">{typeof mVal === 'number' ? mVal.toFixed(4) : mVal}</span>
                                  </div>
                                ))}
                              </div>

                              <div className="text-[10px] text-[#9CA3AF] pt-2 border-t border-[#E7EAF2] font-mono font-bold flex items-center">
                                <Clock className="w-3 h-3 mr-1" /> {new Date(ver.createdAt).toLocaleDateString()}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </motion.div>
          )}

          {/* Tab: Experiment Tracking */}
          {activeTab === 'tracking' && (
            <motion.div
              key="tracking"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              className="space-y-6"
            >
              <Card hover={false} className="p-0 overflow-hidden">
                <div className="p-5 border-b border-[#E7EAF2] flex justify-between items-center bg-[#F8F9FC]">
                  <h3 className="text-sm font-bold text-[#111827] flex items-center">
                    <ClipboardList className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Hyperparameter Trial Runs
                  </h3>
                  <StatusBadge status={`${experimentData?.length || 0} Runs`} type="neutral" />
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left border-collapse">
                    <thead className="bg-[#F8F9FC] text-[#6B7280] uppercase tracking-wider border-b border-[#E7EAF2]">
                      <tr>
                        <th className="px-6 py-4 font-bold">Experiment Run Name</th>
                        <th className="px-6 py-4 font-bold">Status</th>
                        <th className="px-6 py-4 font-bold">Parameters Space</th>
                        <th className="px-6 py-4 font-bold">Metrics Evaluation</th>
                        <th className="px-6 py-4 font-bold">Duration</th>
                        <th className="px-6 py-4 font-bold">Execution Date</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#E7EAF2] font-medium text-[#4B5563]">
                      {experimentData?.map((run: any) => (
                        <tr key={run.id} className="hover:bg-[#F8F9FC]/40 transition-colors">
                          <td className="px-6 py-4">
                            <div className="flex items-center space-x-2">
                              <span className="font-bold text-[#111827]">{run.name}</span>
                              {run.isBestModel && (
                                <span className="px-2 py-0.5 rounded text-[8px] font-bold uppercase tracking-wider bg-[#F59E0B] text-white flex items-center shadow-sm">
                                  <Flame className="w-2.5 h-2.5 mr-0.5 fill-white" /> Best Model
                                </span>
                              )}
                            </div>
                            <span className="text-[10px] text-[#9CA3AF] font-mono">{run.id}</span>
                          </td>
                          <td className="px-6 py-4">
                            <StatusBadge status={run.status} type="success" />
                          </td>
                          <td className="px-6 py-4 font-mono text-[#4B5563]">
                            {Object.entries(run.parameters).map(([k, v]: any) => (
                              <div key={k}>{k}={v}</div>
                            ))}
                          </td>
                          <td className="px-6 py-4 font-mono font-bold text-[#111827]">
                            {Object.entries(run.metrics).map(([k, v]: any) => (
                              <div key={k}>{k}: {v}</div>
                            ))}
                          </td>
                          <td className="px-6 py-4 font-semibold text-[#4B5563]">{run.durationSecs}s</td>
                          <td className="px-6 py-4 text-[#6B7280]">{new Date(run.createdAt).toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>
            </motion.div>
          )}

          {/* Tab: Accuracy Evolution */}
          {activeTab === 'telemetry' && (
            <motion.div
              key="telemetry"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
            >
              <Card hover={false}>
                <div className="flex justify-between items-center mb-6 pb-3 border-b border-[#E7EAF2]">
                  <h3 className="text-sm font-bold text-[#111827] flex items-center">
                    <BarChart3 className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Accuracy Evolution History
                  </h3>
                  <StatusBadge status="Continuous Improvement" type="success" />
                </div>
                <div className="h-80 w-full mt-4 font-mono text-xs">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                      <defs>
                        <linearGradient id="colorAcc" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#5B5CEB" stopOpacity={0.2}/>
                          <stop offset="95%" stopColor="#5B5CEB" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <XAxis dataKey="version" axisLine={false} tickLine={false} tick={{ fill: '#6B7280', fontSize: 11, fontWeight: 'bold' }} dy={10} />
                      <YAxis domain={['auto', 'auto']} axisLine={false} tickLine={false} tick={{ fill: '#6B7280', fontSize: 11, fontWeight: 'bold' }} dx={-10} tickFormatter={(val) => val.toFixed(2)} />
                      <Tooltip 
                        contentStyle={{ 
                          borderRadius: '12px', 
                          border: '1px solid #E7EAF2', 
                          boxShadow: '0 8px 30px rgba(0,0,0,0.02)',
                          fontSize: '11px',
                          fontWeight: 'bold'
                        }}
                      />
                      <Area type="monotone" dataKey="accuracy" stroke="#5B5CEB" strokeWidth={3} fillOpacity={1} fill="url(#colorAcc)" />
                    </AreaChart>
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
