import pytest
import pandas as pd
import os
from core.agents.dataset_understanding import DatasetUnderstandingAgent

def test_dataset_understanding_classification():
    agent = DatasetUnderstandingAgent(output_dir="data")
    
    # Mock dataframe with obvious classification signatures (low cardinality boolean/categorical target)
    df = pd.DataFrame({
        "customer_id": range(100),
        "age": [25] * 100,
        "is_active": [True] * 100,
        "churn_label": ["Yes", "No"] * 50
    })
    
    result = agent.analyze(df, "mock_churn.csv")
    
    assert result["confidence"] > 0
    assert "Classification" in result["dataset_summary"]
    
    profile = result["profile_data"]
    assert "churn_label" in profile["inferred_meta"]["possible_targets"]
    assert "customer_id" in profile["inferred_meta"]["possible_ids"]
    assert "Classification" in profile["inference"]["possible_ml_tasks"]
    
    profile_path = result["profile_path"]
    assert os.path.exists(profile_path)
    
def test_dataset_understanding_regression():
    agent = DatasetUnderstandingAgent(output_dir="data")
    
    # Mock dataframe with obvious regression signatures (continuous target)
    df = pd.DataFrame({
        "house_id": range(150),
        "sqft": [1500 + (i % 20) for i in range(150)],
        "price": [250000.0 + i for i in range(150)] # High cardinality numeric target
    })
    
    result = agent.analyze(df, "mock_housing.csv")
    
    assert "Regression" in result["dataset_summary"]
    
    profile = result["profile_data"]
    assert "price" in profile["inferred_meta"]["possible_targets"]
    assert "house_id" in profile["inferred_meta"]["possible_ids"]
    assert "Regression" in profile["inference"]["possible_ml_tasks"]
