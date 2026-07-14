import os
import json
import pandas as pd
import numpy as np
import sys
from datetime import datetime
from typing import Dict, Any, Tuple
from core.services.data_service import data_service

def safe_float(val):
    if pd.isna(val) or np.isinf(val):
        return None
    return float(val)

def default_encoder(obj):
    if pd.isna(obj):
        return None
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    if isinstance(obj, (np.floating, float)):
        return safe_float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return str(obj)

class DatasetProcessor:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.workspace_base = os.path.abspath(os.path.join(base_dir, "../../data/workspace"))
        os.makedirs(self.workspace_base, exist_ok=True)
        
    def process_dataset(self, dataset_name: str, df: pd.DataFrame = None):
        # Load dataset
        if df is None:
            df = self.load_dataset(dataset_name)
            
        # Validate
        self.validate(df)
        
        # Privacy & Masking (Offline)
        from core.services.privacy_agent import privacy_agent
        df, privacy_report = privacy_agent.process(df, dataset_name)
        
        # Detect schema
        schema = self.detect_schema(df)
        
        # Generate metadata
        metadata = self.generate_metadata(df, dataset_name)
        metadata["Data types"] = schema
        
        # Generate statistics
        statistics = self.generate_statistics(df)
        
        # Generate profile
        profile = self.generate_profile(dataset_name, metadata, statistics)
        
        # Store outputs
        self.store_outputs(dataset_name, metadata, statistics, profile)
        
        return metadata, statistics, profile, privacy_report, df

    def load_dataset(self, dataset_name: str) -> pd.DataFrame:
        df = data_service.get_dataset(dataset_name)
        if df is None:
            raise ValueError(f"Dataset {dataset_name} not found in storage.")
        return df
        
    def validate(self, df: pd.DataFrame):
        if df.empty:
            raise ValueError("Dataset is empty.")
            
    def detect_schema(self, df: pd.DataFrame) -> Dict[str, str]:
        return {str(col): str(dtype) for col, dtype in df.dtypes.items()}
        
    def generate_metadata(self, df: pd.DataFrame, dataset_name: str) -> Dict[str, Any]:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
        categorical_cols = df.select_dtypes(exclude=[np.number, 'datetime', 'datetimetz']).columns.tolist()
        
        target_column = df.columns[-1] if len(df.columns) > 0 else None
        unique_values = {str(col): int(df[col].nunique()) for col in df.columns}
        null_count = {str(col): int(df[col].isna().sum()) for col in df.columns}
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.abspath(os.path.join(base_dir, "../../data"))
        file_path = os.path.join(data_dir, dataset_name)
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
        else:
            file_size = int(sys.getsizeof(df))
            
        metadata = {
            "Rows": int(len(df)),
            "Columns": int(len(df.columns)),
            "File size": file_size,
            "Memory usage": int(df.memory_usage(deep=True).sum()),
            "Column names": df.columns.tolist(),
            "Data types": self.detect_schema(df),
            "Target column": target_column,
            "Unique values": unique_values,
            "Null count": null_count,
            "Duplicate count": int(df.duplicated().sum()),
            "Numeric columns": numeric_cols,
            "Categorical columns": categorical_cols,
            "Datetime columns": datetime_cols
        }
        return metadata
        
    def generate_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        numeric_df = df.select_dtypes(include=[np.number])
        stats = {}
        
        if not numeric_df.empty:
            desc = numeric_df.describe()
            mode_vals = numeric_df.mode()
            corr_matrix = numeric_df.corr().replace({np.nan: None}).to_dict()
            
            for col in numeric_df.columns:
                try:
                    mode_val = float(mode_vals[col].dropna().iloc[0]) if not mode_vals[col].dropna().empty else None
                except Exception:
                    mode_val = None
                    
                stats[col] = {
                    "Mean": safe_float(desc.loc['mean', col]) if 'mean' in desc.index else None,
                    "Median": safe_float(desc.loc['50%', col]) if '50%' in desc.index else None,
                    "Mode": mode_val,
                    "Std": safe_float(desc.loc['std', col]) if 'std' in desc.index else None,
                    "Variance": safe_float(numeric_df[col].var()),
                    "Min": safe_float(desc.loc['min', col]) if 'min' in desc.index else None,
                    "Max": safe_float(desc.loc['max', col]) if 'max' in desc.index else None,
                    "Quartiles": {
                        "25%": safe_float(desc.loc['25%', col]) if '25%' in desc.index else None,
                        "50%": safe_float(desc.loc['50%', col]) if '50%' in desc.index else None,
                        "75%": safe_float(desc.loc['75%', col]) if '75%' in desc.index else None
                    }
                }
                
            stats["Correlation matrix"] = corr_matrix
            stats["Distribution summary"] = "Numerical distribution generated."
        else:
            stats["Distribution summary"] = "No numerical columns found."
            
        return stats

    def generate_profile(self, dataset_name: str, metadata: dict, statistics: dict) -> Dict[str, Any]:
        return {
            "dataset_name": dataset_name,
            "metadata_summary": metadata,
            "statistics_summary": statistics,
            "profiled_at": datetime.utcnow().isoformat() + "Z"
        }
        
    def store_outputs(self, dataset_name: str, metadata: dict, statistics: dict, profile: dict):
        ds_name, _ = os.path.splitext(dataset_name)
        workspace_dir = os.path.join(self.workspace_base, ds_name)
        os.makedirs(workspace_dir, exist_ok=True)
        
        with open(os.path.join(workspace_dir, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2, default=default_encoder)
            
        with open(os.path.join(workspace_dir, "statistics.json"), "w") as f:
            json.dump(statistics, f, indent=2, default=default_encoder)
            
        with open(os.path.join(workspace_dir, "profile.json"), "w") as f:
            json.dump(profile, f, indent=2, default=default_encoder)

dataset_processor = DatasetProcessor()
