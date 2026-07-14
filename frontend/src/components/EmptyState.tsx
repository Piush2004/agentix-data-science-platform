import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Database, Plus } from "lucide-react";
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function EmptyState({ message = "No dataset currently active in memory." }: { message?: string }) {
  return (
    <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="flex items-center justify-center h-[60vh]">
      <Card className="max-w-md border-gray-800 bg-gray-900/50 backdrop-blur-xl shadow-2xl text-center">
        <CardContent className="p-10 space-y-6 flex flex-col items-center">
          <div className="p-6 bg-blue-500/10 rounded-full">
            <Database className="w-12 h-12 text-blue-400" />
          </div>
          <div className="space-y-2">
            <h2 className="text-2xl font-bold text-white">No Active Context</h2>
            <p className="text-gray-400">{message}</p>
          </div>
          <div className="flex gap-4">
            <Link href="/demo">
              <Button variant="outline" className="border-gray-700 hover:bg-gray-800 text-gray-300">Run Demo Workflow</Button>
            </Link>
            <Link href="/data/ingestion">
              <Button className="bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(59,130,246,0.3)]">
                <Plus className="w-4 h-4 mr-2" /> Upload Data
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
