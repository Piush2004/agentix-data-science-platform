"use client";

import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { Cpu, Trophy, Activity, ArrowRight, Loader2, Target, Sliders, Layers, ChevronRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  PageContainer, 
  SectionHeader, 
  Card, 
  EmptyState, 
  StatusBadge, 
  GradientButton, 
  AgentStatusLoader,
  FloatingAIButton 
} from '@/components/ui/design-system';
import Link from 'next/link';

export default function AutoMLPage() {
  const queryClient = useQueryClient();
  const [selectedDataset, setSelectedDataset] = useState<string | null>(null);
  const [targetCol, setTargetCol] = useState<string>('');
  const [automlStats, setAutomlStats] = useState<any>(null);
  const [trainingLogs, setTrainingLogs] = useState<string[]>([]);

  const { data: history } = useQuery({
    queryKey: ['datasetHistory'],
    queryFn: async () => {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/dataset/history`);
      const hist = res.data.history;
      if (hist && hist.length > 0 && !selectedDataset) {
        setSelectedDataset(hist[hist.length - 1].name);
      }
      return hist;
    }
  });

  const { data: profile } = useQuery({
    queryKey: ['datasetProfile', selectedDataset],
    queryFn: async () => {
      if (!selectedDataset) return null;
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/profile`, { dataset_name: selectedDataset });
      if (res.data.data.schema) {
        const cols = Object.keys(res.data.data.schema);
        if (cols.length > 0 && !targetCol) setTargetCol(cols[cols.length - 1]);
      }
      return res.data.data;
    },
    enabled: !!selectedDataset
  });

  const trainMutation = useMutation({
    mutationFn: async () => {
      if (!selectedDataset) throw new Error("No dataset selected");
      setTrainingLogs(["[AutoML] Initializing distributed training cluster...", "[AutoML] Searching hyperparameter space...", "[AutoML] Running Cross-Validation splits..."]);
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/predict`, { 
        dataset_name: selectedDataset,
        target_column: targetCol
      });
      return res.data.data;
    },
    onSuccess: (data) => {
      setAutomlStats(data);
      setTrainingLogs(prev => [...prev, "[AutoML] Training complete.", `[AutoML] Champion model deployed: ${data.best_model}`]);
      queryClient.invalidateQueries({ queryKey: ['dashboardMetrics'] });
    }
  });

  if (history && history.length === 0) {
    return (
      <PageContainer>
        <SectionHeader 
          title="AutoML Training" 
          description="Train and evaluate multiple models simultaneously with intelligent hyperparameter tuning."
        />
        <div className="py-12">
          <EmptyState 
            title="No Datasets Uploaded" 
            description="You must ingest a dataset in your workspace memory before training machine learning models."
            type="neural-network"
            primaryAction={{
              label: "Ingest Spreadsheets",
              onClick: () => {
                window.location.href = "/data/ingestion";
              }
            }}
            secondaryAction={{
              label: "Return to Dashboard",
              onClick: () => {
                window.location.href = "/dashboard";
              }
            }}
          />
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <SectionHeader 
        title="AutoML Training" 
        description="Train and evaluate multiple models simultaneously with intelligent hyperparameter tuning."
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        
        {/* Left Column: Configuration */}
        <div className="lg:col-span-1 space-y-6">
          <Card hover={false}>
            <h3 className="text-sm font-bold text-[#111827] mb-5 border-b border-[#E7EAF2] pb-3 flex items-center">
              <Sliders className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Training Configuration
            </h3>
            
            <div className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider">
                  Training Dataset
                </label>
                <div className="relative">
                  <select 
                    value={selectedDataset || ""} 
                    onChange={(e) => {
                      setSelectedDataset(e.target.value);
                      setAutomlStats(null);
                      setTrainingLogs([]);
                    }}
                    className="w-full bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl px-4 py-3 text-sm text-[#111827] focus:outline-none focus:border-[#5B5CEB] focus:ring-1 focus:ring-[#5B5CEB] transition-all appearance-none cursor-pointer font-medium"
                  >
                    <option value="" disabled>Select a dataset</option>
                    {history?.map((d: any, i: number) => (
                      <option key={i} value={d.name}>{d.name}</option>
                    ))}
                  </select>
                  <ChevronRight className="w-4 h-4 text-[#9CA3AF] pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 rotate-90" />
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider">
                  Target Variable (Y)
                </label>
                <div className="relative">
                  <select 
                    value={targetCol} 
                    onChange={(e) => setTargetCol(e.target.value)}
                    className="w-full bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl px-4 py-3 text-sm text-[#111827] focus:outline-none focus:border-[#5B5CEB] focus:ring-1 focus:ring-[#5B5CEB] transition-all appearance-none cursor-pointer font-medium disabled:opacity-60"
                    disabled={!profile}
                  >
                    {profile?.schema ? (
                      Object.keys(profile.schema).map((col, i) => (
                        <option key={i} value={col}>{col}</option>
                      ))
                    ) : (
                      <option value="">Awaiting profile...</option>
                    )}
                  </select>
                  <ChevronRight className="w-4 h-4 text-[#9CA3AF] pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 rotate-90" />
                </div>
              </div>

              <div className="pt-4 border-t border-[#E7EAF2]">
                <GradientButton 
                  onClick={() => trainMutation.mutate()}
                  disabled={trainMutation.isPending || !selectedDataset || !targetCol}
                  className="w-full h-12 shadow-sm active:scale-98"
                >
                  {trainMutation.isPending ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin text-white" /> 
                      <span>Training Models...</span>
                    </>
                  ) : (
                    <>
                      <Cpu className="w-4 h-4 mr-2 text-white" /> 
                      <span>Start AutoML Run</span>
                    </>
                  )}
                </GradientButton>
              </div>
            </div>
          </Card>

          <Card hover={false} className="bg-[#111827] border-[#1F2937] text-[#D1D5DB] min-h-[250px] flex flex-col p-6 shadow-md relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-[#5B5CEB] to-[#7C4DFF]" />
            <h3 className="text-[10px] font-bold text-[#9CA3AF] font-mono uppercase tracking-wider mb-4 flex items-center justify-between">
              <span className="flex items-center"><Activity className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Training Console</span>
              {trainMutation.isPending && <StatusBadge status="ACTIVE" type="running" />}
            </h3>
            <div className="flex-1 font-mono text-[11px] overflow-y-auto space-y-2.5 pr-1 scrollbar-thin scrollbar-thumb-white/10 select-text">
              {trainingLogs.length === 0 && (
                <div className="text-[#4B5563]">Awaiting pipeline instantiation...</div>
              )}
              <AnimatePresence>
                {trainingLogs.map((log, idx) => (
                  <motion.div 
                    initial={{ opacity: 0, x: -6 }} 
                    animate={{ opacity: 1, x: 0 }} 
                    key={idx}
                    className={`${log.includes('complete') || log.includes('deployed') ? 'text-[#16A34A]' : 'text-slate-300'}`}
                  >
                    <span className="text-[#6B7280] mr-1.5">{'>'}</span> {log}
                  </motion.div>
                ))}
                {trainMutation.isPending && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-[#5B5CEB] flex items-center">
                    <span className="text-[#6B7280] mr-1.5">{'>'}</span> Analyzing features space...
                    <span className="ml-2 w-1.5 h-3.5 bg-[#5B5CEB] animate-pulse"></span>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </Card>
        </div>

        {/* Right Column: Leaderboard & Metrics */}
        <div className="lg:col-span-2 space-y-6">
          
          {!automlStats && !trainMutation.isPending && (
            <div className="p-8">
              <EmptyState 
                title="No Models Trained Yet" 
                description="Run the AutoML pipeline from the config panel on the left to train multiple candidate models (Ridge, Random Forest, XGBoost). They will be ranked on accuracy."
                type="neural-network"
                primaryAction={{
                  label: "Ingest Spreadsheets",
                  onClick: () => {
                    window.location.href = "/data/ingestion";
                  }
                }}
                secondaryAction={{
                  label: "Go to Dashboard",
                  onClick: () => {
                    window.location.href = "/dashboard";
                  }
                }}
              />
            </div>
          )}

          {trainMutation.isPending && !automlStats && (
            <AgentStatusLoader />
          )}

          {automlStats && (
            <motion.div 
              initial={{ opacity: 0, y: 15 }} 
              animate={{ opacity: 1, y: 0 }} 
              className="space-y-6"
            >
              {/* Champion Model Card */}
              <Card hover={false} className="bg-gradient-to-br from-[#111827] to-[#1F2937] border border-[#374151] p-6 md:p-8 relative overflow-hidden text-white shadow-xl">
                <div className="absolute right-0 top-0 w-80 h-80 bg-gradient-to-tr from-[#5B5CEB] to-[#7C4DFF] rounded-full mix-blend-screen filter blur-[80px] opacity-25 translate-x-1/3 -translate-y-1/3 pointer-events-none"></div>
                
                <div className="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                  <div className="space-y-3">
                    <div className="flex items-center space-x-2">
                      <span className="flex items-center text-[#F59E0B] text-[10px] font-bold uppercase tracking-wider bg-[#F59E0B]/10 border border-[#F59E0B]/20 px-2 py-0.5 rounded">
                        <Trophy className="w-3 h-3 mr-1 fill-[#F59E0B] text-[#F59E0B]" /> Champion Model
                      </span>
                      <StatusBadge status="ACTIVE IN MEMORY" type="success" />
                    </div>
                    <h2 className="text-3xl font-extrabold tracking-tight text-white">{automlStats.best_model}</h2>
                    <p className="text-slate-400 text-xs font-semibold flex items-center">
                      <Target className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Target Column: {automlStats.target} • {automlStats.problem_type} Mode
                    </p>
                  </div>
                  
                  <div className="bg-white/10 backdrop-blur-md border border-white/10 rounded-2xl p-4 text-center min-w-[130px] shadow-sm">
                    <p className="text-white/60 text-[10px] font-bold uppercase tracking-wider mb-1">R² Score</p>
                    <p className="text-3xl font-mono font-extrabold text-white">{automlStats.leaderboard[0].r2_score.toFixed(4)}</p>
                  </div>
                </div>
              </Card>

              {/* Leaderboard Table */}
              <Card hover={false} className="p-0 overflow-hidden">
                <div className="p-5 border-b border-[#E7EAF2] flex justify-between items-center bg-[#F8F9FC]">
                  <h3 className="text-sm font-bold text-[#111827] flex items-center">
                    <Layers className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Evaluated Models Leaderboard
                  </h3>
                  <StatusBadge status={`${automlStats.leaderboard.length} Candidates`} type="neutral" />
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left border-collapse">
                    <thead className="bg-[#F8F9FC] text-[#6B7280] uppercase tracking-wider border-b border-[#E7EAF2]">
                      <tr>
                        <th className="px-6 py-4 font-bold">Rank</th>
                        <th className="px-6 py-4 font-bold">Algorithm</th>
                        <th className="px-6 py-4 font-bold text-right">R² Score</th>
                        <th className="px-6 py-4 font-bold text-right">RMSE</th>
                        <th className="px-6 py-4 font-bold text-right">CV Mean (±Std)</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#E7EAF2] font-medium text-[#4B5563]">
                      {automlStats.leaderboard.map((model: any, idx: number) => (
                        <tr 
                          key={idx} 
                          className={`hover:bg-[#F8F9FC]/60 transition-colors ${
                            idx === 0 ? 'bg-[#F0FDF4]/30 text-[#166534]' : 'bg-white text-[#4B5563]'
                          }`}
                        >
                          <td className="px-6 py-4 font-mono font-bold text-[#111827]">#{idx + 1}</td>
                          <td className="px-6 py-4 font-semibold text-[#111827]">
                            <div className="flex items-center">
                              {idx === 0 && <Trophy className="w-3.5 h-3.5 text-[#F59E0B] mr-1.5 fill-[#F59E0B]" />}
                              {model.model}
                            </div>
                          </td>
                          <td className="px-6 py-4 font-mono font-bold text-right text-[#5B5CEB]">{model.r2_score.toFixed(4)}</td>
                          <td className="px-6 py-4 font-mono text-right">{model.rmse.toFixed(4)}</td>
                          <td className="px-6 py-4 font-mono text-right text-[#6B7280]">
                            {model.cv_mean.toFixed(4)} <span className="text-[#9CA3AF] text-[10px]">±{model.cv_std.toFixed(4)}</span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>

              {/* Hyperparameters of Best Model */}
              <Card hover={false} className="p-6">
                <h3 className="text-sm font-bold text-[#111827] mb-4">Champion Hyperparameters</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {Object.entries(automlStats.leaderboard[0].hyperparameters).map(([key, val]: [string, any], idx) => (
                    <div key={idx} className="p-3 bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl flex flex-col justify-center">
                      <p className="text-[10px] text-[#6B7280] font-mono uppercase tracking-wider mb-1 truncate" title={key}>{key}</p>
                      <p className="text-xs font-bold text-[#111827] truncate" title={String(val)}>{String(val)}</p>
                    </div>
                  ))}
                </div>
                
                <div className="mt-6 pt-6 border-t border-[#E7EAF2] flex justify-end">
                  <Link href="/models/explainability">
                    <button className="px-6 py-2.5 bg-[#111827] hover:bg-[#1f2937] active:scale-98 text-white rounded-xl text-xs font-bold transition-all shadow-md hover:shadow-lg flex items-center cursor-pointer">
                      <span>Explain Model (SHAP)</span>
                      <ArrowRight className="w-3.5 h-3.5 ml-2" />
                    </button>
                  </Link>
                </div>
              </Card>

            </motion.div>
          )}

        </div>
      </div>

      <FloatingAIButton />
    </PageContainer>
  );
}
