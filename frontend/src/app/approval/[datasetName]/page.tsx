"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckCircle, ShieldAlert, Zap } from "lucide-react";
import { AgentStatusLoader } from "@/components/ui/design-system";

export default function ApprovalPage() {
  const { datasetName } = useParams();
  const router = useRouter();
  
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [disabledAgents, setDisabledAgents] = useState<string[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/approval/pending/${datasetName}`)
      .then((res) => {
        if (!res.ok) throw new Error("Plan not found or already approved.");
        return res.json();
      })
      .then((payload) => {
        setData(payload);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [datasetName]);

  const toggleAgent = (action: string) => {
    if (disabledAgents.includes(action)) {
      setDisabledAgents(disabledAgents.filter(a => a !== action));
    } else {
      setDisabledAgents([...disabledAgents, action]);
    }
  };

  const handleApprove = async () => {
    setSubmitting(true);
    try {
      const allAgents = data.recommendations.recommendations.map((r: any) => r.action);
      const approved = allAgents.filter((a: string) => !disabledAgents.includes(a));
      
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/approval/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          dataset_name: datasetName,
          approved_agents: approved
        })
      });
      
      if (!res.ok) throw new Error("Failed to submit approval.");
      
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message);
      setSubmitting(false);
    }
  };

  if (loading) return <div className="h-screen pt-24 bg-[#F8F9FC]"><AgentStatusLoader /></div>;
  if (error) return <div className="flex h-screen items-center justify-center text-red-500">{error}</div>;

  const { recommendations, health_score, classification } = data;
  const header = recommendations.header;
  const recs = recommendations.recommendations;
  const totalTime = recommendations.total_estimated_time_sec;

  return (
    <div className="min-h-screen bg-neutral-950 text-white p-10">
      <div className="max-w-4xl mx-auto space-y-6">
        
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-neutral-100">Workflow Approval</h1>
            <p className="text-neutral-400 mt-2">{header}</p>
          </div>
          <div className="text-right">
            <div className="text-neutral-400 text-sm">Health Score</div>
            <div className={`text-2xl font-black ${health_score > 80 ? 'text-green-500' : 'text-amber-500'}`}>
              {health_score}/100 <span className="text-lg opacity-70">({classification})</span>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          {recs.map((rec: any, idx: number) => {
            const isDisabled = disabledAgents.includes(rec.action);
            return (
              <Card key={idx} className={`bg-neutral-900 border-neutral-800 transition-opacity ${isDisabled ? 'opacity-40' : 'opacity-100'}`}>
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle className="text-xl flex items-center gap-2 text-neutral-200">
                      {rec.action}
                    </CardTitle>
                    <CardDescription className="text-neutral-400 mt-1">{rec.reason}</CardDescription>
                  </div>
                  <Button 
                    variant={isDisabled ? "outline" : "destructive"} 
                    className={isDisabled ? "border-neutral-700" : "bg-red-500/10 text-red-500 hover:bg-red-500/20"}
                    onClick={() => toggleAgent(rec.action)}
                  >
                    {isDisabled ? "Enable" : "Remove"}
                  </Button>
                </CardHeader>
                <CardContent className="grid grid-cols-3 gap-4 text-sm">
                  <div className="bg-neutral-950 p-3 rounded border border-neutral-800">
                    <div className="text-neutral-500 mb-1 flex items-center gap-2"><CheckCircle className="w-4 h-4"/> Benefit</div>
                    <div className="text-neutral-300">{rec.expected_benefit}</div>
                  </div>
                  <div className="bg-neutral-950 p-3 rounded border border-neutral-800">
                    <div className="text-neutral-500 mb-1 flex items-center gap-2"><Zap className="w-4 h-4"/> Duration</div>
                    <div className="text-neutral-300">{rec.estimated_duration_sec} sec</div>
                  </div>
                  <div className="bg-neutral-950 p-3 rounded border border-neutral-800">
                    <div className="text-neutral-500 mb-1 flex items-center gap-2"><ShieldAlert className="w-4 h-4"/> Risk Profile</div>
                    <div className="text-neutral-300">{rec.risk}</div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="flex items-center justify-between p-6 bg-neutral-900 rounded-lg border border-neutral-800">
          <div>
            <div className="text-lg font-bold text-neutral-200">Estimated Total Time: {totalTime} seconds</div>
            <div className="text-sm text-neutral-500">You have disabled {disabledAgents.length} workflows.</div>
          </div>
          <div className="flex gap-4">
            <Button variant="outline" className="border-neutral-700" onClick={() => router.push("/dashboard")}>Cancel</Button>
            <Button 
              className="bg-emerald-600 hover:bg-emerald-500 text-white" 
              onClick={handleApprove}
              disabled={submitting}
            >
              {submitting ? "Approving..." : "Approve & Execute"}
            </Button>
          </div>
        </div>

      </div>
    </div>
  );
}
