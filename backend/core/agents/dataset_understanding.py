import pandas as pd
import json
import os
from typing import Dict, Any, List

class DatasetUnderstandingAgent:
    """
    Analyzes datasets strictly for structural and semantic understanding.
    Never modifies data. Never generates visualizations. Never trains models.
    """
    
    def __init__(self, output_dir: str = "data"):
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../../{output_dir}")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def analyze(self, df: pd.DataFrame, dataset_name: str) -> Dict[str, Any]:
        """
        Executes the understanding loop over the provided DataFrame.
        """
        
        # 1. Basic Structural Stats
        rows, cols = df.shape
        mem_usage = df.memory_usage(deep=True).sum() / (1024 * 1024) # Size in MB
        
        # 2. Type Detection
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
        bool_cols = df.select_dtypes(include=['bool']).columns.tolist()
        
        # 3. Semantic Heuristics & Inference
        possible_ids = []
        possible_targets = []
        possible_timestamps = datetime_cols.copy()
        
        for col in df.columns:
            col_lower = str(col).lower()
            unique_count = df[col].nunique()
            
            # Identify IDs (Maximum cardinality, specific nomenclature)
            if unique_count == rows and ('id' in col_lower or 'key' in col_lower or 'index' in col_lower):
                possible_ids.append(col)
                
            # Identify Targets (Nomenclature or low-cardinality flags in moderate+ datasets)
            if any(term in col_lower for term in ['target', 'label', 'class', 'price', 'amount', 'churn']):
                possible_targets.append(col)
            elif unique_count < 15 and rows > 100 and col not in possible_ids:
                if col not in possible_targets:
                    possible_targets.append(col)
                
            # Identify Timestamps hidden as strings
            if col not in possible_timestamps and ('date' in col_lower or 'time' in col_lower):
                possible_timestamps.append(col)

        # 4. Infer Machine Learning Task
        possible_tasks = ["EDA only", "Business Intelligence"]
        
        if possible_targets:
            target_col = possible_targets[0]
            # Continuous targets usually mean Regression
            if target_col in numeric_cols and df[target_col].nunique() > 20:
                possible_tasks.insert(0, "Regression")
            else:
                possible_tasks.insert(0, "Classification")
                
        if possible_timestamps:
            possible_tasks.append("Forecasting")
            
        if len(numeric_cols) > 2 and rows > 50:
            possible_tasks.append("Clustering")
            
        # 5. Dataset Purpose
        primary_task = possible_tasks[0]
        if primary_task == 'Classification':
            purpose = "Categorical prediction and classification"
        elif primary_task == 'Regression':
            purpose = "Continuous value prediction and forecasting"
        else:
            purpose = "General exploratory analytics"

        # 6. Construct Immutable Profile
        profile = {
            "dataset_name": dataset_name,
            "basic_stats": {
                "rows": rows,
                "columns": cols,
                "file_size_mb": round(mem_usage, 4)
            },
            "columns": {
                "names": df.columns.tolist(),
                "numeric": numeric_cols,
                "categorical": categorical_cols,
                "datetime": datetime_cols,
                "boolean": bool_cols
            },
            "inferred_meta": {
                "possible_ids": possible_ids,
                "possible_targets": possible_targets,
                "possible_timestamps": possible_timestamps
            },
            "inference": {
                "dataset_purpose": purpose,
                "possible_ml_tasks": possible_tasks
            }
        }
        
        # 7. Persist Profile to Disk
        profile_filename = f"{dataset_name.split('.')[0]}_profile.json"
        profile_path = os.path.join(self.output_dir, profile_filename)
        
        with open(profile_path, "w") as f:
            json.dump(profile, f, indent=4)
            
        # 8. Actionable Recommendations
        recommended_step = "Run EDA Agent to explore distributions."
        if primary_task in ['Classification', 'Regression']:
            recommended_step = "Run Cleaning Agent followed by AutoML Agent."
            
        # Final Return Payload
        return {
            "dataset_summary": f"Dataset '{dataset_name}' contains {rows} rows and {cols} columns. Identified as a likely {primary_task} task.",
            "confidence": 0.88,
            "reasoning": f"Analyzed cardinality across {cols} columns. Identified targets {possible_targets}, leading to {primary_task} inference.",
            "recommended_next_step": recommended_step,
            "profile_path": profile_path,
            "profile_data": profile
        }
