"use client";

import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { Database, PlayCircle, Loader2, Clock, Server, ChevronRight } from 'lucide-react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
  Position,
  Handle
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { 
  SectionHeader, 
  StatusBadge, 
  GradientButton, 
  FloatingAIButton 
} from '@/components/ui/design-system';

// Custom Node Component
const AgentNode = ({ data }: { data: any }) => {
  const isRunning = data.status === 'Running';
  const isComplete = data.status === 'Completed';
  const isError = data.status === 'Failed';
  
  let borderColor = 'border-[#E7EAF2]';
  let bgColor = 'bg-white';
  let iconColor = 'text-[#9CA3AF]';
  let badgeType: 'success' | 'warning' | 'error' | 'neutral' | 'running' = 'neutral';
  
  if (isRunning) {
    borderColor = 'border-[#5B5CEB]';
    bgColor = 'bg-[#F8F9FC]';
    iconColor = 'text-[#5B5CEB]';
    badgeType = 'running';
  } else if (isComplete) {
    borderColor = 'border-[#16A34A]/30';
    bgColor = 'bg-[#F0FDF4]/30';
    iconColor = 'text-[#16A34A]';
    badgeType = 'success';
  } else if (isError) {
    borderColor = 'border-[#EF4444]/30';
    bgColor = 'bg-[#FEF2F2]/30';
    iconColor = 'text-[#EF4444]';
    badgeType = 'error';
  }

  return (
    <div className={`px-4 py-3 rounded-2xl border ${borderColor} ${bgColor} shadow-[0_4px_20px_rgba(0,0,0,0.015)] w-48 transition-all duration-300 relative select-none font-sans`}>
      <Handle type="target" position={Position.Top} className="w-1.5 h-1.5 !bg-[#D1D5DB] !border-0" />
      
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center">
          <Server className={`w-3.5 h-3.5 mr-1.5 ${iconColor}`} />
          <StatusBadge status={data.status} type={badgeType} />
        </div>
        {isRunning && <Loader2 className="w-3 h-3 text-[#5B5CEB] animate-spin" />}
      </div>
      
      <h4 className="text-xs font-bold text-[#111827] mb-1.5">{data.label}</h4>
      
      <div className="flex items-center text-[10px] text-[#6B7280] font-mono font-bold">
        <Clock className="w-3 h-3 mr-1 text-[#9CA3AF]" /> 
        {data.duration ? `${data.duration.toFixed(1)}s` : '0.0s'}
      </div>

      <Handle type="source" position={Position.Bottom} className="w-1.5 h-1.5 !bg-[#D1D5DB] !border-0" />
    </div>
  );
};

const nodeTypes = {
  agentNode: AgentNode,
};

