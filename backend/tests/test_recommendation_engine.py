import pytest
import os
from core.services.recommendation_engine import RecommendationEngine

def test_recommendation_engine():
    engine = RecommendationEngine(output_dir="data")
    
    plan = {
        "dataset_name": "customer_churn.csv",
        "inferred_domain": "Retail Analytics",
        "inferred_task": "Classification",
        "execution_order": ["Cleaning Agent", "AutoML Agent", "SHAP Agent", "Report Agent"]
    }
    
    result = engine.generate_recommendations(plan)
    
    assert "Retail Analytics" in result["header"]
    assert len(result["recommendations"]) == 4
    assert result["total_estimated_time_sec"] == 23.0 # 0.5 + 15.0 + 5.0 + 2.5
    
    # Check Cleaning Agent parsing
    assert result["recommendations"][0]["action"] == "Clean Data"
    assert result["recommendations"][0]["risk"] == "Low (Uses standard imputation)"
    
    # Check AutoML parsing dynamically parsing 'Classification' task
    assert result["recommendations"][1]["action"] == "Train Classification Models"
    assert result["recommendations"][1]["risk"] == "High (Computationally expensive)"
    
    rec_path = "../../data/customer_churn_recommendations.json"
    assert os.path.exists(os.path.join(os.path.dirname(__file__), rec_path))
