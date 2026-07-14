import pandas as pd
import numpy as np
import json
import os
from typing import Dict, Any

class DataQualityAgent:
    """
    Evaluates dataset hygiene dynamically. Determines whether a Cleaning Pipeline is mathematically required.
    Does NOT modify or clean the data itself.
    """
    
    def __init__(self, output_dir: str = "data"):
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../../{output_dir}")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def analyze(self, df: pd.DataFrame, dataset_name: str, target_col: str = None) -> Dict[str, Any]:
        """
        Executes a rigorous quality diagnostic across missing values, duplicates, variance, and class balance.
        """
        rows, cols = df.shape
        if rows == 0 or cols == 0:
            return self._generate_critical_failure(dataset_name)
            
        metrics = {}
        
        # 1. Missing Values Mapping
        missing_count = int(df.isnull().sum().sum())
        missing_ratio = missing_count / (rows * cols) if rows * cols > 0 else 0
        metrics["missing_values"] = {"count": missing_count, "ratio": float(missing_ratio)}
        
        # 2. Duplicate Detection
        duplicate_count = int(df.duplicated().sum())
        duplicate_ratio = duplicate_count / rows if rows > 0 else 0
        metrics["duplicates"] = {"count": duplicate_count, "ratio": float(duplicate_ratio)}
        
        # 3. Variance & Constant Columns Detection
        constant_cols = []
        low_variance_cols = []
        for col in df.columns:
            unique_vals = df[col].nunique(dropna=False)
            if unique_vals <= 1:
                constant_cols.append(col)
                
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            variances = numeric_df.var()
            low_variance_cols = variances[variances < 1e-4].index.tolist()
            
        metrics["constant_columns"] = constant_cols
        metrics["low_variance_columns"] = list(set(low_variance_cols) - set(constant_cols))
        
        # 4. Statistical Outliers (Z-Score heuristic)
        outlier_cols = {}
        if not numeric_df.empty:
            for col in numeric_df.columns:
                series = numeric_df[col].dropna()
                if not series.empty:
                    mean, std = series.mean(), series.std()
                    if std > 0:
                        z_scores = np.abs((series - mean) / std)
                        outlier_count = int((z_scores > 3).sum())
                        if outlier_count > 0:
                            outlier_cols[col] = outlier_count
        metrics["outliers"] = outlier_cols
        
        # 5. Class Imbalance Assessment
        imbalance_flag = False
        if target_col and target_col in df.columns:
            if df[target_col].nunique() < 20: # Assumed Categorical
                class_counts = df[target_col].value_counts(normalize=True)
                if not class_counts.empty and class_counts.iloc[0] > 0.8: # Single class dominates > 80%
                    imbalance_flag = True
        metrics["imbalanced_target"] = imbalance_flag
        
        # 6. Algorithmic Health Scoring Matrix
        score = 100.0
        
        # Severe penalty for missing data (Max -35)
        score -= min(35, missing_ratio * 100 * 2) 
        # Moderate penalty for duplicates (Max -20)
        score -= min(20, duplicate_ratio * 100 * 1.5)
        # Structural penalty for constant columns (-5 per column)
        score -= min(15, len(constant_cols) * 5)
        # Minor penalty for outliers (-2 per affected column)
        score -= min(10, len(outlier_cols) * 2)
        # Strategic penalty for imbalance (-10)
        if imbalance_flag:
            score -= 10
            
        health_score = max(0, int(score))
        
        # 7. Tiered Classification
        if health_score >= 90:
            classification = "Excellent"
        elif health_score >= 80:
            classification = "Good"
        elif health_score >= 60:
            classification = "Average"
        elif health_score >= 40:
            classification = "Poor"
        else:
            classification = "Critical"
            
        # Decision Intelligence Trigger
        cleaning_required = health_score < 90
        
        # 8. Report Generation & Recommendations
        reasons = []
        recommendations = []
        if missing_ratio > 0:
            reasons.append(f"{(missing_ratio*100):.1f}% missing value contamination detected across the grid.")
            recommendations.append("Execute Cleaning Agent: Impute or drop NaN values.")
        if duplicate_ratio > 0:
            reasons.append(f"{(duplicate_ratio*100):.1f}% duplicate row redundancy detected.")
            recommendations.append("Execute Cleaning Agent: Drop exact row duplicates.")
        if constant_cols:
            reasons.append(f"{len(constant_cols)} constant uninformative columns found.")
            recommendations.append(f"Execute Cleaning Agent: Drop constant columns: {constant_cols}")
        if imbalance_flag:
            reasons.append(f"Target column '{target_col}' exhibits severe class imbalance (>80% majority).")
            recommendations.append("Execute Feature Engineering Agent: Apply SMOTE or enforce class weights.")
            
        if not reasons:
            reasons.append("Data is pristine, clean, and structurally sound.")
            recommendations.append("Bypass Cleaning Agent. Proceed directly to AutoML pipelines.")

        report = {
            "dataset_name": dataset_name,
            "health_score": health_score,
            "classification": classification,
            "cleaning_required": cleaning_required,
            "metrics": metrics,
            "reasons": reasons,
            "recommendations": recommendations,
            "confidence": 0.95
        }
        
        # 9. JSON Serialization
        report_filename = f"{dataset_name.split('.')[0]}_quality_report.json"
        report_path = os.path.join(self.output_dir, report_filename)
        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)
            
        return {
            "health_score": health_score,
            "classification": classification,
            "cleaning_required": cleaning_required,
            "reasons": reasons,
            "recommendations": recommendations,
            "report_path": report_path,
            "report_data": report,
            "confidence": 0.95
        }
        
    def _generate_critical_failure(self, dataset_name: str):
        return {
            "health_score": 0,
            "classification": "Critical",
            "cleaning_required": True,
            "reasons": ["Dataset structure is empty or fundamentally unparsable."],
            "recommendations": ["Halt Pipeline. Await new file ingestion."],
            "confidence": 1.0
        }
