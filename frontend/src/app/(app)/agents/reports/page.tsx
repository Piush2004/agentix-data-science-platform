"use client";

import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { Database, FileText, Download, Loader2, Sparkles, Presentation, FilePieChart, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { 
  PageContainer, 
  SectionHeader, 
  Card, 
  EmptyState, 
  GradientButton, 
  FloatingAIButton,
  LoadingSkeleton
} from '@/components/ui/design-system';

export default function ReportsPage() {
  const [selectedDataset, setSelectedDataset] = useState<string | null>(null);
  const [reportType, setReportType] = useState<'executive'|'technical'>('executive');
  const [reportFormat, setReportFormat] = useState<'pdf'|'docx'|'ppt'>('pdf');
  const [generatedReport, setGeneratedReport] = useState<any>(null);

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

  const generateMutation = useMutation({
    mutationFn: async () => {
      if (!selectedDataset) throw new Error("No dataset selected");
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/reports?dataset_name=${encodeURIComponent(selectedDataset)}`);
      return res.data.data;
    },
    onSuccess: (data) => {
      setGeneratedReport(data);
    }
  });

  if (history && history.length === 0) {
    return (
      <PageContainer>
        <SectionHeader 
          title="Report Generation" 
          description="Automatically compile insights, charts, and SHAP drivers into professional documents."
        />
        <div className="py-12">
          <EmptyState 
            title="No Datasets Uploaded" 
            description="You must ingest a dataset in your workspace memory before compiling executive analysis briefings."
            type="ai-agent"
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
        title="Report Generation" 
        description="Automatically compile insights, charts, and SHAP drivers into professional documents."
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        
        {/* Left Column: Config */}
        <div className="lg:col-span-1 space-y-6">
          <Card hover={false}>
            <div className="space-y-5">
              <div className="space-y-1.5">
                <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider flex items-center">
                  <Database className="w-3.5 h-3.5 mr-1.5 text-[#5B5CEB]" /> Source Data
                </label>
                <div className="relative">
                  <select 
                    value={selectedDataset || ""} 
                    onChange={(e) => setSelectedDataset(e.target.value)}
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
                <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider flex items-center">
                  <FileText className="w-3.5 h-3.5 mr-1.5 text-[#5B5CEB]" /> Audience / Tone
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <button 
                    onClick={() => setReportType('executive')}
                    className={`py-2.5 px-3 text-xs font-bold rounded-xl border transition-all cursor-pointer ${
                      reportType === 'executive' 
                        ? 'bg-[#F8F9FC] border-[#5B5CEB] text-[#5B5CEB] shadow-sm font-extrabold' 
                        : 'bg-white border-[#E7EAF2] text-[#6B7280] hover:bg-[#F8F9FC] hover:text-[#111827]'
                    }`}
                  >
                    Executive
                  </button>
                  <button 
                    onClick={() => setReportType('technical')}
                    className={`py-2.5 px-3 text-xs font-bold rounded-xl border transition-all cursor-pointer ${
                      reportType === 'technical' 
                        ? 'bg-[#F8F9FC] border-[#5B5CEB] text-[#5B5CEB] shadow-sm font-extrabold' 
                        : 'bg-white border-[#E7EAF2] text-[#6B7280] hover:bg-[#F8F9FC] hover:text-[#111827]'
                    }`}
                  >
                    Technical
                  </button>
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider flex items-center">
                  <Download className="w-3.5 h-3.5 mr-1.5 text-[#5B5CEB]" /> Export Format
                </label>
                <div className="grid grid-cols-3 gap-2">
                  <button 
                    onClick={() => setReportFormat('pdf')}
                    className={`py-2.5 text-xs font-extrabold rounded-xl border transition-all cursor-pointer ${
                      reportFormat === 'pdf' 
                        ? 'bg-[#FEF2F2] border-[#EF4444] text-[#EF4444] shadow-sm' 
                        : 'bg-white border-[#E7EAF2] text-[#6B7280] hover:bg-[#F8F9FC] hover:text-[#111827]'
                    }`}
                  >
                    PDF
                  </button>
                  <button 
                    onClick={() => setReportFormat('docx')}
                    className={`py-2.5 text-xs font-extrabold rounded-xl border transition-all cursor-pointer ${
                      reportFormat === 'docx' 
                        ? 'bg-[#EFF6FF] border-[#3B82F6] text-[#3B82F6] shadow-sm' 
                        : 'bg-white border-[#E7EAF2] text-[#6B7280] hover:bg-[#F8F9FC] hover:text-[#111827]'
                    }`}
                  >
                    DOCX
                  </button>
                  <button 
                    onClick={() => setReportFormat('ppt')}
                    className={`py-2.5 text-xs font-extrabold rounded-xl border transition-all cursor-pointer ${
                      reportFormat === 'ppt' 
                        ? 'bg-[#FFF7ED] border-[#F97316] text-[#F97316] shadow-sm' 
                        : 'bg-white border-[#E7EAF2] text-[#6B7280] hover:bg-[#F8F9FC] hover:text-[#111827]'
                    }`}
                  >
                    PPTX
                  </button>
                </div>
              </div>

              <div className="pt-4 border-t border-[#E7EAF2]">
                <GradientButton 
                  onClick={() => generateMutation.mutate()}
                  disabled={generateMutation.isPending || !selectedDataset}
                  className="w-full h-12 shadow-sm active:scale-98"
                >
                  {generateMutation.isPending ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin text-white" /> 
                      <span>Compiling Document...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4 mr-2 text-white" /> 
                      <span>Generate Report</span>
                    </>
                  )}
                </GradientButton>
              </div>
            </div>
          </Card>
        </div>

        {/* Right Column: Preview */}
        <div className="lg:col-span-2 space-y-6">
          
          {!generatedReport && !generateMutation.isPending && (
            <div className="p-6">
              <EmptyState 
                title="No Briefings Generated Yet" 
                description="Select variables and compile executive PDF briefs, PowerPoint presentations, or custom markdown summaries using local LLMs."
                type="report"
                primaryAction={{
                  label: "Compile AI Report",
                  onClick: () => {
                    generateMutation.mutate();
                  }
                }}
                secondaryAction={{
                  label: "Ingest Spreadsheets",
                  onClick: () => {
                    window.location.href = "/data/ingestion";
                  }
                }}
              />
            </div>
          )}

          {generateMutation.isPending && (
            <Card hover={false} className="flex flex-col justify-between min-h-[480px] p-8 space-y-6">
              <div className="space-y-2 border-b border-[#E7EAF2] pb-4">
                <div className="flex items-center space-x-2.5">
                  <LoadingSkeleton className="h-5 w-40" />
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#5B5CEB]/10 text-[#5B5CEB] animate-pulse">Processing</span>
                </div>
                <LoadingSkeleton className="h-3 w-60" />
              </div>
              
              <div className="flex-grow space-y-4 py-4">
                <LoadingSkeleton className="h-4 w-full" />
                <LoadingSkeleton className="h-4 w-[95%]" />
                <div className="grid grid-cols-2 gap-4 my-2">
                  <LoadingSkeleton className="h-28 w-full rounded-xl" />
                  <LoadingSkeleton className="h-28 w-full rounded-xl" />
                </div>
                <LoadingSkeleton className="h-4 w-[85%]" />
              </div>

              <div className="flex flex-col items-center space-y-2.5 border-t border-[#E7EAF2] pt-4">
                <span className="text-xs font-bold text-[#6B7280] uppercase tracking-wider">Compiling {reportFormat.toUpperCase()} Briefing</span>
                <div className="w-64 h-2 bg-[#F8F9FC] border border-[#E7EAF2] rounded-full overflow-hidden relative">
                  <div className="h-full bg-gradient-to-r from-[#5B5CEB] to-[#7C4DFF] animate-[loadingProgress_5s_infinite_ease-out] rounded-full"></div>
                </div>
                <style>{`
                  @keyframes loadingProgress {
                    0% { width: 0%; }
                    50% { width: 75%; }
                    100% { width: 100%; }
                  }
                `}</style>
              </div>
            </Card>
          )}

          {generatedReport && (
            <motion.div initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} className="space-y-6">
              
              <Card hover={false} className="border-[#16A34A]/20 bg-[#F0FDF4]/30 p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="flex items-center">
                  <div className="w-12 h-12 rounded-xl bg-white border border-[#E7EAF2] flex items-center justify-center mr-4 shadow-sm">
                    {reportFormat === 'pdf' ? <FileText className="w-6 h-6 text-[#EF4444]" /> : 
                     reportFormat === 'docx' ? <FileText className="w-6 h-6 text-[#3B82F6]" /> : 
                     <Presentation className="w-6 h-6 text-[#F97316]" />}
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-[#111827]">{selectedDataset} - {reportType.charAt(0).toUpperCase() + reportType.slice(1)} Report</h3>
                    <p className="text-xs text-[#16A34A] font-semibold mt-0.5">Asset successfully compiled and ready for download.</p>
                  </div>
                </div>
                
                <button 
                  onClick={() => alert('Download simulation: ' + generatedReport.download_url)}
                  className="px-6 py-2.5 bg-[#111827] hover:bg-[#1f2937] active:scale-98 text-white rounded-xl text-xs font-bold transition-all shadow-md hover:shadow-lg flex items-center cursor-pointer shrink-0"
                >
                  <Download className="w-4 h-4 mr-2" /> Download {reportFormat.toUpperCase()}
                </button>
              </Card>

              {/* Document Mockup */}
              <div className="bg-white border border-[#E7EAF2] rounded-[24px] p-8 md:p-12 min-h-[500px] font-serif max-w-3xl mx-auto shadow-2xl relative select-text">
                <div className="absolute top-0 right-0 p-6 opacity-5 pointer-events-none">
                  <FilePieChart className="w-24 h-24 text-[#111827]" />
                </div>
                <h1 className="text-3xl font-bold text-[#111827] mb-2 border-b-2 border-[#111827] pb-4 font-sans tracking-tight">Agentix: Insights & Model Analysis</h1>
                <p className="text-xs text-[#6B7280] mb-8 font-sans font-bold uppercase tracking-wider">Prepared for: Workspace Executive Board | Date: {new Date().toLocaleDateString()}</p>
                
                <div className="prose prose-sm max-w-none text-[#374151] space-y-6">
                  <p className="text-base font-semibold leading-relaxed text-[#111827]">
                    This artifact presents automated statistics and models evaluated on the active workspace dataset <strong>{selectedDataset}</strong>.
                  </p>
                  
                  <div className="space-y-2">
                    <h3 className="text-base font-extrabold text-[#111827] font-sans border-b border-[#E7EAF2] pb-1.5">1. Machine Learning Performance Summary</h3>
                    <p className="text-xs leading-relaxed">
                      Using hyperparameter sweep heuristics, we evaluated classification and regression algorithms on the workspace parameters. The champion candidate was benchmarked through K-Fold validation to guarantee out-of-sample stability.
                    </p>
                  </div>
                  
                  <div className="space-y-2">
                    <h3 className="text-base font-extrabold text-[#111827] font-sans border-b border-[#E7EAF2] pb-1.5">2. Explainability and SHAP Game Theory</h3>
                    <p className="text-xs leading-relaxed">
                      We applied localized SHAP explainers to calculate feature impacts. The dominant predictors explain the majority of predictive variance, identifying actionable vectors for model intervention.
                    </p>
                  </div>

                  <div className="mt-12 p-4 bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl font-sans">
                    <p className="text-[10px] text-[#6B7280] font-bold uppercase tracking-wider text-center">
                      [Document Preview Segment - Full content available in the download package]
                    </p>
                  </div>
                </div>
              </div>

            </motion.div>
          )}

        </div>
      </div>

      <FloatingAIButton />
    </PageContainer>
  );
}
