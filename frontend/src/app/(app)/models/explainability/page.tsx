"use client";

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { Database, Lightbulb, TrendingUp, AlertTriangle, ArrowRight, Binary, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { 
  PageContainer, 
  SectionHeader, 
  Card, 
  EmptyState, 
  StatusBadge, 
  AgentStatusLoader,
  FloatingAIButton 
} from '@/components/ui/design-system';
import Link from 'next/link';

export default function ExplainabilityPage() {
  const [selectedDataset, setSelectedDataset] = useState<string | null>(null);

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

  const { data: xai, isLoading } = useQuery({
    queryKey: ['xaiData', selectedDataset],
    queryFn: async () => {
      if (!selectedDataset) return null;
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/xai?dataset_name=${encodeURIComponent(selectedDataset)}`);
      return res.data.data;
    },
    enabled: !!selectedDataset
  });

  if (history && history.length === 0) {
    return (
      <PageContainer>
        <SectionHeader 
          title="Model Explainability (XAI)" 
          description="SHAP values, feature importance, and mathematical business drivers."
        />
        <div className="py-12">
          <EmptyState 
            title="No Datasets Uploaded" 
            description="You must ingest a dataset in your workspace memory before interpreting machine learning variables."
            type="decision-tree"
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
        title="Model Explainability (XAI)" 
        description="SHAP values, feature importance, and mathematical business drivers."
      />

      <Card hover={false} className="p-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center w-full md:w-auto">
          <Database className="w-4 h-4 mr-3 text-[#5B5CEB]" />
          <div className="relative flex-1 sm:flex-initial">
            <select 
              value={selectedDataset || ""} 
              onChange={(e) => setSelectedDataset(e.target.value)}
              className="bg-transparent text-sm font-bold text-[#111827] focus:outline-none w-64 pr-8 cursor-pointer appearance-none"
            >
              <option value="" disabled>Select Dataset</option>
              {history?.map((d: any, i: number) => (
                <option key={i} value={d.name}>{d.name}</option>
              ))}
            </select>
            <ChevronRight className="w-3.5 h-3.5 text-[#9CA3AF] pointer-events-none absolute right-0 top-1/2 -translate-y-1/2 rotate-90" />
          </div>
        </div>
      </Card>

      {isLoading ? (
        <AgentStatusLoader />
      ) : !xai || Object.keys(xai.importances).length === 0 ? (
        <div className="p-8">
          <EmptyState 
            title="No Trained Models Detected" 
            description="SHAP explainability values require a champion trained model. Tune and register a candidate in AutoML first."
            type="decision-tree"
            primaryAction={{
              label: "Go to AutoML Training",
              onClick: () => {
                window.location.href = '/models/automl';
              }
            }}
            secondaryAction={{
              label: "Back to Dashboard",
              onClick: () => {
                window.location.href = '/dashboard';
              }
            }}
          />
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
          
          {/* Left: Summary & Alerts */}
          <div className="lg:col-span-1 space-y-6">
            
            {/* Business Explanation */}
            <Card hover={false} className="bg-gradient-to-br from-[#111827] to-[#1F2937] border border-[#374151] text-white shadow-xl relative overflow-hidden">
              <div className="absolute right-0 top-0 w-32 h-32 bg-[#F59E0B] rounded-full mix-blend-screen filter blur-[40px] opacity-10 translate-x-8 -translate-y-8 pointer-events-none"></div>
              <h3 className="text-xs font-bold uppercase tracking-wider mb-4 flex items-center text-[#F59E0B]">
                <Lightbulb className="w-4 h-4 mr-2" /> Business Impact Analysis
              </h3>
              <p className="text-xs text-slate-300 font-medium leading-relaxed">
                The model's predictions are primarily driven by the variance in <strong className="text-white font-bold">{xai.top_drivers[0]}</strong>. 
                Adjusting this feature has the highest probabilistic influence on predictive outcomes.
              </p>
            </Card>

            {/* Alerts */}
            {xai.leakage_alert && (
              <Card hover={false} className="bg-[#FEF2F2]/30 border-[#EF4444]/20 p-5">
                <h3 className="text-xs font-bold text-[#EF4444] mb-2 flex items-center">
                  <AlertTriangle className="w-4 h-4 mr-2" /> Target Leakage Risk
                </h3>
                <p className="text-xs text-[#EF4444] font-semibold leading-relaxed">
                  Feature <strong className="font-bold underline">{xai.dominant_feature}</strong> exhibits excessive SHAP dominance (&gt;80%). Check if this feature contains implicit target information.
                </p>
              </Card>
            )}

            {/* Global Feature Importance */}
            <Card hover={false}>
              <h3 className="text-xs font-bold uppercase tracking-wider text-[#111827] mb-5 border-b border-[#E7EAF2] pb-3 flex items-center justify-between">
                <span className="flex items-center"><TrendingUp className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Global Importances</span>
                <StatusBadge status="SHAP Mean" type="neutral" />
              </h3>
              <div className="space-y-4">
                {Object.entries(xai.importances)
                  .sort((a: any, b: any) => b[1] - a[1])
                  .slice(0, 8)
                  .map(([feat, imp]: [string, any], idx) => {
                    const maxImp = Math.max(...Object.values(xai.importances) as number[]);
                    const pct = (imp / maxImp) * 100;
                    return (
                      <div key={idx} className="space-y-1.5">
                        <div className="flex justify-between text-xs font-medium">
                          <span className="font-semibold text-[#4B5563] truncate pr-2" title={feat}>{feat}</span>
                          <span className="font-mono font-bold text-[#111827]">{imp.toFixed(4)}</span>
                        </div>
                        <div className="w-full bg-[#F8F9FC] border border-[#E7EAF2] rounded-full h-2 overflow-hidden">
                          <div className="bg-[#5B5CEB] h-2 rounded-full" style={{ width: `${pct}%` }}></div>
                        </div>
                      </div>
                    );
                })}
              </div>
            </Card>

          </div>

          {/* Right: SHAP Waterfall */}
          <div className="lg:col-span-2 space-y-6">
            
            <Card hover={false} className="p-6 md:p-8">
              <div className="flex justify-between items-start mb-6 pb-3 border-b border-[#E7EAF2]">
                <div>
                  <h3 className="text-sm font-bold text-[#111827] flex items-center">
                    <Binary className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Local SHAP Waterfall
                  </h3>
                  <p className="text-xs text-[#6B7280] mt-1 font-medium">
                    Feature contributions driving prediction from base value to final prediction vector.
                  </p>
                </div>
                <StatusBadge status="Game-Theoretic" type="success" />
              </div>

              {/* Waterfall Visualization */}
              <div className="relative font-mono text-[11px] mt-10">
                {/* Base Value Line */}
                <div className="flex justify-between items-center mb-6 text-[#6B7280]">
                  <span className="w-32 text-right pr-4 font-bold text-xs uppercase tracking-wider font-sans">Base Value</span>
                  <div className="flex-1 relative h-6 flex items-center">
                    <div className="absolute left-[50%] top-0 bottom-0 border-l-2 border-dashed border-[#D1D5DB]" />
                    <span className="absolute left-[calc(50%+12px)] text-[10px] font-bold text-[#4B5563] bg-[#F8F9FC] border border-[#E7EAF2] px-2.5 py-0.5 rounded-lg">
                      E[f(x)] = {xai.base_value.toFixed(3)}
                    </span>
                  </div>
                </div>

                {xai.waterfall.map((item: any, idx: number) => {
                  const isPositive = item.impact > 0;
                  const color = isPositive ? 'bg-[#5B5CEB]' : 'bg-[#16A34A]';
                  const textColor = isPositive ? 'text-[#5B5CEB]' : 'text-[#16A34A]';
                  
                  const maxImpact = Math.max(...xai.waterfall.map((w: any) => Math.abs(w.impact)));
                  const widthPct = Math.min(45, Math.max(5, (Math.abs(item.impact) / maxImpact) * 45));
                  
                  return (
                    <div key={idx} className="flex items-center mb-4 relative z-10 group">
                      <span className="w-32 text-right pr-4 text-[#6B7280] truncate font-sans font-bold uppercase tracking-wider text-[9px]" title={item.feature}>
                        {item.feature}
                      </span>
                      
                      <div className="flex-1 relative h-8 flex items-center">
                        <div className="absolute left-[50%] top-0 bottom-0 border-l border-dashed border-[#E7EAF2] z-0" />
                        
                        {isPositive ? (
                          <div className="absolute left-[50%] flex items-center z-10 pl-0.5" style={{ width: `${widthPct}%` }}>
                            <motion.div 
                              initial={{ width: 0 }} 
                              animate={{ width: '100%' }}
                              className={`h-5 ${color} rounded-md opacity-90`}
                            />
                            <span className={`ml-2.5 font-bold ${textColor} shrink-0`}>+{item.impact.toFixed(3)}</span>
                          </div>
                        ) : (
                          <div className="absolute right-[50%] flex items-center justify-end z-10 pr-0.5" style={{ width: `${widthPct}%` }}>
                            <span className={`mr-2.5 font-bold ${textColor} shrink-0`}>{item.impact.toFixed(3)}</span>
                            <motion.div 
                              initial={{ width: 0 }} 
                              animate={{ width: '100%' }}
                              className={`h-5 ${color} rounded-md opacity-90`}
                            />
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}

                {/* Final Prediction */}
                <div className="flex justify-between items-center mt-6 pt-6 border-t border-[#E7EAF2]">
                  <span className="w-32 text-right pr-4 font-bold text-[#111827] text-xs uppercase tracking-wider font-sans">Final Prediction</span>
                  <div className="flex-1 relative h-8 flex items-center">
                    <div className="absolute left-[50%] top-0 bottom-0 border-l-2 border-[#5B5CEB]" />
                    <span className="absolute left-[calc(50%+12px)] text-xs font-extrabold text-[#111827] bg-white border-2 border-[#5B5CEB] px-3 py-1 rounded-xl shadow-sm">
                      f(x) = {xai.final_prediction.toFixed(3)}
                    </span>
                  </div>
                </div>

              </div>
            </Card>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Link href="/agents/analyst" className="w-full">
                <Card hover={true} className="p-5 flex justify-between items-center group cursor-pointer h-24">
                  <div className="space-y-1">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-[#111827]">Talk to AI Analyst</h4>
                    <p className="text-xs text-[#6B7280] font-medium">Query SHAP impact vectors in plain English</p>
                  </div>
                  <ArrowRight className="w-4 h-4 text-[#9CA3AF] group-hover:text-[#5B5CEB] transition-colors" />
                </Card>
              </Link>
              <Link href="/agents/reports" className="w-full">
                <Card hover={true} className="p-5 flex justify-between items-center group cursor-pointer h-24">
                  <div className="space-y-1">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-[#111827]">Generate Insights Report</h4>
                    <p className="text-xs text-[#6B7280] font-medium">Export SHAP explanation plots to PDF</p>
                  </div>
                  <ArrowRight className="w-4 h-4 text-[#9CA3AF] group-hover:text-[#16A34A] transition-colors" />
                </Card>
              </Link>
            </div>

          </div>

        </div>
      )}

      <FloatingAIButton />
    </PageContainer>
  );
}
