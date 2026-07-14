"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { HelpCircle, Bot, X, Send, Loader2 } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

// 1. Page Container
export function PageContainer({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`min-h-screen bg-[#F8F9FC] text-[#111827] font-sans pb-16 max-w-7xl mx-auto px-4 md:px-8 space-y-8 select-none ${className}`}>
      {children}
    </div>
  );
}

// 2. Section Header
export function SectionHeader({ 
  title, 
  description, 
  actions 
}: { 
  title: string; 
  description: string; 
  actions?: React.ReactNode 
}) {
  return (
    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[#E7EAF2] pb-6">
      <div className="space-y-1">
        <h1 className="text-3xl font-extrabold tracking-tight text-[#111827]">{title}</h1>
        <p className="text-sm text-[#6B7280]">{description}</p>
      </div>
      {actions && <div className="flex items-center space-x-3 shrink-0">{actions}</div>}
    </div>
  );
}

// 3. Card Container
export function Card({ 
  children, 
  className = "", 
  hover = true 
}: { 
  children: React.ReactNode; 
  className?: string; 
  hover?: boolean 
}) {
  return (
    <motion.div
      whileHover={hover ? { 
        y: -4, 
        scale: 1.002,
        borderColor: "rgba(91, 92, 235, 0.3)",
        boxShadow: "0 12px 24px rgba(91, 92, 235, 0.03), 0 4px 12px rgba(0,0,0,0.01)" 
      } : {}}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className={`bg-white border border-[#E7EAF2] rounded-[20px] p-6 md:p-8 shadow-[0_8px_30px_rgba(0,0,0,0.003)] ${className}`}
    >
      {children}
    </motion.div>
  );
}

// 4. Stat Card
export function StatCard({
  title,
  value,
  icon,
  trend,
  trendType = "neutral",
  children
}: {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: string;
  trendType?: "success" | "warning" | "error" | "neutral";
  children?: React.ReactNode;
}) {
  const getTrendColor = () => {
    switch (trendType) {
      case "success": return "text-[#16A34A] bg-[#16A34A]/5 border-[#16A34A]/10";
      case "warning": return "text-[#F59E0B] bg-[#F59E0B]/5 border-[#F59E0B]/10";
      case "error": return "text-[#EF4444] bg-[#EF4444]/5 border-[#EF4444]/10";
      default: return "text-[#6B7280] bg-[#F6F7FB] border-[#E7EAF2]";
    }
  };

  return (
    <Card className="flex flex-col justify-between h-40">
      <div className="flex justify-between items-start">
        <div className="space-y-1">
          <p className="text-[11px] font-bold text-[#6B7280] uppercase tracking-wider">{title}</p>
          <h3 className="text-2xl font-extrabold text-[#111827] tracking-tight">{value}</h3>
        </div>
        <div className="w-10 h-10 rounded-xl bg-[#F8F9FC] border border-[#E7EAF2] flex items-center justify-center text-[#5B5CEB]">
          {icon}
        </div>
      </div>
      <div className="flex justify-between items-end">
        {trend ? (
          <span className={`px-2 py-0.5 rounded-lg border text-[10px] font-bold flex items-center ${getTrendColor()}`}>
            {trend}
          </span>
        ) : <div />}
        {children}
      </div>
    </Card>
  );
}

// 5. Empty State
export function EmptyState({
  title,
  description,
  type = "generic",
  primaryAction,
  secondaryAction,
  actionText,
  onAction,
  icon
}: {
  title: string;
  description: string;
  type?: "dataset" | "model" | "report" | "neural-network" | "feature-engineering" | "ai-agent" | "data-pipeline" | "scatter-plot" | "decision-tree" | "correlation-heatmap" | "generic";
  primaryAction?: { label: string; onClick: () => void };
  secondaryAction?: { label: string; onClick: () => void };
  actionText?: string;
  onAction?: () => void;
  icon?: React.ReactNode;
}) {
  const renderIllustration = () => {
    switch (type) {
      case "dataset":
        return (
          <svg className="w-24 h-24 text-[#5B5CEB] mb-6 animate-pulse" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="25" y="30" width="50" height="60" rx="8" stroke="currentColor" strokeWidth="2.5" fill="none" strokeDasharray="3 3" />
            <rect x="35" y="15" width="30" height="20" rx="4" stroke="currentColor" strokeWidth="2.5" fill="white" />
            <path d="M50 40v30M40 55l10-10 10 10" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
            <circle cx="20" cy="40" r="2" fill="#7C4DFF" />
            <circle cx="80" cy="65" r="3" fill="#16A34A" />
            <circle cx="75" cy="30" r="2" fill="#F59E0B" />
          </svg>
        );
      case "model":
        return (
          <svg className="w-24 h-24 text-[#7C4DFF] mb-6" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="28" y="28" width="44" height="40" rx="10" stroke="currentColor" strokeWidth="2.5" fill="white" />
            <circle cx="41" cy="44" r="4.5" fill="currentColor" />
            <circle cx="59" cy="44" r="4.5" fill="currentColor" />
            <path d="M41 40h5m8 0h5" stroke="white" strokeWidth="1" />
            <path d="M42 56h16" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
            <rect x="21" y="40" width="7" height="16" rx="3.5" fill="currentColor" />
            <rect x="72" y="40" width="7" height="16" rx="3.5" fill="currentColor" />
            <path d="M50 28V18" stroke="currentColor" strokeWidth="2.5" />
            <circle cx="50" cy="14" r="4" fill="#5B5CEB" />
            <path d="M15 25l2 2-2 2-2-2 2-2zm70 50l2 2-2 2-2-2 2-2z" fill="#F59E0B" />
          </svg>
        );
      case "report":
        return (
          <svg className="w-24 h-24 text-[#16A34A] mb-6" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="25" y="15" width="50" height="70" rx="8" stroke="currentColor" strokeWidth="2.5" fill="white" />
            <path d="M35 30h30M35 42h20M35 54h30" stroke="currentColor" strokeWidth="2" strokeLinecap="round" opacity="0.4" />
            <circle cx="60" cy="62" r="10" stroke="currentColor" strokeWidth="2" strokeDasharray="40 10" />
            <rect x="35" y="60" width="8" height="10" rx="1.5" fill="#5B5CEB" />
            <rect x="45" y="55" width="8" height="15" rx="1.5" fill="currentColor" />
            <path d="M78 25l6 6M84 25l-6 6" stroke="#F59E0B" strokeWidth="2" strokeLinecap="round" />
          </svg>
        );
      case "neural-network":
        return (
          <svg className="w-24 h-24 mb-6" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>{`
              @keyframes pulse-path {
                0% { stroke-dashoffset: 24; }
                100% { stroke-dashoffset: 0; }
              }
              .nn-pulse {
                stroke-dasharray: 6 6;
                animation: pulse-path 1.5s linear infinite;
              }
              @keyframes pulse-node {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.15); opacity: 0.9; }
              }
              .nn-node {
                transform-origin: center;
                animation: pulse-node 2.5s ease-in-out infinite;
              }
            `}</style>
            <path d="M20 40 L50 20" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            <path d="M20 40 L50 45" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            <path d="M20 40 L50 70" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            <path d="M20 40 L50 95" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            
            <path d="M20 60 L50 20" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            <path d="M20 60 L50 45" stroke="#7C4DFF" strokeWidth="1.5" strokeDasharray="6 6" className="nn-pulse" />
            <path d="M20 60 L50 70" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            <path d="M20 60 L50 95" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />

            <path d="M20 80 L50 20" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            <path d="M20 80 L50 45" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            <path d="M20 80 L50 70" stroke="#7C4DFF" strokeWidth="1.5" opacity="0.3" />
            <path d="M20 80 L50 95" stroke="#7C4DFF" strokeWidth="1.5" strokeDasharray="6 6" className="nn-pulse" />

            <path d="M50 20 L80 40" stroke="#7C4DFF" strokeWidth="1.5" opacity="0.3" />
            <path d="M50 20 L80 75" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            <path d="M50 45 L80 40" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            <path d="M50 45 L80 75" stroke="#7C4DFF" strokeWidth="1.5" strokeDasharray="6 6" className="nn-pulse" />
            <path d="M50 70 L80 40" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            <path d="M50 70 L80 75" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />
            <path d="M50 95 L80 40" stroke="#7C4DFF" strokeWidth="1.5" opacity="0.3" />
            <path d="M50 95 L80 75" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />

            <path d="M80 40 L105 57" stroke="#16A34A" strokeWidth="2" strokeDasharray="4 4" className="nn-pulse" />
            <path d="M80 75 L105 57" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.3" />

            <circle cx="20" cy="40" r="5" fill="white" stroke="#5B5CEB" strokeWidth="2.5" />
            <circle cx="20" cy="60" r="5" fill="#5B5CEB" stroke="#5B5CEB" strokeWidth="1" />
            <circle cx="20" cy="80" r="5" fill="white" stroke="#5B5CEB" strokeWidth="2.5" />

            <circle cx="50" cy="20" r="5.5" fill="white" stroke="#7C4DFF" strokeWidth="2.5" />
            <circle cx="50" cy="45" r="5.5" fill="#7C4DFF" stroke="#7C4DFF" strokeWidth="1" />
            <circle cx="50" cy="70" r="5.5" fill="white" stroke="#7C4DFF" strokeWidth="2.5" />
            <circle cx="50" cy="95" r="5.5" fill="#7C4DFF" stroke="#7C4DFF" strokeWidth="1" />

            <circle cx="80" cy="40" r="6" fill="#5B5CEB" stroke="#5B5CEB" strokeWidth="1" className="nn-node" />
            <circle cx="80" cy="75" r="6" fill="white" stroke="#5B5CEB" strokeWidth="2.5" className="nn-node" />

            <circle cx="105" cy="57" r="7.5" fill="#16A34A" stroke="#16A34A" strokeWidth="1" className="nn-node" style={{ animationDelay: '0.4s' }} />
            <path d="M102 57l2 2 3-3" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        );
      case "feature-engineering":
        return (
          <svg className="w-24 h-24 mb-6" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>{`
              @keyframes rotate-gear {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
              }
              .fe-gear {
                transform-origin: 35px 35px;
                animation: rotate-gear 8s linear infinite;
              }
              @keyframes slide-vector {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(6px); }
              }
              .fe-vector {
                animation: slide-vector 3s ease-in-out infinite;
              }
            `}</style>
            <rect x="10" y="10" width="100" height="100" rx="16" fill="#F8F9FC" stroke="#E7EAF2" strokeWidth="1.5" />
            
            <g className="fe-gear" opacity="0.15">
              <circle cx="35" cy="35" r="16" stroke="#5B5CEB" strokeWidth="2" strokeDasharray="6 4" />
              <circle cx="35" cy="35" r="8" fill="#5B5CEB" />
            </g>
            
            <rect x="20" y="65" width="24" height="8" rx="2" fill="white" stroke="#9CA3AF" strokeWidth="1.5" />
            <rect x="20" y="77" width="24" height="8" rx="2" fill="white" stroke="#9CA3AF" strokeWidth="1.5" />
            <rect x="20" y="89" width="24" height="8" rx="2" fill="white" stroke="#9CA3AF" strokeWidth="1.5" />
            
            <path d="M52 81 H68" stroke="#5B5CEB" strokeWidth="2" strokeLinecap="round" strokeDasharray="4 2" />
            <path d="M64 77 l4 4 -4 4" stroke="#5B5CEB" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />

            <g className="fe-vector">
              <rect x="76" y="60" width="24" height="12" rx="3.5" fill="#5B5CEB" />
              <rect x="76" y="76" width="24" height="12" rx="3.5" fill="#7C4DFF" />
              <rect x="76" y="92" width="24" height="12" rx="3.5" fill="#16A34A" />
              
              <line x1="81" y1="66" x2="95" y2="66" stroke="white" strokeWidth="2" strokeLinecap="round" />
              <line x1="81" y1="82" x2="91" y2="82" stroke="white" strokeWidth="2" strokeLinecap="round" />
              <line x1="81" y1="98" x2="93" y2="98" stroke="white" strokeWidth="2" strokeLinecap="round" />
            </g>

            <text x="68" y="32" fill="#7C4DFF" fontSize="9" fontWeight="bold" fontFamily="monospace">x &rarr; f(x)</text>
            <circle cx="85" cy="85" r="4" fill="#F59E0B" opacity="0.8" />
          </svg>
        );
      case "ai-agent":
        return (
          <svg className="w-24 h-24 mb-6" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>{`
              @keyframes orbit {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
              }
              .agent-orbit {
                transform-origin: 60px 60px;
                animation: orbit 10s linear infinite;
              }
              @keyframes agent-pulse {
                0%, 100% { filter: drop-shadow(0 0 2px rgba(91,92,235,0.2)); }
                50% { filter: drop-shadow(0 0 8px rgba(91,92,235,0.6)); }
              }
              .agent-core {
                animation: agent-pulse 2.5s ease-in-out infinite;
              }
            `}</style>
            
            <circle cx="60" cy="60" r="36" stroke="#E7EAF2" strokeWidth="1.5" strokeDasharray="4 4" />
            <circle cx="60" cy="60" r="20" stroke="#E7EAF2" strokeWidth="1" />
            
            <line x1="60" y1="60" x2="60" y2="24" stroke="#5B5CEB" strokeWidth="1.5" opacity="0.4" />
            <line x1="60" y1="60" x2="88" y2="78" stroke="#7C4DFF" strokeWidth="1.5" opacity="0.4" />
            <line x1="60" y1="60" x2="32" y2="78" stroke="#7C4DFF" strokeWidth="1.5" opacity="0.4" />

            <g className="agent-orbit">
              <circle cx="60" cy="24" r="6" fill="#16A34A" />
              <circle cx="60" cy="24" r="9" stroke="#16A34A" strokeWidth="1" opacity="0.3" />
              <circle cx="88" cy="78" r="6" fill="#F59E0B" />
              <circle cx="32" cy="78" r="6" fill="#7C4DFF" />
            </g>

            <rect className="agent-core" x="48" y="48" width="24" height="24" rx="8" fill="#5B5CEB" stroke="white" strokeWidth="2.5" />
            <circle cx="60" cy="60" r="4" fill="white" />
            
            <path d="M22 28l2-2-2-2 2 2zm78-4l3 3-3 3 3-3z" fill="#7C4DFF" opacity="0.8" />
          </svg>
        );
      case "data-pipeline":
        return (
          <svg className="w-24 h-24 mb-6" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>{`
              @keyframes flow-dots {
                0% { stroke-dashoffset: 40; }
                100% { stroke-dashoffset: 0; }
              }
              .pipe-flow {
                stroke-dasharray: 8 8;
                animation: flow-dots 2s linear infinite;
              }
            `}</style>
            
            <g fill="white" stroke="#9CA3AF" strokeWidth="1.5">
              <path d="M15 25 c0-3 12-3 12-3 s12 0 12 3 v10 c0 3-12 3-12 3 s-12 0-12-3 Z" />
              <path d="M15 35 c0 3 12 3 12 3 s12 0 12-3 v10 c0 3-12 3-12 3 s-12 0-12-3 Z" />
              <path d="M15 45 c0 3 12 3 12 3 s12 0 12-3 v10 c0 3-12 3-12 3 s-12 0-12-3 Z" fill="#5B5CEB" stroke="#5B5CEB" />
            </g>
            
            <path d="M39 40 C60 40, 50 80, 80 80" stroke="#E7EAF2" strokeWidth="4" strokeLinecap="round" />
            <path d="M39 40 C60 40, 50 80, 80 80" stroke="#7C4DFF" strokeWidth="2.5" strokeLinecap="round" className="pipe-flow" />

            <path d="M39 40 H80" stroke="#E7EAF2" strokeWidth="4" strokeLinecap="round" />
            <path d="M39 40 H80" stroke="#5B5CEB" strokeWidth="2.5" strokeLinecap="round" className="pipe-flow" />

            <rect x="48" y="28" width="24" height="24" rx="6" fill="white" stroke="#7C4DFF" strokeWidth="2.5" />
            <path d="M54 40h12M60 34v12" stroke="#7C4DFF" strokeWidth="1.5" strokeLinecap="round" />

            <g fill="white" stroke="#16A34A" strokeWidth="1.5">
              <rect x="80" y="30" width="24" height="24" rx="5" fill="#16A34A" stroke="#16A34A" />
              <line x1="86" y1="38" x2="98" y2="38" stroke="white" strokeWidth="2" strokeLinecap="round" />
              <line x1="86" y1="44" x2="94" y2="44" stroke="white" strokeWidth="2" strokeLinecap="round" />
              
              <rect x="80" y="68" width="24" height="24" rx="5" />
              <line x1="86" y1="76" x2="98" y2="76" stroke="#16A34A" strokeWidth="2" strokeLinecap="round" opacity="0.6" />
              <line x1="86" y1="82" x2="92" y2="82" stroke="#16A34A" strokeWidth="2" strokeLinecap="round" opacity="0.6" />
            </g>
          </svg>
        );
      case "scatter-plot":
        return (
          <svg className="w-24 h-24 mb-6" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>{`
              @keyframes pulse-points {
                0%, 100% { r: 3.5; opacity: 0.8; }
                50% { r: 5; opacity: 1; }
              }
              .sp-dot {
                animation: pulse-points 2s ease-in-out infinite;
              }
            `}</style>
            <line x1="20" y1="20" x2="20" y2="100" stroke="#9CA3AF" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="20" y1="100" x2="100" y2="100" stroke="#9CA3AF" strokeWidth="1.5" strokeLinecap="round" />
            
            <path d="M22 88 L100 28 L100 48 L22 96 Z" fill="#5B5CEB" opacity="0.08" />

            <line x1="20" y1="92" x2="100" y2="36" stroke="#5B5CEB" strokeWidth="2" strokeLinecap="round" />

            <circle className="sp-dot" cx="30" cy="80" r="4" fill="#7C4DFF" style={{ animationDelay: '0s' }} />
            <circle className="sp-dot" cx="42" cy="74" r="4.5" fill="#5B5CEB" style={{ animationDelay: '0.4s' }} />
            <circle className="sp-dot" cx="50" cy="82" r="3.5" fill="#7C4DFF" style={{ animationDelay: '0.8s' }} />
            <circle className="sp-dot" cx="58" cy="62" r="4" fill="#5B5CEB" style={{ animationDelay: '0.2s' }} />
            <circle className="sp-dot" cx="64" cy="50" r="4" fill="#F59E0B" style={{ animationDelay: '1.2s' }} />
            <circle className="sp-dot" cx="72" cy="58" r="3.5" fill="#7C4DFF" style={{ animationDelay: '0.6s' }} />
            <circle className="sp-dot" cx="80" cy="46" r="4.5" fill="#16A34A" style={{ animationDelay: '0.1s' }} />
            <circle className="sp-dot" cx="88" cy="40" r="3.5" fill="#5B5CEB" style={{ animationDelay: '1.5s' }} />
            <circle className="sp-dot" cx="95" cy="30" r="4" fill="#16A34A" style={{ animationDelay: '0.5s' }} />
            
            <circle className="sp-dot" cx="40" cy="40" r="3" fill="#EF4444" style={{ animationDelay: '1.8s' }} />
            <circle className="sp-dot" cx="85" cy="85" r="3.5" fill="#EF4444" style={{ animationDelay: '0.9s' }} />
          </svg>
        );
      case "decision-tree":
        return (
          <svg className="w-24 h-24 mb-6" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M60 20 L35 50" stroke="#5B5CEB" strokeWidth="2" strokeLinecap="round" />
            <path d="M60 20 L85 50" stroke="#7C4DFF" strokeWidth="2" strokeLinecap="round" />
            
            <path d="M35 50 L20 80" stroke="#5B5CEB" strokeWidth="1.5" strokeLinecap="round" />
            <path d="M35 50 L50 80" stroke="#16A34A" strokeWidth="1.5" strokeLinecap="round" />

            <path d="M85 50 L70 80" stroke="#7C4DFF" strokeWidth="1.5" strokeLinecap="round" />
            <path d="M85 50 L100 80" stroke="#EF4444" strokeWidth="1.5" strokeLinecap="round" />

            <rect x="48" y="10" width="24" height="18" rx="4" fill="white" stroke="#5B5CEB" strokeWidth="2.5" />
            <text x="60" y="22" fill="#5B5CEB" fontSize="9" fontWeight="bold" textAnchor="middle" fontFamily="monospace">x&lt;5</text>

            <rect x="23" y="41" width="24" height="18" rx="4" fill="#5B5CEB" stroke="#5B5CEB" strokeWidth="1" />
            <text x="35" y="53" fill="white" fontSize="9" fontWeight="bold" textAnchor="middle" fontFamily="monospace">y&gt;2</text>

            <rect x="73" y="41" width="24" height="18" rx="4" fill="white" stroke="#7C4DFF" strokeWidth="2.5" />
            <text x="85" y="53" fill="#7C4DFF" fontSize="9" fontWeight="bold" textAnchor="middle" fontFamily="monospace">z&lt;0</text>

            <circle cx="20" cy="80" r="5" fill="#5B5CEB" />
            <circle cx="50" cy="80" r="5" fill="#16A34A" />
            <circle cx="70" cy="80" r="5" fill="#7C4DFF" />
            <circle cx="100" cy="80" r="5" fill="#EF4444" />
          </svg>
        );
      case "correlation-heatmap":
        return (
          <svg className="w-24 h-24 mb-6" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="15" y="15" width="90" height="90" rx="12" fill="#F8F9FC" stroke="#E7EAF2" strokeWidth="1.5" />
            
            <rect x="23" y="23" width="18" height="18" rx="3" fill="#5B5CEB" />
            <rect x="44" y="23" width="18" height="18" rx="3" fill="#5B5CEB" opacity="0.6" />
            <rect x="65" y="23" width="18" height="18" rx="3" fill="#7C4DFF" opacity="0.3" />
            <rect x="86" y="23" width="18" height="18" rx="3" fill="#EF4444" opacity="0.1" />

            <rect x="23" y="44" width="18" height="18" rx="3" fill="#5B5CEB" opacity="0.6" />
            <rect x="44" y="44" width="18" height="18" rx="3" fill="#5B5CEB" />
            <rect x="65" y="44" width="18" height="18" rx="3" fill="#7C4DFF" opacity="0.7" />
            <rect x="86" y="44" width="18" height="18" rx="3" fill="#EF4444" opacity="0.4" />

            <rect x="23" y="65" width="18" height="18" rx="3" fill="#7C4DFF" opacity="0.3" />
            <rect x="44" y="65" width="18" height="18" rx="3" fill="#7C4DFF" opacity="0.7" />
            <rect x="65" y="65" width="18" height="18" rx="3" fill="#7C4DFF" />
            <rect x="86" y="65" width="18" height="18" rx="3" fill="#16A34A" opacity="0.5" />

            <rect x="23" y="86" width="18" height="18" rx="3" fill="#EF4444" opacity="0.1" />
            <rect x="44" y="86" width="18" height="18" rx="3" fill="#EF4444" opacity="0.4" />
            <rect x="65" y="86" width="18" height="18" rx="3" fill="#16A34A" opacity="0.5" />
            <rect x="86" y="86" width="18" height="18" rx="3" fill="#16A34A" />

            <text x="32" y="11" fill="#9CA3AF" fontSize="6" fontWeight="bold" textAnchor="middle">col_A</text>
            <text x="53" y="11" fill="#9CA3AF" fontSize="6" fontWeight="bold" textAnchor="middle">col_B</text>
            <text x="74" y="11" fill="#9CA3AF" fontSize="6" fontWeight="bold" textAnchor="middle">col_C</text>
            <text x="95" y="11" fill="#9CA3AF" fontSize="6" fontWeight="bold" textAnchor="middle">col_D</text>
          </svg>
        );
      default:
        return (
          <div className="w-16 h-16 bg-[#F8F9FC] border border-[#E7EAF2] rounded-2xl flex items-center justify-center mb-6 text-[#6B7280]">
            {icon || <HelpCircle className="w-8 h-8 text-[#9CA3AF]" />}
          </div>
        );
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-10 md:p-14 text-center bg-white border border-[#E7EAF2] rounded-[24px] max-w-lg mx-auto shadow-[0_8px_30px_rgba(0,0,0,0.01)] transition-all">
      {renderIllustration()}
      <h3 className="text-lg font-bold text-[#111827] mb-2">{title}</h3>
      <p className="text-xs md:text-sm text-[#6B7280] mb-8 leading-relaxed max-w-sm">{description}</p>
      <div className="flex flex-col sm:flex-row items-center justify-center gap-3 w-full sm:w-auto">
        {actionText && onAction && (
          <GradientButton onClick={onAction} className="px-6 py-2.5 w-full sm:w-auto">
            {actionText}
          </GradientButton>
        )}
        {primaryAction && (
          <GradientButton onClick={primaryAction.onClick} className="px-6 py-2.5 w-full sm:w-auto shadow-sm">
            {primaryAction.label}
          </GradientButton>
        )}
        {secondaryAction && (
          <button 
            type="button"
            onClick={secondaryAction.onClick} 
            className="px-5 py-2.5 border border-[#E7EAF2] hover:bg-[#F8F9FC] text-[#4B5563] text-xs font-bold rounded-xl transition-all cursor-pointer w-full sm:w-auto active:scale-98 shadow-sm bg-white"
          >
            {secondaryAction.label}
          </button>
        )}
      </div>
    </div>
  );
}

// 6. Loading Skeleton
export function LoadingSkeleton({ className = "h-4 w-full" }: { className?: string }) {
  return (
    <div className={`bg-gradient-to-r from-[#F8F9FC] via-[#EEF2F6] to-[#F8F9FC] bg-[length:200%_100%] animate-[shimmer_1.5s_infinite] rounded-xl ${className}`}>
      <style>{`
        @keyframes shimmer {
          0% { background-position: -200% 0; }
          100% { background-position: 200% 0; }
        }
      `}</style>
    </div>
  );
}

export function CardSkeleton() {
  return (
    <div className="bg-white border border-[#E7EAF2] rounded-[20px] p-6 space-y-4">
      <div className="flex justify-between items-start">
        <div className="space-y-2 flex-grow">
          <LoadingSkeleton className="h-3 w-1/4" />
          <LoadingSkeleton className="h-6 w-1/2" />
        </div>
        <LoadingSkeleton className="w-10 h-10 rounded-xl" />
      </div>
      <div className="pt-2">
        <LoadingSkeleton className="h-4 w-3/4" />
      </div>
    </div>
  );
}

export function ChartSkeleton({ type = "bar" }: { type?: "bar" | "line" | "area" }) {
  return (
    <div className="bg-white border border-[#E7EAF2] rounded-[20px] p-6 space-y-6">
      <div className="space-y-2">
        <LoadingSkeleton className="h-3.5 w-1/3" />
        <LoadingSkeleton className="h-3 w-1/4" />
      </div>
      <div className="h-48 flex items-end justify-between gap-3 pt-6 border-b border-[#E7EAF2]">
        {type === "bar" ? (
          <>
            <LoadingSkeleton className="h-[40%] flex-1" />
            <LoadingSkeleton className="h-[75%] flex-1" />
            <LoadingSkeleton className="h-[55%] flex-1" />
            <LoadingSkeleton className="h-[90%] flex-1" />
            <LoadingSkeleton className="h-[60%] flex-1" />
            <LoadingSkeleton className="h-[80%] flex-1" />
          </>
        ) : (
          <div className="w-full h-full relative flex items-center justify-center">
            <svg className="w-full h-full text-[#EEF2F6]" viewBox="0 0 400 150">
              <path d="M0,100 Q80,50 160,80 T320,30 T400,60" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" opacity="0.4" />
              <path d="M0,100 Q80,50 160,80 T320,30 T400,60 L400,150 L0,150 Z" fill="currentColor" opacity="0.1" />
            </svg>
            <LoadingSkeleton className="absolute w-[20%] h-4 rounded-full" />
          </div>
        )}
      </div>
      <div className="flex justify-between items-center text-[10px] text-[#9CA3AF] font-bold">
        <LoadingSkeleton className="h-3 w-1/5" />
        <LoadingSkeleton className="h-3 w-1/6" />
      </div>
    </div>
  );
}

export function TableSkeleton({ rows = 4 }: { rows?: number }) {
  return (
    <div className="bg-white border border-[#E7EAF2] rounded-[20px] p-6 space-y-4">
      <div className="flex justify-between items-center border-b border-[#E7EAF2] pb-3">
        <LoadingSkeleton className="h-4 w-1/3" />
        <LoadingSkeleton className="h-4 w-8" />
      </div>
      <div className="space-y-3">
        {Array.from({ length: rows }).map((_, i) => (
          <div key={i} className="flex justify-between items-center p-3 border border-[#E7EAF2] rounded-xl bg-[#F8F9FC]">
            <div className="flex items-center space-x-3 w-2/3">
              <LoadingSkeleton className="w-6 h-6 rounded-lg" />
              <div className="space-y-1.5 flex-grow">
                <LoadingSkeleton className="h-3 w-1/2" />
                <LoadingSkeleton className="h-2 w-1/3" />
              </div>
            </div>
            <LoadingSkeleton className="h-4 w-12 rounded-lg" />
          </div>
        ))}
      </div>
    </div>
  );
}

// 7. Status Badge
export function StatusBadge({ 
  status, 
  type = "neutral" 
}: { 
  status: string; 
  type?: "success" | "warning" | "error" | "neutral" | "running" 
}) {
  const getColors = () => {
    switch (type) {
      case "success": return "bg-[#F0FDF4] text-[#16A34A] border-[#BBF7D0]";
      case "warning": return "bg-[#FFFBEB] text-[#F59E0B] border-[#FEF3C7]";
      case "error": return "bg-[#FEF2F2] text-[#EF4444] border-[#FEE2E2]";
      case "running": return "bg-[#EEF2F6] text-[#5B5CEB] border-[#E7EAF2]";
      default: return "bg-[#F8F9FC] text-[#6B7280] border-[#E7EAF2]";
    }
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-lg text-[10px] font-bold border ${getColors()}`}>
      {type === "running" && <span className="w-1.5 h-1.5 rounded-full bg-[#5B5CEB] animate-pulse mr-1.5" />}
      {status}
    </span>
  );
}

// 8. Gradient Button
export function GradientButton({
  children,
  onClick,
  className = "",
  disabled = false,
  type = "button"
}: {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
  disabled?: boolean;
  type?: "button" | "submit" | "reset";
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`px-5 py-2.5 bg-[#5B5CEB] hover:bg-[#4E4FD6] active:scale-98 text-white rounded-xl text-xs font-bold transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:scale-100 flex items-center justify-center space-x-1.5 cursor-pointer ${className}`}
    >
      {children}
    </button>
  );
}

// 9. Animated Number / Counter
export function AnimatedCounter({ 
  value, 
  duration = 0.25, 
  decimals = 0,
  prefix = "",
  suffix = ""
}: { 
  value: number; 
  duration?: number; 
  decimals?: number;
  prefix?: string;
  suffix?: string;
}) {
  const [display, setDisplay] = useState(prefix + (0).toFixed(decimals) + suffix);

  useEffect(() => {
    const start = 0;
    const end = value;
    if (start === end) {
      setDisplay(prefix + end.toFixed(decimals) + suffix);
      return;
    }

    const startTime = performance.now();
    const durationMs = Math.min(duration * 1000, 300); // Strict limit below 300ms

    let animationFrameId: number;

    const updateCount = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / durationMs, 1);
      
      // Ease out quad
      const easeProgress = progress * (2 - progress);
      const current = start + (end - start) * easeProgress;

      setDisplay(prefix + current.toFixed(decimals) + suffix);

      if (progress < 1) {
        animationFrameId = requestAnimationFrame(updateCount);
      }
    };

    animationFrameId = requestAnimationFrame(updateCount);
    return () => cancelAnimationFrame(animationFrameId);
  }, [value, duration, decimals, prefix, suffix]);

  return <span className="font-mono">{display}</span>;
}

export function AnimatedNumber({ value }: { value: number | string }) {
  const numVal = typeof value === 'string' ? parseFloat(value) : value;
  if (!isNaN(numVal) && isFinite(numVal)) {
    return <AnimatedCounter value={numVal} />;
  }
  return (
    <motion.span 
      key={value}
      initial={{ opacity: 0, y: -2 }}
      animate={{ opacity: 1, y: 0 }}
      className="font-mono"
    >
      {value}
    </motion.span>
  );
}

// 10. Floating AI Assistant Button
export function FloatingAIButton() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([
    {
      role: 'assistant',
      content: "Hi! I am the Agentix AI Analyst Copilot. I can clean columns, train AutoML leaderboards, interpret variables, or compile briefings. Ask me anything about your active dataset!"
    }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch telemetry to know the active dataset
  const { data: telemetryData } = useQuery({
    queryKey: ['floatingTelemetryDataset'],
    queryFn: async () => {
      try {
        const res = await axios.get('/api/dashboard');
        return res.data.data.telemetry;
      } catch {
        return { active_dataset: "Sales Data" };
      }
    }
  });

  const activeDataset = telemetryData?.active_dataset || "Sales Data";

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      setTimeout(scrollToBottom, 100);
    }
  }, [messages, isOpen, isTyping]);

  const handleSend = async (queryText: string) => {
    if (!queryText.trim()) return;
    
    const userMsg = { role: 'user' as const, content: queryText };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/chat`, {
        query: queryText,
        dataset_name: activeDataset
      });
      const responseText = res.data.data?.response || "I have processed your request.";
      setMessages(prev => [...prev, { role: 'assistant', content: responseText }]);
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: "I encountered an error communicating with the local Ollama service cluster." }]);
    } finally {
      setIsTyping(false);
    }
  };

  const suggestedPrompts = [
    { label: "Explain my dataset", query: "Explain my active dataset schema, records, and distribution parameters." },
    { label: "Clean my data", query: "Run data cleaning agent passes to resolve missing values." },
    { label: "Build a model", query: "Explain how to build a champion model on this dataset using AutoML." },
    { label: "Show feature importance", query: "Calculate SHAP game-theoretic drivers and feature importances." },
    { label: "Export report", query: "Generate a downloadable PDF executive summary briefing." }
  ];

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end select-text text-left font-sans">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 30, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 30, scale: 0.95 }}
            transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className="w-[360px] sm:w-[400px] h-[550px] bg-white border border-[#E7EAF2] rounded-[24px] shadow-2xl flex flex-col overflow-hidden mb-4"
          >
            {/* Header */}
            <div className="p-4 bg-gradient-to-r from-[#5B5CEB] to-[#7C4DFF] text-white flex items-center justify-between shadow-sm">
              <div className="flex items-center space-x-3">
                <div className="w-9 h-9 rounded-xl bg-white/10 flex items-center justify-center border border-white/15">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h4 className="text-sm font-bold tracking-tight">Agentix AI Copilot</h4>
                  <div className="flex items-center space-x-1 mt-0.5">
                    <span className="w-1.5 h-1.5 bg-[#22C55E] rounded-full animate-pulse" />
                    <span className="text-[10px] font-bold text-white/80 uppercase tracking-wider">Ollama Swarm Live</span>
                  </div>
                </div>
              </div>
              <button 
                type="button"
                onClick={() => setIsOpen(false)}
                className="p-1.5 hover:bg-white/10 rounded-xl transition-all text-white/85 hover:text-white cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Active Context Banner */}
            <div className="px-4 py-2 bg-[#F8F9FC] border-b border-[#E7EAF2] text-[10px] text-[#6B7280] font-bold uppercase tracking-wider flex items-center justify-between">
              <span>Active dataset: {activeDataset}</span>
              <span className="text-[#5B5CEB]">V2.1</span>
            </div>

            {/* Messages Panel */}
            <div className="flex-1 p-4 overflow-y-auto space-y-3.5 scrollbar-thin bg-slate-50/30">
              {messages.map((msg, idx) => (
                <div 
                  key={idx} 
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[85%] rounded-[18px] p-3.5 text-xs font-semibold leading-relaxed shadow-[0_2px_8px_rgba(0,0,0,0.005)] ${
                    msg.role === 'user' 
                      ? 'bg-[#5B5CEB] text-white rounded-tr-none' 
                      : 'bg-white border border-[#E7EAF2] text-[#111827] rounded-tl-none'
                  }`}>
                    {msg.content}
                  </div>
                </div>
              ))}
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-white border border-[#E7EAF2] rounded-[18px] rounded-tl-none p-3.5 flex items-center space-x-1 shadow-sm">
                    <span className="w-1.5 h-1.5 bg-[#6B7280] rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-1.5 h-1.5 bg-[#6B7280] rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-1.5 h-1.5 bg-[#6B7280] rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Suggested Prompts Grid */}
            <div className="p-3 border-t border-[#E7EAF2] bg-[#F8F9FC] flex flex-wrap gap-1.5">
              {suggestedPrompts.map((p, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSend(p.query)}
                  className="px-2.5 py-1.5 rounded-lg border border-[#E7EAF2] bg-white hover:border-[#5B5CEB]/30 hover:bg-[#F8F9FC] text-[#4B5563] hover:text-[#111827] text-[10px] font-bold tracking-tight transition-all cursor-pointer select-none active:scale-95 shadow-sm"
                >
                  {p.label}
                </button>
              ))}
            </div>

            {/* Input Form */}
            <form 
              onSubmit={(e) => {
                e.preventDefault();
                handleSend(input);
              }}
              className="p-3.5 border-t border-[#E7EAF2] flex items-center space-x-2 bg-white"
            >
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask your AI analyst Copilot..."
                className="flex-grow bg-[#F8F9FC] border border-[#E7EAF2] rounded-xl px-4 py-2.5 text-xs text-[#111827] placeholder-[#9CA3AF] focus:outline-none focus:border-[#5B5CEB] focus:ring-1 focus:ring-[#5B5CEB] transition-all"
                disabled={isTyping}
              />
              <button
                type="submit"
                disabled={!input.trim() || isTyping}
                className="w-9 h-9 rounded-xl bg-[#5B5CEB] hover:bg-[#4E4FD6] disabled:opacity-50 text-white flex items-center justify-center transition-all cursor-pointer shrink-0"
              >
                {isTyping ? <Loader2 className="w-4 h-4 animate-spin text-white" /> : <Send className="w-4 h-4 text-white" />}
              </button>
            </form>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Floating Toggle Button */}
      <motion.button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="w-12 h-12 rounded-full bg-[#5B5CEB] hover:bg-[#4E4FD6] text-white flex items-center justify-center shadow-xl hover:shadow-[0_8px_30px_rgba(91,92,235,0.4)] cursor-pointer relative"
      >
        <Bot className="w-5 h-5 text-white" />
        <span className="absolute -top-1 -right-1 flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#16A34A] opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-[#16A34A]"></span>
        </span>
      </motion.button>
    </div>
  );
}

