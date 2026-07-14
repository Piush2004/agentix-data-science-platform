import { create } from 'zustand';
import axios from 'axios';

export interface DashboardMetrics {
  active_dataset: string;
  dataset_health_score: number;
  best_model: string;
  model_accuracy: number;
  active_agents: number;
  ollama_status: string;
  langgraph_status: string;
  mlops_status: string;
  workflow_state: string;
}

export interface ProfileData {
  rows: number;
  cols: number;
  missing: number;
  duplicates: number;
  outliers: number;
  schema: Record<string, string>;
}

export interface EDAData {
  correlations: Record<string, Record<string, number>>;
  histograms: Record<string, { counts: number[]; bins: number[] }>;
  boxplots: Record<string, { min: number; q1: number; median: number; q3: number; max: number }>;
  statistics: Record<string, { mean: number; std: number; skew: number }>;
}

export interface AutoMLData {
  problem_type: string;
  target: string;
  best_model: string;
  leaderboard: {
    model: string;
    r2_score: number;
    rmse: number;
    mae: number;
    cv_mean: number;
    cv_std: number;
    hyperparameters: Record<string, any>;
    feature_importances?: Record<string, number>;
  }[];
}

export interface XAIData {
  top_drivers: string[];
  bias_detected: boolean;
  leakage_alert: boolean;
  dominant_feature: string;
  importances: Record<string, number>;
  waterfall: { feature: string; start: number; end: number; impact: number }[];
  base_value: number;
  final_prediction: number;
}

export interface InsightsData {
  insights: string[];
}

export interface RecommendationsData {
  actions: string[];
}

export interface MLOpsData {
  status: string;
  drift: boolean;
  accuracy_trend: number[];
  deployments: number;
}

interface PlatformState {
  // Global State
  datasetName: string | null;
  isLoading: boolean;
  error: string | null;
  
  // Data Objects
  dashboardMetrics: DashboardMetrics | null;
  profileData: ProfileData | null;
  edaData: EDAData | null;
  automlData: AutoMLData | null;
  xaiData: XAIData | null;
  insightsData: InsightsData | null;
  recommendationsData: RecommendationsData | null;
  mlopsData: MLOpsData | null;

  // Actions
  setDatasetName: (name: string) => void;
  fetchDashboardMetrics: () => Promise<void>;
  fetchEDA: () => Promise<void>;
  fetchAutoML: () => Promise<void>;
  fetchXAI: () => Promise<void>;
  fetchInsights: () => Promise<void>;
  fetchRecommendations: () => Promise<void>;
  fetchMLOps: () => Promise<void>;
}

const API_BASE = 'http://localhost:8000/api/v1/platform';

export const usePlatformStore = create<PlatformState>((set, get) => ({
  datasetName: 'live_ds', // Start with demo default for seamless UX
  isLoading: false,
  error: null,
  
  dashboardMetrics: null,
  profileData: null,
  edaData: null,
  automlData: null,
  xaiData: null,
  insightsData: null,
  recommendationsData: null,
  mlopsData: null,

  setDatasetName: (name: string) => set({ datasetName: name }),

  fetchDashboardMetrics: async () => {
    set({ isLoading: true, error: null });
    try {
      const res = await axios.get(`${API_BASE}/dashboard-metrics`);
      set({ dashboardMetrics: res.data.data, isLoading: false });
    } catch (err: unknown) {
      if (err instanceof Error) {
        set({ error: err.message, isLoading: false });
      } else {
        set({ error: String(err), isLoading: false });
      }
    }
  },

  fetchEDA: async () => {
    const ds = get().datasetName;
    if (!ds) return set({ error: 'No active dataset', edaData: null });
    set({ isLoading: true, error: null });
    try {
      const res = await axios.get(`${API_BASE}/eda?dataset_name=${ds}`);
      set({ edaData: res.data.data, isLoading: false });
    } catch (err: unknown) {
      if (err instanceof Error) {
        set({ error: err.message, isLoading: false });
      } else {
        set({ error: String(err), isLoading: false });
      }
    }
  },

  fetchAutoML: async () => {
    const ds = get().datasetName;
    if (!ds) return set({ error: 'No active dataset', automlData: null });
    set({ isLoading: true, error: null });
    try {
      const res = await axios.post(`${API_BASE}/predict`, { dataset_name: ds });
      set({ automlData: res.data.data, isLoading: false });
    } catch (err: unknown) {
      if (err instanceof Error) {
        set({ error: err.message, isLoading: false });
      } else {
        set({ error: String(err), isLoading: false });
      }
    }
  },

  fetchXAI: async () => {
    const ds = get().datasetName;
    if (!ds) return set({ error: 'No active dataset', xaiData: null });
    set({ isLoading: true, error: null });
    try {
      const res = await axios.get(`${API_BASE}/xai?dataset_name=${ds}`);
      set({ xaiData: res.data.data, isLoading: false });
    } catch (err: unknown) {
      if (err instanceof Error) {
        set({ error: err.message, isLoading: false });
      } else {
        set({ error: String(err), isLoading: false });
      }
    }
  },

  fetchInsights: async () => {
    const ds = get().datasetName;
    if (!ds) return set({ error: 'No active dataset', insightsData: null });
    set({ isLoading: true, error: null });
    try {
      const res = await axios.get(`${API_BASE}/insights?dataset_name=${ds}`);
      set({ insightsData: res.data.data, isLoading: false });
    } catch (err: unknown) {
      if (err instanceof Error) {
        set({ error: err.message, isLoading: false });
      } else {
        set({ error: String(err), isLoading: false });
      }
    }
  },

  fetchRecommendations: async () => {
    const ds = get().datasetName;
    if (!ds) return set({ error: 'No active dataset', recommendationsData: null });
    set({ isLoading: true, error: null });
    try {
      const res = await axios.get(`${API_BASE}/recommendations?dataset_name=${ds}`);
      set({ recommendationsData: res.data.data, isLoading: false });
    } catch (err: unknown) {
      if (err instanceof Error) {
        set({ error: err.message, isLoading: false });
      } else {
        set({ error: String(err), isLoading: false });
      }
    }
  },

  fetchMLOps: async () => {
    set({ isLoading: true, error: null });
    try {
      const res = await axios.get(`${API_BASE}/mlops`);
      set({ mlopsData: res.data.data, isLoading: false });
    } catch (err: unknown) {
      if (err instanceof Error) {
        set({ error: err.message, isLoading: false });
      } else {
        set({ error: String(err), isLoading: false });
      }
    }
  }
}));
