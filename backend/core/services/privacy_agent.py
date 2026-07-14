import os
import json
import re
import pandas as pd
import numpy as np

class MaskingEngine:
    def mask_email(self, val):
        if pd.isna(val): return val
        val_str = str(val)
        if '@' in val_str:
            local, domain = val_str.split('@', 1)
            return '*' * max(len(local), 4) + '@' + domain
        return '*' * 8

    def mask_phone(self, val):
        if pd.isna(val): return val
        val_str = str(val).strip()
        # To handle cases like 9876543210 -> 98******10
        if len(val_str) >= 4:
            return val_str[:2] + '*' * (len(val_str) - 4) + val_str[-2:]
        return '*' * len(val_str)

    def mask_pseudonymize(self, series: pd.Series, prefix="Entity_") -> pd.Series:
        # Generate unique IDs for each unique value
        unique_vals = series.dropna().unique()
        mapping = {val: f"{prefix}{i+1:03d}" for i, val in enumerate(unique_vals)}
        return series.map(mapping).fillna(series)
        
    def mask_generic(self, val):
        if pd.isna(val): return val
        return '*' * len(str(val))

class PrivacyAgent:
    def __init__(self):
        self.masking_engine = MaskingEngine()
        
        # Regex patterns
        self.patterns = {
            "email": re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'),
            "phone": re.compile(r'^\+?[\d\s-]{10,14}$'),
            "pan": re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]$', re.IGNORECASE),
            "aadhaar": re.compile(r'^\d{4}\s?\d{4}\s?\d{4}$'),
            "credit_card": re.compile(r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9][0-9])[0-9]{12})$'),
        }
        
        # Column name heuristics (lowercase)
        self.heuristics = {
            "name": ["name", "first_name", "last_name", "fullname", "first name", "last name"],
            "address": ["address", "street", "city", "zipcode", "postal", "location"],
            "dob": ["dob", "date of birth", "birthdate", "birth_date"],
            "id": ["customer id", "customer_id", "employee id", "employee_id", "emp_id", "cust_id"]
        }
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.workspace_base = os.path.abspath(os.path.join(base_dir, "../../data/workspace"))
        os.makedirs(self.workspace_base, exist_ok=True)

    def detect_pii(self, df: pd.Series, col_name: str) -> str:
        col_lower = str(col_name).lower()
        
        # 1. Check heuristics (exact match or prominent substring)
        for pii_type, keywords in self.heuristics.items():
            if any(keyword in col_lower for keyword in keywords):
                return pii_type
                
        # Skip regex matching for datetime columns to prevent false positives (like dates matching phone regex)
        if pd.api.types.is_datetime64_any_dtype(df):
            return None
            
        # 2. Check regex on sample
        sample = df.dropna().head(100).astype(str)
        if sample.empty:
            return None
            
        import re
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}.*$')
            
        for pii_type, pattern in self.patterns.items():
            if pii_type == 'phone':
                # Filter out likely dates before checking phone numbers
                sample_phone = sample[~sample.apply(lambda x: bool(date_pattern.match(x)))]
                match_count = sample_phone.apply(lambda x: bool(pattern.match(x))).sum()
                # Use original len(sample) to ensure it truly is a column of phone numbers
                if len(sample) > 0 and match_count / len(sample) > 0.5: 
                    return pii_type
            else:
                match_count = sample.apply(lambda x: bool(pattern.match(x))).sum()
                if match_count / len(sample) > 0.5: # If more than 50% match
                    return pii_type
                
        return None

    def process(self, df: pd.DataFrame, dataset_name: str) -> tuple[pd.DataFrame, dict]:
        report = {
            "columns_containing_pii": {},
            "masking_applied": {},
            "risk_score": 0
        }
        
        masked_df = df.copy()
        pii_columns_found = 0
        total_columns = len(df.columns)
        
        for col in df.columns:
            pii_type = self.detect_pii(df[col], col)
            if pii_type:
                pii_columns_found += 1
                report["columns_containing_pii"][col] = pii_type
                
                if pii_type == "email":
                    masked_df[col] = df[col].apply(self.masking_engine.mask_email)
                    report["masking_applied"][col] = "Partial Masking (Email)"
                elif pii_type == "phone":
                    masked_df[col] = df[col].apply(self.masking_engine.mask_phone)
                    report["masking_applied"][col] = "Partial Masking (Phone)"
                elif pii_type in ["name", "id"]:
                    prefix = "Customer_" if "cust" in col.lower() else ("Employee_" if "emp" in col.lower() else "Entity_")
                    masked_df[col] = self.masking_engine.mask_pseudonymize(df[col], prefix=prefix)
                    report["masking_applied"][col] = "Pseudonymization"
                else: # Generic mask for PAN, Aadhaar, Credit Card, DOB, Address
                    masked_df[col] = df[col].apply(self.masking_engine.mask_generic)
                    report["masking_applied"][col] = "Full Masking"
                    
        # Calculate Risk Score (0 to 100)
        # Based on proportion of PII columns and severity (e.g., PAN/CC is high risk)
        if total_columns > 0:
            base_risk = (pii_columns_found / total_columns) * 50
            # Add penalty for highly sensitive info
            high_risk_types = ["pan", "aadhaar", "credit_card", "address"]
            high_risk_found = sum(1 for t in report["columns_containing_pii"].values() if t in high_risk_types)
            risk_score = min(100, int(base_risk + (high_risk_found * 15)))
            report["risk_score"] = risk_score
            
        # Store report
        ds_name, _ = os.path.splitext(dataset_name)
        workspace_dir = os.path.join(self.workspace_base, ds_name)
        os.makedirs(workspace_dir, exist_ok=True)
        with open(os.path.join(workspace_dir, "privacy_report.json"), "w") as f:
            json.dump(report, f, indent=2)
            
        return masked_df, report

privacy_agent = PrivacyAgent()
