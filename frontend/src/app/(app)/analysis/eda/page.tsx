"use client";

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { Database, Filter, BarChart2, Activity, LayoutGrid, ChevronRight } from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { 
  PageContainer, 
  SectionHeader, 
  Card, 
  AgentStatusLoader,
  FloatingAIButton,
  StatusBadge,
  EmptyState
} from '@/components/ui/design-system';

export default function EDAPage() {
  const [selectedDataset, setSelectedDataset] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'distributions' | 'correlations' | 'statistics'>('distributions');

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

  const { data: eda, isLoading } = useQuery({
    queryKey: ['edaData', selectedDataset],
    queryFn: async () => {
      if (!selectedDataset) return null;
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/eda?dataset_name=${encodeURIComponent(selectedDataset)}`);
      return res.data.data;
    },
    enabled: !!selectedDataset
  });

  const actionTabs = (
    <div className="flex items-center space-x-1.5 bg-[#F8F9FC] border border-[#E7EAF2] p-1 rounded-xl">
      <button 
        onClick={() => setActiveTab('distributions')}
        className={`px-4 py-2 text-xs font-bold rounded-lg transition-all cursor-pointer ${
          activeTab === 'distributions' 
            ? 'bg-white text-[#5B5CEB] shadow-sm border border-[#E7EAF2]' 
            : 'text-[#6B7280] hover:text-[#111827]'
        }`}
      >
        Distributions
      </button>
      <button 
        onClick={() => setActiveTab('correlations')}
        className={`px-4 py-2 text-xs font-bold rounded-lg transition-all cursor-pointer ${
          activeTab === 'correlations' 
            ? 'bg-white text-[#5B5CEB] shadow-sm border border-[#E7EAF2]' 
            : 'text-[#6B7280] hover:text-[#111827]'
        }`}
      >
        Correlations
      </button>
      <button 
        onClick={() => setActiveTab('statistics')}
        className={`px-4 py-2 text-xs font-bold rounded-lg transition-all cursor-pointer ${
          activeTab === 'statistics' 
            ? 'bg-white text-[#5B5CEB] shadow-sm border border-[#E7EAF2]' 
            : 'text-[#6B7280] hover:text-[#111827]'
        }`}
      >
        Statistics
      </button>
    </div>
  );

  return (
    <PageContainer>
      <SectionHeader 
        title="Exploratory Data Analysis" 
        description="Interactive visualizations for distribution, correlation, and statistical anomalies."
        actions={actionTabs}
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
        <button className="hidden md:flex items-center text-xs font-bold text-[#6B7280] hover:text-[#111827] px-3 py-1.5 border border-[#E7EAF2] bg-[#F8F9FC] rounded-lg transition-all">
          <Filter className="w-3.5 h-3.5 mr-2" /> Filters
        </button>
      </Card>

      {isLoading ? (
        <AgentStatusLoader />
      ) : !eda ? (
        <div className="py-8">
          <EmptyState 
            title="Begin Exploratory Analysis" 
            description="Select an active dataset from the switcher dropdown above to analyze histograms, correlation heatmaps, and statistical skews."
            type="correlation-heatmap"
            primaryAction={{
              label: "Ingest Spreadsheet",
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
      ) : (
        <div className="space-y-6">
          
          {/* DISTRIBUTIONS */}
          {activeTab === 'distributions' && eda.histograms && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {Object.entries(eda.histograms).map(([col, data]: [string, any], idx) => {
                const chartData = data.bins.slice(0, -1).map((bin: number, i: number) => ({
                  name: bin.toFixed(2),
                  count: data.counts[i]
                }));
                return (
                  <Card key={idx} hover={true} className="flex flex-col">
                    <div className="flex justify-between items-center mb-6 pb-3 border-b border-[#E7EAF2]">
                      <h3 className="text-sm font-bold text-[#111827] flex items-center">
                        <BarChart2 className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Histogram: {col}
                      </h3>
                      <StatusBadge status="Distribution" type="neutral" />
                    </div>
                    <div className="h-64 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={chartData} margin={{ left: -10, right: 10 }}>
                          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E7EAF2" />
                          <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fontSize: 9, fill: '#6B7280', fontWeight: 'bold'}} />
                          <YAxis axisLine={false} tickLine={false} tick={{fontSize: 9, fill: '#6B7280', fontWeight: 'bold'}} />
                          <Tooltip 
                            cursor={{fill: '#F8F9FC'}} 
                            contentStyle={{
                              borderRadius: '12px', 
                              border: '1px solid #E7EAF2', 
                              fontSize: '11px',
                              fontWeight: 'bold',
                              boxShadow: '0 8px 30px rgba(0,0,0,0.04)'
                            }} 
                          />
                          <Bar dataKey="count" fill="#5B5CEB" radius={[6, 6, 0, 0]} maxBarSize={40} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </Card>
                );
              })}
            </div>
          )}

          {/* CORRELATIONS / HEATMAP */}
          {activeTab === 'correlations' && eda.correlations && (
            <Card hover={false} className="p-6 md:p-8 overflow-x-auto">
              <div className="flex justify-between items-center mb-6 pb-3 border-b border-[#E7EAF2]">
                <h3 className="text-sm font-bold text-[#111827] flex items-center">
                  <LayoutGrid className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Correlation Matrix Heatmap
                </h3>
                <span className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider bg-[#F8F9FC] px-2.5 py-1 rounded-lg border border-[#E7EAF2]">Linear Associations</span>
              </div>
              <div className="inline-block min-w-full">
                <table className="w-full text-xs font-mono text-center border-collapse">
                  <thead>
                    <tr>
                      <th className="p-3 border-b border-[#E7EAF2]"></th>
                      {Object.keys(eda.correlations).map(k => (
                        <th key={k} className="p-3 border-b border-[#E7EAF2] text-[#6B7280] font-bold tracking-tight truncate max-w-[100px]">{k}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {Object.keys(eda.correlations).map(row => (
                      <tr key={row} className="hover:bg-[#F8F9FC]/40 transition-colors">
                        <td className="p-3 border-r border-[#E7EAF2] text-[#6B7280] font-bold text-right pr-4">{row}</td>
                        {Object.keys(eda.correlations).map(col => {
                          const val = eda.correlations[row][col];
                          const opacity = Math.abs(val);
                          // success green for positive correlation, danger red for negative
                          const bg = val > 0 
                            ? `rgba(22, 163, 74, ${opacity * 0.9})` 
                            : `rgba(239, 68, 68, ${opacity * 0.9})`;
                          const textColor = opacity > 0.4 ? 'white' : '#111827';
                          return (
                            <td 
                              key={col} 
                              className="p-3 transition-all hover:scale-105 hover:ring-2 hover:ring-[#111827] hover:z-10 relative font-semibold"
                              style={{ backgroundColor: bg, color: textColor }}
                            >
                              {val.toFixed(2)}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          )}

          {/* STATISTICS / BOXPLOTS */}
          {activeTab === 'statistics' && eda.statistics && eda.boxplots && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.entries(eda.statistics).map(([col, stats]: [string, any], idx) => (
                <Card key={idx} hover={true} className="flex flex-col">
                  <h3 className="text-sm font-bold text-[#111827] mb-4 border-b border-[#E7EAF2] pb-3 flex items-center justify-between">
                    <span className="flex items-center">
                      <Activity className="w-4 h-4 mr-2 text-[#5B5CEB]" /> {col}
                    </span>
                    <span className="text-[10px] font-bold text-[#6B7280] bg-[#F8F9FC] border border-[#E7EAF2] px-2 py-0.5 rounded-md">Descriptive</span>
                  </h3>
                  <div className="space-y-3 font-sans">
                    <div className="flex justify-between items-center text-xs">
                      <span className="font-bold text-[#6B7280] uppercase tracking-wider">Mean</span>
                      <span className="font-mono font-bold text-[#111827]">{stats.mean.toFixed(4)}</span>
                    </div>
                    <div className="flex justify-between items-center text-xs">
                      <span className="font-bold text-[#6B7280] uppercase tracking-wider">Std Dev</span>
                      <span className="font-mono font-bold text-[#111827]">{stats.std.toFixed(4)}</span>
                    </div>
                    <div className="flex justify-between items-center text-xs">
                      <span className="font-bold text-[#6B7280] uppercase tracking-wider">Skewness</span>
                      <span className={`font-mono font-bold ${Math.abs(stats.skew) > 1 ? 'text-[#F59E0B]' : 'text-[#16A34A]'}`}>{stats.skew.toFixed(4)}</span>
                    </div>
                    
                    {/* Boxplot Info */}
                    {eda.boxplots[col] && (
                      <div className="pt-3 mt-3 border-t border-[#E7EAF2] space-y-3">
                        <div className="flex justify-between items-center text-xs">
                          <span className="font-bold text-[#6B7280] uppercase tracking-wider">Min</span>
                          <span className="font-mono text-[#4B5563]">{eda.boxplots[col].min.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between items-center text-xs">
                          <span className="font-bold text-[#6B7280] uppercase tracking-wider">Median</span>
                          <span className="font-mono font-bold text-[#5B5CEB] text-sm bg-[#5B5CEB]/5 px-2 py-0.5 border border-[#5B5CEB]/10 rounded-md">
                            {eda.boxplots[col].median.toFixed(2)}
                          </span>
                        </div>
                        <div className="flex justify-between items-center text-xs">
                          <span className="font-bold text-[#6B7280] uppercase tracking-wider">Max</span>
                          <span className="font-mono text-[#4B5563]">{eda.boxplots[col].max.toFixed(2)}</span>
                        </div>
                      </div>
                    )}
                  </div>
                </Card>
              ))}
            </div>
          )}

        </div>
      )}

      <FloatingAIButton />
    </PageContainer>
  );
}
