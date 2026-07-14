import os
import json
import pytest
from core.services.knowledge_memory import KnowledgeMemory

@pytest.fixture
def memory_service(tmp_path):
    mem_dir = os.path.join(tmp_path, "memory")
    return KnowledgeMemory(base_dir=mem_dir)

def test_preferences(memory_service):
    memory_service.set_preference("theme", "dark")
    assert memory_service.get_preference("theme") == "dark"
    assert memory_service.get_preference("language", "en") == "en"

def test_workspace_context(memory_service):
    workspace = "default_ws"
    
    # Add dataset
    memory_service.add_dataset(workspace, "sales.csv", {"rows": 100})
    
    # Add EDA
    memory_service.update_eda(workspace, "sales.csv", "High correlation found")
    
    # Add Model
    memory_service.add_model(workspace, "sales.csv", {"type": "RandomForest", "r2": 0.95})
    
    # Add Chat
    memory_service.add_chat(workspace, "user", "What is the best model?")
    memory_service.add_chat(workspace, "assistant", "Random Forest is best.")
    
    # Add Report
    memory_service.add_report(workspace, "Q1 Executive Report")
    
    ctx = memory_service.get_workspace_context(workspace)
    
    assert "sales.csv" in ctx["datasets"]
    assert ctx["datasets"]["sales.csv"]["metadata"]["rows"] == 100
    assert ctx["datasets"]["sales.csv"]["eda_summary"] == "High correlation found"
    assert len(ctx["datasets"]["sales.csv"]["models"]) == 1
    assert ctx["datasets"]["sales.csv"]["models"][0]["type"] == "RandomForest"
    
    assert len(ctx["chats"]) == 2
    assert ctx["chats"][0]["role"] == "user"
    
    assert len(ctx["reports"]) == 1
    assert ctx["reports"][0] == "Q1 Executive Report"

def test_persistence(tmp_path):
    mem_dir = os.path.join(tmp_path, "memory")
    mem1 = KnowledgeMemory(base_dir=mem_dir)
    
    mem1.set_preference("mode", "expert")
    mem1.add_chat("ws_1", "user", "Hello memory")
    
    # Create new instance pointing to same dir to test loading
    mem2 = KnowledgeMemory(base_dir=mem_dir)
    
    assert mem2.get_preference("mode") == "expert"
    ctx = mem2.get_workspace_context("ws_1")
    assert len(ctx["chats"]) == 1
    assert ctx["chats"][0]["content"] == "Hello memory"
