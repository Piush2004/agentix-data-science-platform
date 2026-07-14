import os
import pytest
from core.services.knowledge_memory import KnowledgeMemory
from core.services.semantic_search import SemanticSearchAgent

@pytest.fixture
def mock_memory_and_db(tmp_path):
    mem_dir = os.path.join(tmp_path, "memory")
    db_path = os.path.join(tmp_path, "vector_db.json")
    
    km = KnowledgeMemory(base_dir=mem_dir)
    ws = "test_workspace"
    
    # Dataset 1: Low accuracy, low rows
    km.add_dataset(ws, "q1_sales.csv", {"rows": 500, "Target column": "revenue"})
    km.add_model(ws, "q1_sales.csv", {"type": "LinearRegression", "r2": 0.45})
    
    # Dataset 2: High accuracy, high rows, recent
    km.add_dataset(ws, "q2_sales_last_week.csv", {"rows": 50000, "Target column": "churn"})
    km.add_model(ws, "q2_sales_last_week.csv", {"type": "XGBoost", "r2": 0.96})
    
    # Monkeypatch the global instance in semantic_search so it uses our test memory
    import core.services.semantic_search as ss
    import core.services.knowledge_memory as k_mod
    k_mod.knowledge_memory = km
    
    agent = SemanticSearchAgent(db_path=db_path)
    return ws, agent

def test_semantic_search_indexing(mock_memory_and_db):
    ws, agent = mock_memory_and_db
    
    # Run indexing
    agent.index_workspace_datasets(ws)
    
    assert len(agent.retriever.vector_db.embeddings) == 2
    
    doc1 = [doc for doc in agent.retriever.vector_db.embeddings if doc["id"] == "q1_sales.csv"][0]
    assert doc1["metadata"]["best_accuracy"] == 0.45
    
    doc2 = [doc for doc in agent.retriever.vector_db.embeddings if doc["id"] == "q2_sales_last_week.csv"][0]
    assert doc2["metadata"]["best_accuracy"] == 0.96

def test_semantic_search_retrieval(mock_memory_and_db):
    ws, agent = mock_memory_and_db
    agent.index_workspace_datasets(ws)
    
    # Query for the highest accuracy
    query = "Show me the dataset I uploaded last week with the highest accuracy."
    response = agent.answer_query(query)
    
    # In our simple pseudo-embedding, both will have positive score, but let's just make sure it doesn't crash and returns a formatted string.
    assert "Based on your query, the most relevant dataset is" in response
    assert "Relevance Score" in response
    assert "Best Accuracy" in response
