import pytest
from core.services.reasoning_engine import ReasoningEngine

def test_reasoning_engine_metadata_only():
    engine = ReasoningEngine()
    
    # 1. User: "How many missing values are there?"
    # Should run only up to Metadata Agent. 
    # But Metadata depends on Dataset. If we mock cache:
    cached_agents = {"Dataset"}
    result = engine.process_request("How many missing values are there?", cached_agents)
    
    plan = result["execution_plan"]["agents"]
    assert "Metadata" in plan
    assert "Cleaning" not in plan
    assert "AutoML" not in plan
    assert "EDA" not in plan
    assert result["target_agent"] == "Metadata"

def test_reasoning_engine_train_model():
    engine = ReasoningEngine()
    
    # 2. User: "Train the best model."
    cached_agents = {"Dataset"}
    result = engine.process_request("Train the best model.", cached_agents)
    
    plan = result["execution_plan"]["agents"]
    assert "Cleaning" in plan
    assert "Feature Engineering" in plan
    assert "AutoML" in plan
    assert result["target_agent"] == "AutoML"
    assert "Report" not in plan

def test_reasoning_engine_executive_report():
    engine = ReasoningEngine()
    
    # 3. User: "Generate executive report."
    cached_agents = {"Dataset"}
    result = engine.process_request("Generate executive report.", cached_agents)
    
    plan = result["execution_plan"]["agents"]
    assert "EDA" in plan
    assert "AutoML" in plan
    assert "Context Builder" in plan
    assert "Report" in plan
    assert result["target_agent"] == "Report"

def test_reasoning_engine_cache_skipping():
    engine = ReasoningEngine()
    
    # Everything up to Feature Engineering is cached
    cached_agents = {"Dataset", "Metadata", "Cleaning", "Feature Engineering"}
    result = engine.process_request("Evaluate and explain the results", cached_agents)
    
    plan = result["execution_plan"]["agents"]
    assert "AutoML" in plan
    assert "Explainability" in plan
    assert "Cleaning" not in plan # Must be skipped due to cache
