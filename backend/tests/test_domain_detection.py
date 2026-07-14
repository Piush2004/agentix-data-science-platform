import pytest
import pandas as pd
import os
from core.agents.domain_detection import DomainDetectionAgent

def test_domain_retail():
    agent = DomainDetectionAgent(output_dir="data")
    
    df = pd.DataFrame({
        "product_id": [1, 2],
        "sales_volume": [100, 200],
        "store_location": ["NY", "CA"],
        "customer_age": [30, 40],
        "revenue_total": [1000.0, 2000.0]
    })
    
    res = agent.analyze(df, "retail.csv")
    
    assert res["primary_domain"] == "Retail"
    assert res["confidence"] > 0.8
    assert "product" in res["reasoning"].lower() or "sales" in res["reasoning"].lower()

def test_domain_healthcare():
    agent = DomainDetectionAgent(output_dir="data")
    
    df = pd.DataFrame({
        "patient_id": [1, 2],
        "doctor_name": ["Smith", "Jones"],
        "diagnosis_code": ["A1", "B2"],
        "blood_pressure": [120, 130]
    })
    
    res = agent.analyze(df, "health.csv")
    
    assert res["primary_domain"] == "Healthcare"
    assert res["confidence"] > 0.7

def test_domain_generic():
    agent = DomainDetectionAgent(output_dir="data")
    
    df = pd.DataFrame({
        "col_a": [1, 2],
        "col_b": [3, 4]
    })
    
    res = agent.analyze(df, "generic.csv")
    assert res["primary_domain"] == "General/Agnostic"
    assert res["confidence"] == 0.50
