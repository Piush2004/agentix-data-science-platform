import os
import json
import pandas as pd
import numpy as np
import pytest
from core.services.privacy_agent import privacy_agent, MaskingEngine

def test_masking_engine_email():
    engine = MaskingEngine()
    assert engine.mask_email("john@gmail.com") == "****@gmail.com"
    assert engine.mask_email("a@b.com") == "****@b.com"
    assert engine.mask_email("invalidemail") == "********"

def test_masking_engine_phone():
    engine = MaskingEngine()
    assert engine.mask_phone("9876543210") == "98******10"
    assert engine.mask_phone("+1234567890") == "+1*******90"
    assert engine.mask_phone("123") == "***"

def test_masking_engine_pseudonymize():
    engine = MaskingEngine()
    series = pd.Series(["John Smith", "Alice", "John Smith", np.nan])
    masked = engine.mask_pseudonymize(series, "Customer_")
    assert masked.iloc[0] == "Customer_001"
    assert masked.iloc[1] == "Customer_002"
    assert masked.iloc[2] == "Customer_001"
    assert pd.isna(masked.iloc[3])

def test_privacy_agent_detect_and_process(tmp_path, monkeypatch):
    monkeypatch.setattr(privacy_agent, "workspace_base", str(tmp_path))
    
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "customer_name": ["Alice Smith", "Bob Jones", "Charlie Brown"],
        "contact_email": ["alice@gmail.com", "bob@yahoo.com", "charlie@hotmail.com"],
        "user_phone": ["9876543210", "1234567890", "5555555555"],
        "public_score": [85.5, 90.0, 88.0]
    })
    
    masked_df, report = privacy_agent.process(df, "test_dataset.csv")
    
    # Check that report accurately reflects detection
    assert "customer_name" in report["columns_containing_pii"]
    assert "contact_email" in report["columns_containing_pii"]
    assert "user_phone" in report["columns_containing_pii"]
    assert "public_score" not in report["columns_containing_pii"]
    
    # Check masking applied
    assert report["masking_applied"]["contact_email"] == "Partial Masking (Email)"
    assert report["masking_applied"]["user_phone"] == "Partial Masking (Phone)"
    
    # Check Risk Score
    assert report["risk_score"] > 0
    
    # Check actual DataFrame masking
    assert masked_df["contact_email"].iloc[0] == "*****@gmail.com"
    assert masked_df["user_phone"].iloc[0] == "98******10"
    assert masked_df["customer_name"].iloc[0] == "Customer_001"
    assert masked_df["public_score"].iloc[0] == 85.5
    
    # Check file persistence
    workspace_dir = os.path.join(str(tmp_path), "test_dataset")
    assert os.path.exists(os.path.join(workspace_dir, "privacy_report.json"))
