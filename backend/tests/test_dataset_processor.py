import os
import json
import pandas as pd
import numpy as np
import pytest
from core.services.dataset_processor import dataset_processor

def test_process_dataset(tmp_path, monkeypatch):
    # Patch workspace base to use tmp_path
    monkeypatch.setattr(dataset_processor, "workspace_base", str(tmp_path))
    
    # Create sample dataframe
    df = pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "Alice", "Eve"],
        "score": [85.5, 90.0, np.nan, 88.0, 92.5],
        "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"])
    })
    
    # Process dataset
    metadata, statistics, profile, privacy_report, df_masked = dataset_processor.process_dataset("test_dataset.csv", df)
    
    # Assert metadata
    assert metadata["Rows"] == 5
    assert metadata["Columns"] == 4
    assert metadata["Null count"]["score"] == 1
    assert "id" in metadata["Numeric columns"]
    assert "name" in metadata["Categorical columns"]
    assert "date" in metadata["Datetime columns"]
    assert metadata["Duplicate count"] == 0
    assert metadata["Unique values"]["name"] == 4
    
    # Assert statistics
    assert "score" in statistics
    assert statistics["score"]["Mean"] is not None
    assert statistics["score"]["Min"] == 85.5
    assert statistics["score"]["Max"] == 92.5
    assert "Distribution summary" in statistics
    
    # Assert profile
    assert profile["dataset_name"] == "test_dataset.csv"
    assert "metadata_summary" in profile
    assert "statistics_summary" in profile
    
    # Assert files are created
    workspace_dir = os.path.join(str(tmp_path), "test_dataset")
    assert os.path.exists(os.path.join(workspace_dir, "metadata.json"))
    assert os.path.exists(os.path.join(workspace_dir, "statistics.json"))
    assert os.path.exists(os.path.join(workspace_dir, "profile.json"))

def test_empty_dataset():
    df = pd.DataFrame()
    with pytest.raises(ValueError, match="Dataset is empty."):
        dataset_processor.process_dataset("empty.csv", df)
