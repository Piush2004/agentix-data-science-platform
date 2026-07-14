import os
import json
import pytest
from core.services.context_builder import ContextBuilder, PromptBuilder

@pytest.fixture
def mock_workspace(tmp_path):
    dataset_name = "test_data.csv"
    ds_name, _ = os.path.splitext(dataset_name)
    workspace_dir = os.path.join(tmp_path, ds_name)
    os.makedirs(workspace_dir)
    
    metadata = {
        "Rows": 1000,
        "Columns": 10,
        "Target column": "is_fraud",
        "Null count": {"col1": 50, "col2": 50}
    }
    
    statistics = {
        "Correlation matrix": {
            "col1": {"col1": 1.0, "col2": 0.85},
            "col2": {"col1": 0.85, "col2": 1.0}
        }
    }
    
    privacy = {
        "risk_score": 45,
        "columns_containing_pii": {"user_email": "email", "phone": "phone"}
    }
    
    with open(os.path.join(workspace_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f)
    with open(os.path.join(workspace_dir, "statistics.json"), "w") as f:
        json.dump(statistics, f)
    with open(os.path.join(workspace_dir, "privacy_report.json"), "w") as f:
        json.dump(privacy, f)
        
    return str(tmp_path), dataset_name

def test_context_builder(mock_workspace, monkeypatch):
    workspace_path, dataset_name = mock_workspace
    
    cb = ContextBuilder()
    monkeypatch.setattr(cb, "workspace_base", workspace_path)
    
    eda = {"Data Distribution": "Normal"}
    metrics = {"accuracy": 0.95, "feature_importance": {"col1": 0.6, "col2": 0.4}}
    question = "What is the accuracy?"
    
    context = cb.build_context(dataset_name, eda, metrics, question)
    
    # Assert base context elements
    assert "Dataset: test_data.csv" in context
    assert "Shape: 1000 rows, 10 columns" in context
    assert "Target: is_fraud" in context
    assert "Missing Data: 1.0%" in context # 100 missing / (1000*10) = 0.01 = 1.0%
    assert "Privacy Risk Score: 45/100" in context
    assert "Masked PII Columns: user_email, phone" in context
    assert "col1 & col2: 0.85" in context
    
    # Assert dynamic context elements
    assert "EDA Insights:" in context
    assert "Data Distribution: Normal" in context
    assert "Model Metrics:" in context
    assert "Performance (Accuracy/R2): 0.95" in context
    assert "Top Features: col1 (0.60), col2 (0.40)" in context
    
    # Assert question appended
    assert "User Question: What is the accuracy?" in context
    
    # Assert cache is populated
    assert cb.cache.get(dataset_name) is not None

def test_prompt_builder(mock_workspace, monkeypatch):
    workspace_path, dataset_name = mock_workspace
    
    pb = PromptBuilder()
    monkeypatch.setattr(pb.context_builder, "workspace_base", workspace_path)
    
    prompt = pb.build_prompt(dataset_name, "Hello")
    
    assert "You are a Data Intelligence Assistant." in prompt
    assert "NEVER request raw row data." in prompt
    assert "Dataset: test_data.csv" in prompt
    assert "User Question: Hello" in prompt
