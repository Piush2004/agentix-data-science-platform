"use client";

import { Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import { Lock, ShieldCheck, BrainCircuit } from "lucide-react";

function LoginModal() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") || "/dashboard";

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-[#F6F7FB] relative overflow-hidden font-sans text-[#111827]">
      {/* Subtle Grid Background */}
      <div className="absolute inset-0 z-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(#111827 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}></div>
      
      {/* Background SVG Decoration */}
      <div className="absolute top-0 right-0 -mt-32 -mr-32 w-96 h-96 bg-[#5B5CEB] rounded-full mix-blend-multiply filter blur-[120px] opacity-10"></div>
      <div className="absolute bottom-0 left-0 -mb-32 -ml-32 w-96 h-96 bg-[#7C4DFF] rounded-full mix-blend-multiply filter blur-[120px] opacity-10"></div>
 
      <motion.div 
        initial={{ opacity: 0, scale: 0.95, y: 15 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="relative z-10 w-full max-w-md p-10 bg-white border border-[#E7EAF2] rounded-[24px] shadow-[0_8px_40px_rgba(0,0,0,0.02)]"
      >
        <div className="flex flex-col items-center text-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-[#5B5CEB] flex items-center justify-center mb-5 shadow-sm">
            <BrainCircuit className="w-6 h-6 text-white" />
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-[#111827]">Welcome to Agentix</h2>
          <p className="text-[#6B7280] text-sm mt-2 font-medium">Log in to continue to your workspace</p>
        </div>

        <div className="space-y-4">
          <button 
            onClick={() => router.push(callbackUrl)}
            className="w-full flex items-center justify-center space-x-3 bg-white hover:bg-[#F6F7FB] border border-[#E7EAF2] text-[#111827] active:scale-98 transition-all py-3.5 px-4 rounded-xl text-sm font-semibold shadow-sm cursor-pointer"
          >
            <svg className="w-5 h-5 mr-1.5" viewBox="0 0 24 24">
              <path fill="#EA4335" d="M12 5.04c1.62 0 3.08.56 4.22 1.65l3.15-3.15C17.45 1.7 14.93.8 12 .8 7.37.8 3.4 3.4 1.45 7.15l3.79 2.94c.94-2.82 3.57-5.05 6.76-5.05z" />
              <path fill="#4285F4" d="M23.49 12.27c0-.82-.07-1.61-.21-2.38H12v4.51h6.44a5.51 5.51 0 0 1-2.39 3.61l3.71 2.87c2.17-2 3.43-4.94 3.43-8.61z" />
              <path fill="#34A853" d="M12 23.2c3.24 0 5.95-1.07 7.93-2.91l-3.71-2.87c-1.03.69-2.35 1.1-3.93 1.1-3.19 0-5.9-2.15-6.86-5.05L1.5 16.33c2.01 3.96 6.1 6.87 10.5 6.87z" />
              <path fill="#FBBC05" d="M5.14 13.47a6.97 6.97 0 0 1 0-4.44L1.35 6.09A11.94 11.94 0 0 0 0 11.25c0 1.83.41 3.57 1.14 5.14l4-3.1-.28-.18z" />
            </svg>
            <span>Continue with Google</span>
          </button>
        </div>

        <div className="mt-8 flex items-center justify-center space-x-2 text-xs text-[#9CA3AF] font-medium">
          <ShieldCheck className="w-4 h-4 text-[#5B5CEB]" />
          <span>Enterprise SSO enforced</span>
        </div>

        <div className="mt-8 pt-6 border-t border-[#E7EAF2] text-center">
          <p className="text-xs text-[#9CA3AF] leading-relaxed">
            By continuing, you agree to our <br/>
            <a href="#" className="text-[#6B7280] hover:text-[#111827] transition-colors underline decoration-[#E7EAF2] underline-offset-2">Terms of Service</a> and <a href="#" className="text-[#6B7280] hover:text-[#111827] transition-colors underline decoration-[#E7EAF2] underline-offset-2">Privacy Policy</a>.
          </p>
        </div>
      </motion.div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen w-full flex items-center justify-center bg-[#F6F7FB]">
        <Lock className="w-6 h-6 text-[#9CA3AF] animate-pulse" />
      </div>
    }>
      <LoginModal />
    </Suspense>
  );
}
