"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { StatusBadge } from "@/components/ui/design-system";
import { motion, AnimatePresence } from "framer-motion";
import { 
  ArrowRight, Shield, Layers, Workflow, FileText, Database,
  Play, CheckCircle2, Cpu, LineChart, Bot, Sparkles, Activity,
  ChevronDown, Server
} from "lucide-react";

export default function LandingPage() {
  const [scrolled, setScrolled] = useState(false);
  const [activePreview, setActivePreview] = useState("dashboard");
  const [activeFaq, setActiveFaq] = useState<number | null>(null);
  
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Monitor scroll for glassmorphic navbar styling
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // HTML5 Canvas dynamic particle network graph animation representing pipelines
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    const particles: any[] = [];
    const maxParticles = 50;

    let canvasWidth = canvas.width;
    let canvasHeight = canvas.height;

    const resizeCanvas = () => {
      if (canvas && canvas.parentElement) {
        canvas.width = canvas.parentElement.clientWidth || window.innerWidth;
        canvas.height = canvas.parentElement.clientHeight || 650;
        canvasWidth = canvas.width;
        canvasHeight = canvas.height;
      }
    };
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    class Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      radius: number;

      constructor() {
        this.x = Math.random() * canvasWidth;
        this.y = Math.random() * canvasHeight;
        this.vx = (Math.random() - 0.5) * 0.7;
        this.vy = (Math.random() - 0.5) * 0.7;
        this.radius = Math.random() * 2 + 1;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvasWidth) this.vx *= -1;
        if (this.y < 0 || this.y > canvasHeight) this.vy *= -1;
      }

      draw() {
        ctx!.beginPath();
        ctx!.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx!.fillStyle = 'rgba(91, 92, 235, 0.4)';
        ctx!.fill();
      }
    }

    for (let i = 0; i < maxParticles; i++) {
      particles.push(new Particle());
    }

    const drawLines = () => {
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 130) {
            ctx!.beginPath();
            ctx!.moveTo(particles[i].x, particles[i].y);
            ctx!.lineTo(particles[j].x, particles[j].y);
            ctx!.strokeStyle = `rgba(91, 92, 235, ${0.15 * (1 - dist / 130)})`;
            ctx!.lineWidth = 0.8;
            ctx!.stroke();
          }
        }
      }
    };

    const render = () => {
      ctx!.clearRect(0, 0, canvas.width, canvas.height);
      
      particles.forEach(p => {
        p.update();
        p.draw();
      });
      
      drawLines();
      animationFrameId = requestAnimationFrame(render);
    };
    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', resizeCanvas);
    };
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1, 
      transition: { staggerChildren: 0.12, delayChildren: 0.1 } 
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0, 
      transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] as const } 
    },
  };

  const featureCards = [
    {
      title: "Data Cleaning",
      description: "Instantly sweep variables. Auto-detect datatypes, resolve null occurrences, and filter outliers through standard criteria.",
      icon: <Layers className="w-5 h-5 text-[#5B5CEB]" />
    },
    {
      title: "AutoML Suite",
      description: "Train regressions and classification pipelines concurrently. Track hyperparameters inside a unified candidate leaderboard.",
      icon: <Cpu className="w-5 h-5 text-[#7C4DFF]" />
    },
    {
      title: "SHAP Explainability",
      description: "Demystify black-box choices. Map local feature waterfalls and global parameter importances with proof.",
      icon: <LineChart className="w-5 h-5 text-[#16A34A]" />
    },
    {
      title: "AI Analyst Copilot",
      description: "Conversational terminal to inspect tables, write Python, or query diagnostic outcomes in plain English.",
      icon: <Bot className="w-5 h-5 text-[#F59E0B]" />
    },
    {
      title: "Orchestration DAG",
      description: "Visualize execution timelines and task nodes communicating autonomously through a Directed Acyclic Graph.",
      icon: <Workflow className="w-5 h-5 text-[#EF4444]" />
    },
    {
      title: "Insights Reports",
      description: "Compile statistical matrices, drift charts, and training logs into corporate-ready PDF and PowerPoint documents.",
      icon: <FileText className="w-5 h-5 text-[#5B5CEB]" />
    }
  ];

  const steps = [
    { phase: "Ingestion", desc: "Drag CSV/Excel spreadsheets into local memory workspace." },
    { phase: "Cleaning", desc: "AI scans schemas, resolving datatype distributions." },
    { phase: "Advanced EDA", desc: "Plot histograms and linear correlation heatmaps." },
    { phase: "AutoML", desc: "Hyperparameter sweep to rank accuracy R² leaderboards." },
    { phase: "SHAP Explain", desc: "Local waterfall graphs mapping predictive drivers." },
    { phase: "Export", desc: "Compile briefings and download corporate reports." }
  ];

  const faqs = [
    {
      q: "How does the AutoML sweep work?",
      a: "The AutoML engine evaluates multiple regressions or classification models concurrently (Ridge, Random Forest, XGBoost, LightGBM) using local K-Fold cross-validation, hyperparameter tuning, and lists them on a ranked leaderboard."
    },
    {
      q: "Does my data leave the server?",
      a: "No. Agentix is built with a zero-egress architecture. Your raw dataset stays locked inside your PostgreSQL database workspace, and chatbot queries interact directly with localized LLM clusters."
    },
    {
      q: "What local LLMs are supported?",
      a: "The platform integrates with localized Ollama model registries running Llama-3 regressive and feature extraction weights for private, server-side execution."
    },
    {
      q: "Can I customize the generated reports?",
      a: "Yes. The AI Analyst can compile PDF, Word, or PowerPoint presentation decks with custom scopes (Executive or Technical summaries) containing exact correlation heatmaps and SHAP coefficients."
    }
  ];

  return (
    <main className="relative min-h-screen bg-[#F8F9FC] text-[#111827] overflow-x-hidden font-sans select-none">
      
      {/* Canvas background for animated graphs & particles */}
      <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden h-[700px]">
        <canvas ref={canvasRef} className="w-full h-full opacity-70" />
        <div className="absolute top-0 right-0 -mt-40 -mr-40 w-[500px] h-[500px] bg-[#5B5CEB]/5 rounded-full mix-blend-multiply filter blur-[120px] pointer-events-none"></div>
        <div className="absolute bottom-10 left-0 -mb-40 -ml-40 w-[500px] h-[500px] bg-[#7C4DFF]/5 rounded-full mix-blend-multiply filter blur-[120px] pointer-events-none"></div>
      </div>

      {/* Sticky Glassmorphic Navbar */}
      <nav 
        className="fixed top-0 left-0 right-0 w-full z-50 transition-all duration-300 border-b flex items-center justify-between px-6 md:px-12"
        style={{
          height: '72px',
          backgroundColor: scrolled ? 'rgba(255, 255, 255, 0.85)' : 'transparent',
          borderColor: scrolled ? '#E7EAF2' : 'transparent',
          backdropFilter: scrolled ? 'blur(16px)' : 'none',
        }}
      >
        <div className="flex items-center space-x-3 shrink-0">
          <div className="w-8 h-8 rounded-xl bg-[#5B5CEB] flex items-center justify-center shadow-sm text-white">
            <Workflow className="w-4 h-4" />
          </div>
          <span className="text-base font-extrabold tracking-tight text-[#111827]">
            Agentix
          </span>
        </div>

        <div className="hidden md:flex items-center space-x-8 text-xs font-bold uppercase tracking-wider text-[#6B7280]">
          <a href="#features" className="hover:text-[#5B5CEB] transition-colors">Features</a>
          <a href="#workflow" className="hover:text-[#5B5CEB] transition-colors">Workflow</a>
          <a href="#ai-capabilities" className="hover:text-[#5B5CEB] transition-colors">AI Engine</a>
          <a href="#faq" className="hover:text-[#5B5CEB] transition-colors">FAQ</a>
        </div>

        <div className="flex items-center space-x-4 shrink-0">
          <Link href="/login">
            <span className="text-xs font-bold uppercase tracking-wider text-[#6B7280] hover:text-[#111827] cursor-pointer transition-colors px-3 py-2">
              Login
            </span>
          </Link>
          <Link href="/dashboard">
            <button className="px-5 py-2.5 bg-[#5B5CEB] hover:bg-[#4E4FD6] active:scale-98 text-white rounded-xl text-xs font-bold transition-all shadow-md cursor-pointer">
              Get Started
            </button>
          </Link>
        </div>
      </nav>

      {/* Spacer for sticky nav */}
      <div className="h-[72px] w-full"></div>

      {/* 1. Hero Section */}
      <section className="w-full max-w-7xl mx-auto px-6 md:px-12 pt-16 pb-28 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center min-h-[calc(100vh-72px)] relative z-10">
        
        {/* Info */}
        <motion.div 
          initial="hidden" 
          animate="visible" 
          variants={containerVariants} 
          className="flex flex-col items-start text-left space-y-8"
        >
          <motion.div 
            variants={itemVariants} 
            className="flex items-center space-x-2 rounded-full border border-[#E7EAF2] bg-white px-4 py-1.5 text-[10px] font-bold uppercase tracking-wider text-[#5B5CEB] shadow-sm"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Agentix Enterprise v2.1</span>
          </motion.div>

          <motion.div variants={itemVariants} className="space-y-4">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-[#111827] leading-[1.15]">
              Your AI Data Science <br />
              <span className="text-[#5B5CEB] bg-gradient-to-r from-[#5B5CEB] to-[#7C4DFF] bg-clip-text text-transparent">Operating System.</span>
            </h1>
            <p className="text-sm md:text-base text-[#6B7280] font-medium max-w-lg leading-relaxed mt-3">
              Automate data ingestion, run complex Auto-ML leaderboard trials, map localized SHAP waterfall parameters, and compile boardroom-ready executive PDF reports with offline agent swarms.
            </p>
          </motion.div>

          <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-3 pt-2 w-full sm:w-auto">
            <Link href="/dashboard">
              <button className="h-12 inline-flex items-center justify-center rounded-xl bg-[#5B5CEB] hover:bg-[#4E4FD6] px-8 text-xs font-bold text-white transition-all shadow-md active:scale-95 cursor-pointer min-w-[150px]">
                Start Free
                <ArrowRight className="ml-2 h-4 w-4" />
              </button>
            </Link>
            <a href="#preview">
              <button className="h-12 inline-flex items-center justify-center rounded-xl bg-white border border-[#E7EAF2] hover:bg-[#F8F9FC] px-8 text-xs font-bold text-[#111827] transition-all shadow-sm active:scale-95 cursor-pointer min-w-[150px]">
                <Play className="mr-2 h-3.5 w-3.5 fill-[#111827]" />
                View Demo
              </button>
            </a>
          </motion.div>
        </motion.div>

        {/* Network pipeline representation DAG SVG */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7, ease: "easeOut" }}
          className="relative w-full h-[400px] lg:h-[480px] bg-white border border-[#E7EAF2] rounded-[24px] shadow-sm flex items-center justify-center overflow-hidden"
        >
          <div className="absolute inset-0" style={{ backgroundImage: 'radial-gradient(#E7EAF2 1px, transparent 1px)', backgroundSize: '32px 32px' }}></div>
          
          <svg className="absolute w-full h-full p-8" viewBox="0 0 600 450" fill="none" xmlns="http://www.w3.org/2000/svg">
            <motion.line x1="120" y1="225" x2="280" y2="125" stroke="#E7EAF2" strokeWidth="1.5" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1 }} />
            <motion.line x1="120" y1="225" x2="280" y2="325" stroke="#E7EAF2" strokeWidth="1.5" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1 }} />
            <motion.line x1="280" y1="125" x2="480" y2="225" stroke="#E7EAF2" strokeWidth="1.5" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1 }} />
            <motion.line x1="280" y1="325" x2="480" y2="225" stroke="#E7EAF2" strokeWidth="1.5" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 1 }} />
            
            <motion.line x1="120" y1="225" x2="280" y2="125" stroke="#5B5CEB" strokeWidth="1.5" strokeDasharray="6 6" animate={{ strokeDashoffset: [-60, 0] }} transition={{ repeat: Infinity, duration: 2.5, ease: "linear" }} />
            <motion.line x1="280" y1="325" x2="480" y2="225" stroke="#16A34A" strokeWidth="1.5" strokeDasharray="6 6" animate={{ strokeDashoffset: [-60, 0] }} transition={{ repeat: Infinity, duration: 2.5, ease: "linear" }} />
            
            <g>
              <circle cx="120" cy="225" r="28" fill="white" stroke="#E7EAF2" strokeWidth="1.5" />
              <Database className="w-5 h-5 text-[#5B5CEB]" x="110" y="215" />
            </g>
            <g>
              <circle cx="280" cy="125" r="32" fill="white" stroke="#5B5CEB" strokeWidth="1.5" />
              <Cpu className="w-5 h-5 text-[#5B5CEB]" x="270" y="115" />
            </g>
            <g>
              <circle cx="280" cy="325" r="32" fill="white" stroke="#7C4DFF" strokeWidth="1.5" />
              <LineChart className="w-5 h-5 text-[#7C4DFF]" x="270" y="315" />
            </g>
            <g>
              <circle cx="480" cy="225" r="30" fill="white" stroke="#16A34A" strokeWidth="1.5" />
              <Bot className="w-5 h-5 text-[#16A34A]" x="470" y="215" />
            </g>
          </svg>

          {/* Floating diagnostic nodes */}
          <div className="absolute top-8 left-8 p-3.5 bg-white/95 backdrop-blur-md rounded-xl border border-[#E7EAF2] shadow-sm flex items-center space-x-2.5">
            <Activity className="w-4 h-4 text-[#16A34A] animate-pulse" />
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#111827]">AutoML Model Sweep active</span>
          </div>

          <div className="absolute bottom-8 right-8 p-3.5 bg-white/95 backdrop-blur-md rounded-xl border border-[#E7EAF2] shadow-sm flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-[#5B5CEB] animate-ping" />
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#6B7280]">Workspace local registry sync</span>
          </div>
        </motion.div>

      </section>

      {/* 2. Features Grid Section */}
      <section id="features" className="w-full bg-white border-y border-[#E7EAF2] py-28 relative">
        <div className="max-w-7xl mx-auto px-6 md:px-12">
          
          <div className="max-w-xl text-left mb-16 space-y-3">
            <h2 className="text-[10px] font-bold text-[#5B5CEB] uppercase tracking-widest">Platform Modules</h2>
            <h3 className="text-3xl font-extrabold text-[#111827] tracking-tight">
              Enterprise Data Science Capabilities
            </h3>
            <p className="text-xs md:text-sm font-semibold text-[#6B7280] leading-relaxed">
              Every stage of your machine learning workflow is enhanced by specialized AI pipelines and analytics.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featureCards.map((f, i) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, y: 15 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: i * 0.08 }}
                className="p-6 md:p-8 rounded-2xl bg-[#F8F9FC] border border-[#E7EAF2] flex flex-col items-start hover:border-[#5B5CEB]/30 hover:bg-white hover:shadow-md transition-all duration-200"
              >
                <div className="w-10 h-10 rounded-xl bg-white border border-[#E7EAF2] flex items-center justify-center shadow-sm mb-5 text-[#5B5CEB]">
                  {f.icon}
                </div>
                <h4 className="text-sm font-bold text-[#111827] mb-2">{f.title}</h4>
                <p className="text-xs text-[#6B7280] leading-relaxed font-semibold">{f.description}</p>
              </motion.div>
            ))}
          </div>

        </div>
      </section>

      {/* 3. Workflow journey section */}
      <section id="workflow" className="w-full py-28 max-w-7xl mx-auto px-6 md:px-12">
        <div className="text-center mb-16 space-y-3">
          <h2 className="text-[10px] font-bold text-[#7C4DFF] uppercase tracking-widest">Execution Timeline</h2>
          <h3 className="text-3xl font-extrabold text-[#111827] tracking-tight">The Data Ingestion to Report Workflow</h3>
          <p className="text-xs md:text-sm font-semibold text-[#6B7280] max-w-md mx-auto">Transforming raw spreadsheets into explainable machine learning predictions in six modular steps.</p>
        </div>

        {/* Step Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4">
          {steps.map((s, idx) => (
            <motion.div 
              key={idx}
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.3, delay: idx * 0.05 }}
              className="p-5 bg-white border border-[#E7EAF2] rounded-2xl shadow-sm flex flex-col items-start space-y-3 hover:border-[#5B5CEB]/30 transition-all cursor-default"
            >
              <div className="w-7 h-7 rounded-lg bg-[#5B5CEB]/10 flex items-center justify-center text-xs font-extrabold text-[#5B5CEB]">
                {idx + 1}
              </div>
              <h4 className="text-xs font-bold text-[#111827]">{s.phase}</h4>
              <p className="text-[10px] text-[#6B7280] font-semibold leading-relaxed">{s.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* 4. AI Capabilities Split Section */}
      <section id="ai-capabilities" className="w-full bg-white border-y border-[#E7EAF2] py-28">
        <div className="max-w-7xl mx-auto px-6 md:px-12 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          
          <div className="space-y-6">
            <h2 className="text-[10px] font-bold text-[#16A34A] uppercase tracking-widest">AI Agent Swarm</h2>
            <h3 className="text-3xl font-extrabold text-[#111827] tracking-tight leading-tight">
              Direct Collaborative Conversations With Your Data
            </h3>
            <p className="text-xs md:text-sm font-semibold text-[#6B7280] leading-relaxed">
              Agentix models run offline on localized execution clusters. Chat directly to request missing value counts, trigger AutoML leaderboards, or query explainability models in English.
            </p>
            
            <div className="space-y-3 pt-2">
              <div className="flex items-center space-x-3 text-xs font-bold text-[#111827]">
                <CheckCircle2 className="w-4 h-4 text-[#16A34A] shrink-0" />
                <span>Zero Data Egress. Query secure offline local LLMs.</span>
              </div>
              <div className="flex items-center space-x-3 text-xs font-bold text-[#111827]">
                <CheckCircle2 className="w-4 h-4 text-[#16A34A] shrink-0" />
                <span>In-Context Model Awareness. Agents scan schema statistics.</span>
              </div>
              <div className="flex items-center space-x-3 text-xs font-bold text-[#111827]">
                <CheckCircle2 className="w-4 h-4 text-[#16A34A] shrink-0" />
                <span>One-Click code conversions and statistical interpretations.</span>
              </div>
            </div>
          </div>

          {/* Interactive Chat Console mock */}
          <div className="bg-[#111827] border border-[#1F2937] rounded-3xl p-5 shadow-xl text-slate-300 font-mono text-[10px] leading-relaxed select-text">
            <div className="flex items-center justify-between border-b border-[#1F2937] pb-3 mb-4 text-[#9CA3AF]">
              <div className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-[#EF4444]/70" />
                <span className="w-2.5 h-2.5 rounded-full bg-[#F59E0B]/70" />
                <span className="w-2.5 h-2.5 rounded-full bg-[#16A34A]/70" />
              </div>
              <span className="text-[9px] uppercase font-bold tracking-wider">Agentix LLM Console</span>
              <span className="text-[#6B7280]">v2.1</span>
            </div>

            <div className="space-y-4">
              <div>
                <span className="text-[#5B5CEB] font-bold">visitor@agentix:~$</span> query --dataset customer_churn --shap
              </div>
              <div className="text-slate-400">
                Parsing SHAP Game-Theoretic matrices for model: XGBoost_Classifier_v1.0...
              </div>
              <div className="p-3 bg-white/5 border border-white/5 rounded-xl text-slate-300 space-y-2">
                <p className="text-[#16A34A] font-bold">{'[AI Analyst explainer]'}</p>
                <p>The prediction probability is pushed up +15.4% by "Contract_Month-to-Month" indicating it is the dominant churn predictor. "Tenure" acts as the strongest negative offset contributing -8.5% to the base value calculation.</p>
              </div>
              <div className="flex items-center space-x-1 text-[#5B5CEB]">
                <span className="font-bold">visitor@agentix:~$</span>
                <span className="w-1.5 h-3.5 bg-[#5B5CEB] animate-pulse" />
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* 5. Interactive Screenshots Laptop view */}
      <section id="preview" className="w-full bg-[#111827] py-28 text-white border-t border-[#111827]">
        <div className="max-w-7xl mx-auto px-6 md:px-12 flex flex-col items-center">
          
          <div className="text-center max-w-xl mb-12 space-y-3">
            <h2 className="text-[10px] font-bold text-[#5B5CEB] uppercase tracking-widest">Interface Preview</h2>
            <h3 className="text-3xl font-extrabold text-white tracking-tight">Interactive Workspace Panels</h3>
            <p className="text-xs text-slate-400 font-semibold">Toggle tabs below to preview actual dashboards built inside the Agentix platform.</p>
            
            {/* Gallery Slide Toggles */}
            <div className="flex flex-wrap justify-center gap-2 pt-6">
              {[
                { id: "dashboard", label: "Executive Dashboard" },
                { id: "eda", label: "Correlation Heatmaps" },
                { id: "automl", label: "AutoML Leaderboards" },
                { id: "explainability", label: "Explainability SHAP" }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActivePreview(tab.id)}
                  className={`px-3 py-1.5 rounded-xl text-[10px] font-bold uppercase tracking-wider transition-all cursor-pointer border ${
                    activePreview === tab.id 
                      ? 'bg-[#5B5CEB] border-[#5B5CEB] text-white shadow-md' 
                      : 'bg-white/5 hover:bg-white/10 border-white/5 text-slate-400'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Premium MacBook mockup frame */}
          <div className="w-full max-w-4xl bg-[#1E1E24] rounded-[24px] p-3 md:p-4 border border-white/10 shadow-[0_25px_60px_rgba(0,0,0,0.5)] overflow-hidden">
            <div className="bg-[#111827] rounded-[16px] aspect-video border border-white/10 overflow-hidden relative flex flex-col">
              
              {/* Window Header */}
              <div className="h-9 bg-[#1E1E24]/60 border-b border-white/5 flex items-center px-4 justify-between select-none">
                <div className="flex space-x-1.5 shrink-0">
                  <div className="w-2.5 h-2.5 rounded-full bg-[#EF4444]/60" />
                  <div className="w-2.5 h-2.5 rounded-full bg-[#F59E0B]/60" />
                  <div className="w-2.5 h-2.5 rounded-full bg-[#16A34A]/60" />
                </div>
                <div className="text-[9px] text-white/40 font-mono truncate max-w-xs">http://localhost:3000/{activePreview}</div>
                <div className="w-10 shrink-0" />
              </div>

              {/* Dynamic View Mock */}
              <div className="flex-1 p-5 overflow-y-auto text-left scrollbar-hide text-xs">
                <AnimatePresence mode="wait">
                  {activePreview === "dashboard" && (
                    <motion.div 
                      key="dashboard"
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -8 }}
                      className="space-y-4"
                    >
                      <div className="flex justify-between items-center pb-3 border-b border-white/10">
                        <div>
                          <h4 className="text-base font-bold text-white">Platform Health Overview</h4>
                          <p className="text-[10px] text-slate-400">Workspace data pipeline indicators</p>
                        </div>
                        <StatusBadge status="Optimal state" type="success" />
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div className="p-3 bg-white/5 rounded-xl border border-white/5">
                          <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider">Active Columns</span>
                          <p className="text-xl font-mono font-bold mt-1 text-white">42</p>
                        </div>
                        <div className="p-3 bg-white/5 rounded-xl border border-white/5">
                          <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider">Model accuracy</span>
                          <p className="text-xl font-mono font-bold mt-1 text-[#5B5CEB]">94.25%</p>
                        </div>
                        <div className="p-3 bg-white/5 rounded-xl border border-white/5">
                          <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider">Concept Drift</span>
                          <p className="text-xl font-mono font-bold mt-1 text-[#16A34A]">Stable</p>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {activePreview === "eda" && (
                    <motion.div 
                      key="eda"
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -8 }}
                      className="space-y-4"
                    >
                      <h4 className="text-base font-bold text-white border-b border-white/10 pb-2">Correlation Matrix</h4>
                      <div className="grid grid-cols-3 gap-2 font-mono text-[9px] text-center">
                        <div className="bg-white/5 p-2 rounded">Variables</div>
                        <div className="bg-white/5 p-2 rounded text-slate-400">Income</div>
                        <div className="bg-white/5 p-2 rounded text-slate-400">Churn</div>
                        
                        <div className="bg-white/5 p-2 rounded text-slate-400 text-left">Income</div>
                        <div className="bg-[#16A34A]/80 p-2 rounded text-white font-bold">1.00</div>
                        <div className="bg-[#EF4444]/60 p-2 rounded text-white font-bold">-0.42</div>

                        <div className="bg-white/5 p-2 rounded text-slate-400 text-left">Churn</div>
                        <div className="bg-[#EF4444]/60 p-2 rounded text-white font-bold">-0.42</div>
                        <div className="bg-[#16A34A]/80 p-2 rounded text-white font-bold">1.00</div>
                      </div>
                    </motion.div>
                  )}

                  {activePreview === "automl" && (
                    <motion.div 
                      key="automl"
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -8 }}
                      className="space-y-4"
                    >
                      <h4 className="text-base font-bold text-white border-b border-white/10 pb-2">AutoML regressors leaderboard</h4>
                      <div className="border border-white/5 rounded-xl overflow-hidden">
                        <table className="w-full text-left border-collapse text-[10px]">
                          <thead>
                            <tr className="bg-white/5 border-b border-white/10 font-bold text-slate-300">
                              <th className="p-2.5">Rank</th>
                              <th className="p-2.5">Candidate Model</th>
                              <th className="p-2.5">R² Score</th>
                              <th className="p-2.5">RMSE</th>
                            </tr>
                          </thead>
                          <tbody className="text-slate-300">
                            <tr className="border-b border-white/5 bg-[#16A34A]/5">
                              <td className="p-2.5 font-bold text-amber-400">#1</td>
                              <td className="p-2.5 font-bold text-white">XGBoost Regressor</td>
                              <td className="p-2.5 font-bold text-[#16A34A]">0.954</td>
                              <td className="p-2.5">0.034</td>
                            </tr>
                            <tr className="border-b border-white/5">
                              <td className="p-2.5">#2</td>
                              <td className="p-2.5">Random Forest</td>
                              <td className="p-2.5 text-white">0.932</td>
                              <td className="p-2.5">0.045</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </motion.div>
                  )}

                  {activePreview === "explainability" && (
                    <motion.div 
                      key="explainability"
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -8 }}
                      className="space-y-4"
                    >
                      <h4 className="text-base font-bold text-white border-b border-white/10 pb-2">Local SHAP Waterfall</h4>
                      <div className="space-y-3 font-mono text-[9px]">
                        <div className="flex justify-between items-center">
                          <span className="w-20 text-right pr-2 text-slate-400">Income</span>
                          <div className="flex-1 bg-white/5 rounded h-4 overflow-hidden relative">
                            <div className="bg-[#5B5CEB] absolute left-1/2 w-[35%] h-full rounded" />
                          </div>
                          <span className="w-12 text-right font-bold text-[#5B5CEB] ml-2">+0.35</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="w-20 text-right pr-2 text-slate-400">Tenure</span>
                          <div className="flex-1 bg-white/5 rounded h-4 overflow-hidden relative">
                            <div className="bg-[#16A34A] absolute right-1/2 w-[22%] h-full rounded" />
                          </div>
                          <span className="w-12 text-right font-bold text-[#16A34A] ml-2">-0.22</span>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

            </div>
          </div>

        </div>
      </section>

      {/* 6. Why Agentix Marketing Info */}
      <section className="w-full py-28 max-w-7xl mx-auto px-6 md:px-12 relative z-10 text-left">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 items-start">
          
          <div className="space-y-4">
            <h2 className="text-[10px] font-bold text-[#5B5CEB] uppercase tracking-widest">Why Agentix</h2>
            <h3 className="text-3xl font-extrabold text-[#111827] tracking-tight leading-tight">
              An Operations Hub For Machine Learning
            </h3>
            <p className="text-xs font-semibold text-[#6B7280] leading-relaxed">
              We bridge the gap between black-box calculations and business analytics stakeholders.
            </p>
          </div>

          <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card hover={true}>
              <h4 className="text-sm font-bold text-[#111827] mb-2 flex items-center">
                <Shield className="w-4 h-4 mr-2 text-[#5B5CEB]" /> Game-Theoretic SHAP Validation
              </h4>
              <p className="text-xs text-[#6B7280] font-semibold leading-relaxed">
                Move away from opaque guesswork. Know exactly which metrics and variables push models to make churn, price, or risk choices.
              </p>
            </Card>

            <Card hover={true}>
              <h4 className="text-sm font-bold text-[#111827] mb-2 flex items-center">
                <Server className="w-4 h-4 mr-2 text-[#16A34A]" /> Zero Egress Offline Inference
              </h4>
              <p className="text-xs text-[#6B7280] font-semibold leading-relaxed">
                Connect localized Ollama model registries to keep parameters entirely host-level. No third-party API dependencies.
              </p>
            </Card>

            <Card hover={true}>
              <h4 className="text-sm font-bold text-[#111827] mb-2 flex items-center">
                <Activity className="w-4 h-4 mr-2 text-[#F59E0B]" /> Continuous Drift Auditing
              </h4>
              <p className="text-xs text-[#6B7280] font-semibold leading-relaxed">
                Monitor live endpoints and calculate concept drift. Trigger alarm webhooks if data integrity drops below optimal validation bounds.
              </p>
            </Card>

            <Card hover={true}>
              <h4 className="text-sm font-bold text-[#111827] mb-2 flex items-center">
                <Workflow className="w-4 h-4 mr-2 text-[#EF4444]" /> LangGraph Swarms
              </h4>
              <p className="text-xs text-[#6B7280] font-semibold leading-relaxed">
                Orchestrate cleaning, training, and documentation reports steps asynchronously through native autonomous workflows.
              </p>
            </Card>
          </div>

        </div>
      </section>

      {/* 7. FAQ Section */}
      <section id="faq" className="w-full bg-[#F8F9FC] border-t border-[#E7EAF2] py-28 relative z-10 text-left">
        <div className="max-w-3xl mx-auto px-6">
          <div className="text-center mb-16 space-y-3">
            <h2 className="text-[10px] font-bold text-[#7C4DFF] uppercase tracking-widest">Common Questions</h2>
            <h3 className="text-3xl font-extrabold text-[#111827] tracking-tight">Frequently Asked Questions</h3>
          </div>

          <div className="space-y-4">
            {faqs.map((faq, index) => {
              const isOpen = activeFaq === index;
              return (
                <div 
                  key={index}
                  className="bg-white border border-[#E7EAF2] rounded-2xl overflow-hidden shadow-sm transition-all"
                >
                  <button
                    onClick={() => setActiveFaq(isOpen ? null : index)}
                    className="w-full px-6 py-5 flex items-center justify-between text-left cursor-pointer focus:outline-none"
                  >
                    <span className="text-xs font-bold text-[#111827]">{faq.q}</span>
                    <ChevronDown className={`w-4 h-4 text-[#9CA3AF] transition-transform duration-200 ${isOpen ? 'rotate-180 text-[#5B5CEB]' : ''}`} />
                  </button>
                  
                  <AnimatePresence initial={false}>
                    {isOpen && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        className="px-6 pb-5 text-xs text-[#6B7280] font-semibold leading-relaxed border-t border-[#F8F9FC] pt-3 bg-[#F8F9FC]/25"
                      >
                        {faq.a}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* 8. Footer Section */}
      <footer className="w-full border-t border-[#E7EAF2] bg-white pt-20 pb-8 relative z-10 text-left">
        <div className="max-w-7xl mx-auto px-6 md:px-12 grid grid-cols-1 md:grid-cols-4 gap-8 mb-16">
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="w-7 h-7 rounded-lg bg-[#5B5CEB] flex items-center justify-center text-white shadow-sm">
                <Workflow className="w-3.5 h-3.5" />
              </div>
              <span className="font-extrabold text-base text-[#111827] tracking-tight">Agentix</span>
            </div>
            <p className="text-xs text-[#6B7280] font-semibold leading-relaxed">
              Agentix is a secure, local-inference AI workspace coordinating automated data engineering, AutoML leaderboards, and SHAP decision explanations.
            </p>
          </div>
          <div>
            <h4 className="font-bold text-[10px] text-[#111827] uppercase tracking-wider mb-4">Platform</h4>
            <ul className="space-y-3 text-xs text-[#6B7280] font-semibold">
              <li><a href="#features" className="hover:text-[#5B5CEB] transition-colors">Platform Features</a></li>
              <li><a href="#workflow" className="hover:text-[#5B5CEB] transition-colors">Workflow Orchestrator</a></li>
              <li><a href="/login" className="hover:text-[#5B5CEB] transition-colors">Enterprise Login</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-[10px] text-[#111827] uppercase tracking-wider mb-4">Inference Resources</h4>
            <ul className="space-y-3 text-xs text-[#6B7280] font-semibold">
              <li><a href="#" className="hover:text-[#5B5CEB] transition-colors">Ollama Model Guide</a></li>
              <li><a href="#" className="hover:text-[#5B5CEB] transition-colors">FastAPI Router specs</a></li>
              <li><a href="#" className="hover:text-[#5B5CEB] transition-colors">PostgreSQL schemas</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-[10px] text-[#111827] uppercase tracking-wider mb-4">Company Details</h4>
            <ul className="space-y-3 text-xs text-[#6B7280] font-semibold">
              <li><a href="#" className="hover:text-[#5B5CEB] transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-[#5B5CEB] transition-colors">Terms of Service</a></li>
              <li><a href="#" className="hover:text-[#5B5CEB] transition-colors">Security Overview</a></li>
            </ul>
          </div>
        </div>
        
        <div className="max-w-7xl mx-auto px-6 md:px-12 border-t border-[#E7EAF2] pt-8 flex flex-col md:flex-row justify-between items-center text-[10px] text-[#9CA3AF] font-bold uppercase tracking-wider">
          <p>© 2026 Agentix. All rights reserved.</p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <a href="#" className="hover:text-[#6B7280] transition-colors">Privacy</a>
            <a href="#" className="hover:text-[#6B7280] transition-colors">Terms</a>
          </div>
        </div>
      </footer>

    </main>
  );
}

// Simple Card wrapper to keep JSX clean and standardized
function Card({ children, hover = false }: { children: React.ReactNode; hover?: boolean }) {
  return (
    <div className={`p-6 bg-white border border-[#E7EAF2] rounded-2xl shadow-[0_4px_20px_rgba(0,0,0,0.002)] transition-all duration-200 ${
      hover ? 'hover:-translate-y-1 hover:shadow-md hover:border-[#5B5CEB]/30' : ''
    }`}>
      {children}
    </div>
  );
}