import json
import os
from typing import Dict, Any, Optional

import json
from core.redis_client import get_redis

class ContextCache:
    def __init__(self):
        self.redis = get_redis()
        self.fallback = {}

    def get(self, dataset_name: str) -> str:
        try:
            if self.redis:
                val = self.redis.get(f"chat_context:{dataset_name}")
                return val if val else None
        except:
            pass
        return self.fallback.get(dataset_name)

    def set(self, dataset_name: str, context: str):
        try:
            if self.redis:
                self.redis.setex(f"chat_context:{dataset_name}", 3600, context)
                return
        except:
            pass
        self.fallback[dataset_name] = context

    def clear(self):
        try:
            if self.redis:
                keys = self.redis.keys("chat_context:*")
                if keys:
                    self.redis.delete(*keys)
        except:
            pass
        self.fallback = {}

class ContextBuilder:
    def __init__(self):
        self.cache = ContextCache()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.workspace_base = os.path.abspath(os.path.join(base_dir, "../../data/workspace"))
        
    def _load_json(self, dataset_name: str, filename: str) -> dict:
        ds_name, _ = os.path.splitext(dataset_name)
        file_path = os.path.join(self.workspace_base, ds_name, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def build_context(self, dataset_name: str, eda: dict = None, model_metrics: dict = None, question: str = "") -> str:
        cached_base = self.cache.get(dataset_name)
        if cached_base:
            base_context = cached_base
        else:
            metadata = self._load_json(dataset_name, "metadata.json")
            statistics = self._load_json(dataset_name, "statistics.json")
            privacy_report = self._load_json(dataset_name, "privacy_report.json")
            
            base_context = self._format_base_context(dataset_name, metadata, statistics, privacy_report)
            self.cache.set(dataset_name, base_context)
            
        dynamic_context = self._format_dynamic_context(eda, model_metrics)
        
        prompt = f"{base_context}\n{dynamic_context}\nUser Question: {question}\n"
        
        # Enforce max context size of ~5KB (5000 chars)
        if len(prompt) > 5000:
            return prompt[:5000] + "...[TRUNCATED]"
        return prompt

    def _format_base_context(self, dataset_name: str, metadata: dict, statistics: dict, privacy: dict) -> str:
        rows = metadata.get("Rows", "Unknown")
        cols = metadata.get("Columns", "Unknown")
        target = metadata.get("Target column", "Unknown")
        
        total_cells = rows * cols if isinstance(rows, int) and isinstance(cols, int) else 0
        total_missing = sum(metadata.get("Null count", {}).values()) if metadata and "Null count" in metadata else 0
        missing_pct = round((total_missing / total_cells * 100), 2) if total_cells > 0 else 0
        
        context = f"Dataset: {dataset_name}\n"
        context += f"Shape: {rows} rows, {cols} columns\n"
        context += f"Target: {target}\n"
        context += f"Missing Data: {missing_pct}%\n"
        
        if privacy:
            risk = privacy.get("risk_score", 0)
            context += f"Privacy Risk Score: {risk}/100\n"
            pii_cols = list(privacy.get("columns_containing_pii", {}).keys())
            if pii_cols:
                context += f"Masked PII Columns: {', '.join(pii_cols)}\n"
                
        if "Correlation matrix" in statistics:
            corr_matrix = statistics["Correlation matrix"]
            correlations = []
            for col1, row_vals in corr_matrix.items():
                if isinstance(row_vals, dict):
                    for col2, val in row_vals.items():
                        if col1 != col2 and val is not None:
                            try:
                                correlations.append((col1, col2, abs(float(val))))
                            except ValueError:
                                pass
                                
            unique_corrs = []
            seen = set()
            for c1, c2, val in correlations:
                if (c1, c2) not in seen and (c2, c1) not in seen:
                    unique_corrs.append((c1, c2, val))
                    seen.add((c1, c2))
            unique_corrs.sort(key=lambda x: x[2], reverse=True)
            top_corrs = unique_corrs[:5]
            if top_corrs:
                context += "Top Correlations:\n"
                for c1, c2, val in top_corrs:
                    context += f" - {c1} & {c2}: {val:.2f}\n"
                    
        return context
        
    def _format_dynamic_context(self, eda: dict, metrics: dict) -> str:
        context = ""
        if eda:
            context += "EDA Insights:\n"
            for k, v in eda.items():
                context += f" - {k}: {v}\n"
                
        if metrics:
            context += "Model Metrics:\n"
            acc = metrics.get("accuracy", metrics.get("r2", metrics.get("accuracy_score", "N/A")))
            context += f" - Performance (Accuracy/R2): {acc}\n"
            feat_imp = metrics.get("feature_importance", {})
            if feat_imp:
                sorted_feats = sorted(feat_imp.items(), key=lambda x: x[1], reverse=True)[:3]
                context += " - Top Features: " + ", ".join([f"{k} ({v:.2f})" for k, v in sorted_feats]) + "\n"
                
        return context

class PromptBuilder:
    def __init__(self):
        self.context_builder = ContextBuilder()
        
    def build_prompt(self, dataset_name: str, question: str, eda: dict = None, model_metrics: dict = None) -> str:
        context = self.context_builder.build_context(dataset_name, eda, model_metrics, question)
        prompt = (
            "You are a Data Intelligence Assistant.\n"
            "Use the following structured metadata to answer the user's question.\n"
            "NEVER request raw row data.\n\n"
            f"{context}\n"
            "Answer:"
        )
        return prompt

context_builder = ContextBuilder()
prompt_builder = PromptBuilder()