export default function WorkflowPage() {
  const [selectedDataset, setSelectedDataset] = useState<string | null>(null);
  const [nodes, setNodes, onNodesChange] = useNodesState<any>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<any>([]);

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

  const { data: statusData } = useQuery({
    queryKey: ['workflowStatus'],
    queryFn: async () => {
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/workflow-status`);
      return res.data;
    },
    refetchInterval: 1000 // Poll aggressively for live workflow animation
  });

  const startMutation = useMutation({
    mutationFn: async () => {
      if (!selectedDataset) throw new Error("No dataset selected");
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/start-workflow`, { dataset_name: selectedDataset });
    }
  });

  useEffect(() => {
    if (statusData && statusData.nodes && statusData.nodes.length > 0) {
      // Calculate positions for a visual DAG
      const initialNodes = statusData.nodes.map((node: any, idx: number) => {
        const row = Math.floor(idx / 2);
        const col = idx % 2;
        
        return {
          id: node.id,
          type: 'agentNode',
          position: { x: col * 250 + 100, y: row * 150 + 50 },
          data: { label: node.label, status: node.status, duration: node.duration, error: node.error }
        };
      });

      const initialEdges = [];
      for (let i = 0; i < statusData.nodes.length - 1; i++) {
        const sourceId = statusData.nodes[i].id;
        const targetId = statusData.nodes[i+1].id;
        const isSourceComplete = statusData.nodes[i].status === 'Completed';
        
        initialEdges.push({
          id: `e-${sourceId}-${targetId}`,
          source: sourceId,
          target: targetId,
          animated: !isSourceComplete,
          style: { stroke: isSourceComplete ? '#16A34A' : '#9CA3AF', strokeWidth: 1.5 },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            color: isSourceComplete ? '#16A34A' : '#9CA3AF',
          },
        });
      }

      setNodes(initialNodes);
      setEdges(initialEdges);
    } else if (nodes.length === 0) {
      // Setup empty default graph
      const defaultAgents = [
        "Upload", "Profiling", "Cleaning", "Engineering", "EDA", "Prediction", "Explainability", "Report"
      ];
      
      const defaultNodes = defaultAgents.map((label, idx) => {
        const row = Math.floor(idx / 2);
        const col = idx % 2;
        return {
          id: `default-${idx}`,
          type: 'agentNode',
          position: { x: col * 250 + 100, y: row * 150 + 50 },
          data: { label, status: "Pending", duration: 0 }
        };
      });

      const defaultEdges = [];
      for (let i = 0; i < defaultAgents.length - 1; i++) {
        defaultEdges.push({
          id: `e-default-${i}-${i+1}`,
          source: `default-${i}`,
          target: `default-${i+1}`,
          animated: false,
          style: { stroke: '#E7EAF2', strokeWidth: 1.5 },
          markerEnd: { type: MarkerType.ArrowClosed, color: '#E7EAF2' },
        });
      }
      
      setNodes(defaultNodes);
      setEdges(defaultEdges);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusData]);

  const headerActions = (
    <div className="flex items-center space-x-3">
      <div className="flex items-center bg-white border border-[#E7EAF2] rounded-xl px-3 py-1.5 shadow-sm">
        <Database className="w-4 h-4 text-[#5B5CEB] mr-2" />
        <div className="relative flex items-center">
          <select 
            value={selectedDataset || ""} 
            onChange={(e) => setSelectedDataset(e.target.value)}
            className="bg-transparent text-xs font-bold text-[#111827] focus:outline-none w-48 pr-6 cursor-pointer appearance-none"
          >
            <option value="" disabled>Select Context</option>
            {history?.map((d: any, i: number) => (
              <option key={i} value={d.name}>{d.name}</option>
            ))}
          </select>
          <ChevronRight className="w-3.5 h-3.5 text-[#9CA3AF] pointer-events-none absolute right-0 rotate-90" />
        </div>
      </div>
      
      <GradientButton 
        onClick={() => startMutation.mutate()}
        disabled={statusData?.state === 'RUNNING' || !selectedDataset}
        className="h-10 min-w-[140px] shadow-sm active:scale-98"
      >
        {statusData?.state === 'RUNNING' ? (
          <>
            <Loader2 className="w-4 h-4 mr-2 animate-spin text-white" /> 
            <span>Orchestrating...</span>
          </>
        ) : (
          <>
            <PlayCircle className="w-4 h-4 mr-2 text-white" /> 
            <span>Start Agents Swarm</span>
          </>
        )}
      </GradientButton>
    </div>
  );

  return (
    <div className="h-[calc(100vh-100px)] flex flex-col font-sans max-w-7xl mx-auto px-4 md:px-8 space-y-6">
      
      <div className="shrink-0">
        <SectionHeader 
          title="LangGraph Workflow Orchestration" 
          description="Visualize multi-agent communication and autonomous pipeline execution."
          actions={headerActions}
        />
      </div>

      {/* React Flow Workspace */}
      <div className="flex-1 border border-[#E7EAF2] rounded-3xl overflow-hidden bg-[#F8F9FC] shadow-[0_8px_30px_rgb(0,0,0,0.005)] relative select-none">
        
        <div className="absolute top-4 left-4 z-10 bg-white border border-[#E7EAF2] shadow-sm rounded-2xl p-4 flex flex-col space-y-2">
          <h4 className="text-[10px] font-bold text-[#6B7280] uppercase tracking-wider">Swarm Process Status</h4>
          <div className="flex items-center">
            <span className="relative flex h-2 w-2 mr-2">
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                statusData?.state === 'RUNNING' ? 'bg-[#5B5CEB]' : statusData?.state === 'COMPLETED' ? 'bg-[#16A34A]' : 'bg-[#9CA3AF]'
              }`} />
              <span className={`relative inline-flex rounded-full h-2 w-2 ${
                statusData?.state === 'RUNNING' ? 'bg-[#5B5CEB]' : statusData?.state === 'COMPLETED' ? 'bg-[#16A34A]' : 'bg-[#9CA3AF]'
              }`} />
            </span>
            <span className="text-xs font-mono font-bold text-[#4B5563]">{statusData?.state || 'IDLE'}</span>
          </div>
        </div>

        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          fitView
          attributionPosition="bottom-right"
        >
          <Background color="#E7EAF2" gap={16} size={1} />
          <Controls className="bg-white border-[#E7EAF2] shadow-sm !rounded-2xl overflow-hidden" />
          <MiniMap className="!bg-white !border !border-[#E7EAF2] !rounded-2xl !shadow-sm overflow-hidden" />
        </ReactFlow>
      </div>

      <FloatingAIButton />
    </div>
  );
}
