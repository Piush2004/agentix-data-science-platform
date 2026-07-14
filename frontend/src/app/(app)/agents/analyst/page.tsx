"use client";

import React, { useState, useRef, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { BrainCircuit, User, Send, Database, MessageSquare, Plus, CheckCircle2, ChevronRight } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
// Design System Imports removed since they are unused

export default function AIAnalystPage() {
  const [selectedDataset, setSelectedDataset] = useState<string | null>(null);
  const [messages, setMessages] = useState<{role: 'user'|'assistant', content: string}[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

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

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (query: string) => {
    if (!query.trim()) return;
    
    const userMsg = { role: 'user' as const, content: query };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/platform/chat`, { 
        query: query,
        dataset_name: selectedDataset
      });
      
      const assistantMsg = { role: 'assistant' as const, content: res.data.data.response };
      setMessages(prev => [...prev, assistantMsg]);
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error communicating with the Ollama model cluster." }]);
    } finally {
      setIsTyping(false);
    }
  };

  const suggestedPrompts = [
    "What are the top correlations in this dataset?",
    "Which feature is the strongest predictor for the target?",
    "Summarize the SHAP business drivers.",
    "Recommend 3 actionable business strategies."
  ];

  return (
    <div className="h-[calc(100vh-100px)] flex flex-col font-sans pb-4 max-w-7xl mx-auto px-4 md:px-8 space-y-6">
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-[#E7EAF2] pb-4 shrink-0">
        <div className="flex items-center">
          <div className="w-10 h-10 rounded-xl bg-white border border-[#E7EAF2] flex items-center justify-center mr-4 shadow-sm text-[#5B5CEB]">
            <BrainCircuit className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold tracking-tight text-[#111827]">Agentix AI Assistant</h1>
            <p className="text-[#6B7280] text-xs mt-0.5 flex items-center font-medium">
              Llama-3 LLM Cluster <span className="mx-2">•</span> <CheckCircle2 className="w-3 h-3 text-[#16A34A] mr-1" /> Dataset Aware
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-3 bg-white border border-[#E7EAF2] rounded-xl px-3 py-1.5 shadow-sm">
          <Database className="w-4 h-4 text-[#5B5CEB]" />
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
      </div>

      {/* Chat Area */}
      <div className="flex-1 bg-white border border-[#E7EAF2] rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.005)] flex flex-col overflow-hidden relative">
        
        {messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center p-8 text-center bg-[#F8F9FC]">
            <div className="w-14 h-14 bg-white rounded-2xl shadow-sm border border-[#E7EAF2] flex items-center justify-center mb-6 text-[#5B5CEB]">
              <BrainCircuit className="w-6 h-6 animate-pulse" />
            </div>
            <h2 className="text-xl font-bold text-[#111827] mb-2">Data Science Copilot</h2>
            <p className="text-[#6B7280] text-xs font-medium max-w-sm mb-8 leading-relaxed">
              Query metrics, inspect model features, or request mathematical drivers. I have access to your active workspace variables.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl w-full">
              {suggestedPrompts.map((prompt, idx) => (
                <button 
                  key={idx}
                  onClick={() => handleSend(prompt)}
                  className="p-4 bg-white border border-[#E7EAF2] rounded-xl hover:border-[#5B5CEB]/40 hover:shadow-sm transition-all text-left flex flex-col group cursor-pointer"
                >
                  <MessageSquare className="w-4 h-4 text-[#9CA3AF] mb-2 group-hover:text-[#5B5CEB] transition-colors" />
                  <span className="text-xs font-bold text-[#4B5563] group-hover:text-[#111827] transition-colors">{prompt}</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar bg-[#F8F9FC]">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                
                <div className={`flex max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  
                  {/* Avatar */}
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
                    msg.role === 'user' ? 'bg-[#111827] ml-3' : 'bg-white border border-[#E7EAF2] mr-3 shadow-sm text-[#5B5CEB]'
                  }`}>
                    {msg.role === 'user' ? (
                      <User className="w-4 h-4 text-white" />
                    ) : (
                      <BrainCircuit className="w-4 h-4" />
                    )}
                  </div>
                  
                  {/* Bubble */}
                  <div className={`px-4 py-3 rounded-2xl text-xs leading-relaxed ${
                    msg.role === 'user' 
                      ? 'bg-[#5B5CEB] text-white font-medium shadow-sm' 
                      : 'bg-white border border-[#E7EAF2] shadow-[0_4px_20px_rgba(0,0,0,0.01)] text-[#374151]'
                  }`}>
                    {msg.role === 'user' ? (
                      msg.content
                    ) : (
                      <div className="prose prose-sm max-w-none prose-p:leading-relaxed prose-pre:bg-[#111827] prose-pre:text-white prose-th:bg-[#F8F9FC] text-xs font-medium">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {msg.content}
                        </ReactMarkdown>
                      </div>
                    )}
                  </div>

                </div>

              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="flex max-w-[80%] flex-row">
                  <div className="w-8 h-8 rounded-full bg-white border border-[#E7EAF2] flex items-center justify-center mr-3 shrink-0 shadow-sm text-[#5B5CEB]">
                    <BrainCircuit className="w-4 h-4" />
                  </div>
                  <div className="px-4 py-3 rounded-2xl bg-white border border-[#E7EAF2] shadow-sm flex items-center space-x-1 h-8">
                    <span className="w-1.5 h-1.5 bg-[#5B5CEB] rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-1.5 h-1.5 bg-[#5B5CEB] rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-1.5 h-1.5 bg-[#5B5CEB] rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}

        {/* Input Bar */}
        <div className="p-4 bg-white border-t border-[#E7EAF2]">
          <div className="max-w-4xl mx-auto relative flex items-end bg-[#F8F9FC] border border-[#E7EAF2] rounded-2xl overflow-hidden focus-within:border-[#5B5CEB] focus-within:ring-1 focus-within:ring-[#5B5CEB] transition-all">
            <button className="p-3 text-[#9CA3AF] hover:text-[#111827] transition-colors shrink-0 cursor-pointer">
              <Plus className="w-4 h-4" />
            </button>
            <textarea 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend(input);
                }
              }}
              placeholder="Query dataset insights..."
              className="flex-1 bg-transparent border-0 focus:ring-0 resize-none py-3 px-2 text-xs font-semibold text-[#111827] max-h-32 min-h-[46px] outline-none"
              rows={1}
            />
            <button 
              onClick={() => handleSend(input)}
              disabled={!input.trim() || isTyping}
              className={`p-2.5 m-1 rounded-xl shrink-0 transition-all cursor-pointer ${
                input.trim() && !isTyping ? 'bg-[#5B5CEB] text-white hover:bg-[#4E4FD6]' : 'bg-[#E7EAF2] text-[#9CA3AF] opacity-50'
              }`}
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
          <p className="text-center text-[9px] text-[#9CA3AF] mt-2 font-semibold tracking-wide uppercase">
            Agentix AI calculations should be cross-verified for model deployments.
          </p>
        </div>

      </div>
    </div>
  );
}
