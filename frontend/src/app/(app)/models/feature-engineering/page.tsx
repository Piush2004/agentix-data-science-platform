"use client";

import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { Database, Binary, Scale, Scissors, Sparkles, CheckCircle2, ArrowRight, Loader2, PlayCircle, Eye } from 'lucide-react';
import { motion } from 'framer-motion';

export default function FeatureEngineeringPage() {
  const queryClient = useQueryClient();
  const [selectedDataset, setSelectedDataset] = useState<string | null>(null);
  const [feStats, setFeStats] = useState<any>(null);

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

  const feMutation = useMutation({
    mutationFn: async () => {
      if (!selectedDataset) throw new Error("No dataset selected");
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/feature-engineering`, { dataset_name: selectedDataset });
      return res.data.data;
    },
    onSuccess: (data) => {
      setFeStats(data);
      queryClient.invalidateQueries({ queryKey: ['dashboardMetrics'] });
    }
  });

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500 font-sans pb-10">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[#E5E7EB] pb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-[#111827]">
            Feature Engineering
          </h1>
          <p className="text-[#6B7280] mt-1 text-sm">Automated encoding, scaling, and feature selection pipelines.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Context & Config */}
        <div className="lg:col-span-1 space-y-6">
          <div className="p-6 rounded-xl bg-white border border-[#E5E7EB] shadow-sm">
            <label className="text-sm font-semibold text-[#111827] mb-3 flex items-center">
              <Database className="w-4 h-4 mr-2 text-[#9CA3AF]" />
              Target Dataset
            </label>
            <select 
              value={selectedDataset || ""} 
              onChange={(e) => {
                setSelectedDataset(e.target.value);
                setFeStats(null);
              }}
              className="w-full bg-[#F5F7FA] border border-[#E5E7EB] rounded-lg py-2.5 px-4 text-sm text-[#111827] focus:outline-none focus:border-[#5B5CEB] transition-colors"
            >
              <option value="" disabled>Select a dataset</option>
              {history?.map((d: any, i: number) => (
                <option key={i} value={d.name}>{d.name}</option>
              ))}
            </select>
          </div>

          <div className="p-6 rounded-xl bg-white border border-[#E5E7EB] shadow-sm">
            <h3 className="text-sm font-semibold text-[#111827] mb-5 border-b border-[#E5E7EB] pb-3 flex items-center">
              <Sparkles className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Automated Pipeline
            </h3>
            
            <div className="space-y-5">
              <div className="flex items-start">
                <div className="w-8 h-8 rounded bg-[#EEF2F6] flex items-center justify-center mr-3 mt-0.5 shrink-0">
                  <Binary className="w-4 h-4 text-[#5B5CEB]" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-[#111827]">Categorical Encoding</h4>
                  <p className="text-xs text-[#6B7280] mt-1 leading-relaxed">Auto-detects categorical variables and applies One-Hot Encoding to prevent model bias.</p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="w-8 h-8 rounded bg-[#EEF2F6] flex items-center justify-center mr-3 mt-0.5 shrink-0">
                  <Scale className="w-4 h-4 text-[#5B5CEB]" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-[#111827]">Feature Scaling</h4>
                  <p className="text-xs text-[#6B7280] mt-1 leading-relaxed">Applies Standard Scaler to numerical variables ensuring zero mean and unit variance.</p>
                </div>
              </div>

              <div className="flex items-start">
                <div className="w-8 h-8 rounded bg-[#EEF2F6] flex items-center justify-center mr-3 mt-0.5 shrink-0">
                  <Scissors className="w-4 h-4 text-[#5B5CEB]" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-[#111827]">Feature Selection</h4>
                  <p className="text-xs text-[#6B7280] mt-1 leading-relaxed">Drops highly collinear features automatically to reduce dimensionality.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Execution */}
        <div className="lg:col-span-2 flex flex-col space-y-6">
          
          {!feStats && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
              className="p-8 rounded-xl bg-white border border-[#E5E7EB] shadow-sm flex flex-col items-center justify-center min-h-[400px] text-center"
            >
              <div className="w-16 h-16 bg-[#F5F7FA] rounded-full flex items-center justify-center mb-6 border border-[#E5E7EB]">
                <PlayCircle className="w-8 h-8 text-[#5B5CEB]" />
              </div>
              <h2 className="text-xl font-bold text-[#111827] mb-2">Execute FE Pipeline</h2>
              <p className="text-[#6B7280] text-sm max-w-md mb-8">
                The agent will dynamically assess your schema and mathematically transform the dataset for optimal machine learning performance.
              </p>
              
              <button 
                onClick={() => feMutation.mutate()}
                disabled={feMutation.isPending || !selectedDataset}
                className="inline-flex h-12 items-center justify-center rounded-xl bg-[#111827] px-8 text-sm font-semibold text-white shadow-sm transition-all hover:bg-[#1f2937] disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {feMutation.isPending ? (
                  <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Compiling Features...</>
                ) : (
                  <><Sparkles className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Run Pipeline</>
                )}
              </button>
            </motion.div>
          )}

          {feStats && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }}
              className="rounded-xl bg-white border border-[#5B5CEB] shadow-sm overflow-hidden"
            >
              <div className="p-6 border-b border-[#E5E7EB] bg-[#EEF2F6] flex items-center justify-between">
                <div className="flex items-center">
                  <CheckCircle2 className="w-6 h-6 text-[#5B5CEB] mr-3" />
                  <div>
                    <h3 className="text-base font-bold text-[#111827]">Pipeline Completed</h3>
                    <p className="text-sm text-[#4B5563] mt-0.5">Dataset is fully vectorized and scaled.</p>
                  </div>
                </div>
              </div>

              <div className="p-8">
                
                <div className="mb-8">
                  <h4 className="text-sm font-semibold text-[#111827] mb-4 flex items-center"><Eye className="w-4 h-4 mr-2 text-[#6B7280]" /> Pipeline Transformations</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {feStats.actions?.map((action: string, idx: number) => (
                      <div key={idx} className="p-4 rounded-xl bg-[#F5F7FA] border border-[#E5E7EB] flex items-center">
                        <CheckCircle2 className="w-5 h-5 text-[#16A34A] mr-3 shrink-0" />
                        <span className="text-sm font-medium text-[#111827]">{action}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mb-8">
                  <h4 className="text-sm font-semibold text-[#111827] mb-4">Total Features Output ({feStats.features_added?.length || 0})</h4>
                  <div className="flex flex-wrap gap-2 max-h-64 overflow-y-auto pr-2 custom-scrollbar">
                    {feStats.features_added?.map((feat: string, idx: number) => (
                      <span key={idx} className="px-3 py-1.5 bg-white border border-[#E5E7EB] text-xs font-mono text-[#4B5563] rounded-lg">
                        {feat}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex justify-end pt-6 border-t border-[#E5E7EB]">
                  <a href="/analysis/eda" className="px-6 py-2.5 bg-[#111827] hover:bg-[#1f2937] text-white rounded-lg text-sm font-medium shadow-sm transition-colors flex items-center">
                    Proceed to EDA <ArrowRight className="w-4 h-4 ml-2" />
                  </a>
                </div>
              </div>
            </motion.div>
          )}

        </div>
      </div>
    </div>
  );
}
