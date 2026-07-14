import pytest
import pandas as pd
import os
from core.agents.data_quality import DataQualityAgent

def test_excellent_quality():
    agent = DataQualityAgent(output_dir="data")
    
    # Perfect dataset
    df = pd.DataFrame({
        "id": range(100),
        "feature_1": [x * 0.5 for x in range(100)],
        "feature_2": [x * 1.5 for x in range(100)],
        "target": ["A", "B"] * 50 # perfectly balanced
    })
    
    res = agent.analyze(df, "perfect.csv", target_col="target")
    assert res["health_score"] >= 90
    assert res["classification"] in ["Excellent", "Good"]
    assert res["cleaning_required"] is False
    assert os.path.exists(res["report_path"])

def test_poor_quality():
    agent = DataQualityAgent(output_dir="data")
    
    # Messy dataset
    df = pd.DataFrame({
        "id": [1] * 50 + [2] * 50, # 50% duplicates
        "constant": ["Always"] * 100, # constant column
        "missing": [None] * 50 + [1] * 50, # 50% missing in this column
        "target": ["A"] * 90 + ["B"] * 10 # 90% imbalanced
    })
    
    res = agent.analyze(df, "messy.csv", target_col="target")
    assert res["health_score"] < 90
    assert res["cleaning_required"] is True
    
    reasons = " ".join(res["reasons"]).lower()
    assert "constant" in reasons
    assert "duplicate" in reasons
    assert "missing" in reasons
    assert "imbalance" in reasons