export function AgentStatusLoader() {
  const [currentStep, setCurrentStep] = React.useState(0);
  const steps = [
    "Thinking...",
    "Cleaning...",
    "Detecting Domain...",
    "Planning Workflow...",
    "Running AutoML...",
    "Generating Report...",
    "Completed"
  ];

  React.useEffect(() => {
    // Cycle through steps every 1.5 seconds, but stop at "Completed"
    const timer = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < steps.length - 1) return prev + 1;
        clearInterval(timer);
        return prev;
      });
    }, 1500);
    return () => clearInterval(timer);
  }, [steps.length]);

  return (
    <div className="w-full max-w-2xl mx-auto my-12 p-8 bg-white border border-[#E7EAF2] rounded-[24px] shadow-[0_20px_40px_rgba(91,92,235,0.08)] overflow-hidden relative">
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[#5B5CEB] to-transparent animate-[shimmer_2s_infinite]"></div>
      
      <div className="flex items-center space-x-4 mb-8 pb-6 border-b border-[#E7EAF2]">
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#5B5CEB] to-[#7C4DFF] flex items-center justify-center shadow-lg shadow-[#5B5CEB]/30 relative">
           <Bot className="w-7 h-7 text-white z-10" />
           <div className="absolute inset-0 bg-[#5B5CEB] rounded-2xl animate-ping opacity-30"></div>
        </div>
        <div>
          <h3 className="text-2xl font-extrabold text-[#111827]">Agentix AI</h3>
          <p className="text-sm font-medium text-[#5B5CEB] flex items-center">
            <Loader2 className="w-4 h-4 mr-1.5 animate-spin" />
            Executing Autonomous Pipeline
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {steps.map((step, index) => {
          const isActive = index === currentStep;
          const isPast = index < currentStep;
          
          return (
            <div key={index} className="relative">
              {index !== steps.length - 1 && (
                <div className={`absolute left-4 top-8 bottom-[-16px] w-[2px] rounded-full transition-colors duration-500 ${isPast ? "bg-[#16A34A]" : "bg-[#E7EAF2]"}`} />
              )}
              <div className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center z-10 transition-all duration-500 shadow-sm ${
                  isPast ? "bg-[#16A34A] text-white scale-100" : 
                  isActive ? "bg-[#5B5CEB] text-white scale-110 shadow-md shadow-[#5B5CEB]/40 ring-4 ring-[#5B5CEB]/20" : 
                  "bg-[#F8F9FC] text-[#9CA3AF] border-2 border-[#E7EAF2] scale-90"
                }`}>
                  {isPast ? (
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : isActive ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <div className="w-2 h-2 rounded-full bg-current" />
                  )}
                </div>
                
                <span className={`ml-4 text-lg font-semibold transition-all duration-300 ${
                  isPast ? "text-[#16A34A]" : 
                  isActive ? "text-[#111827] translate-x-1" : 
                  "text-[#9CA3AF]"
                }`}>
                  {step}
                </span>
                
                {isActive && (
                  <motion.div 
                    initial={{ opacity: 0, width: 0 }}
                    animate={{ opacity: 1, width: "auto" }}
                    className="ml-auto flex space-x-1"
                  >
                    <div className="w-1.5 h-1.5 rounded-full bg-[#5B5CEB] animate-bounce" style={{ animationDelay: "0ms" }} />
                    <div className="w-1.5 h-1.5 rounded-full bg-[#5B5CEB] animate-bounce" style={{ animationDelay: "150ms" }} />
                    <div className="w-1.5 h-1.5 rounded-full bg-[#5B5CEB] animate-bounce" style={{ animationDelay: "300ms" }} />
                  </motion.div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
