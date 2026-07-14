import pytest
from core.memory.episodic.types import DatasetFingerprint, Episode, ExecutionMetrics
from core.memory.episodic.episode_store import InMemoryEpisodeStore
from core.memory.episodic.episode_index import InMemoryEpisodeIndex
from core.memory.episodic.episode_similarity import StructuralSimilarityEngine
from core.memory.episodic.episode_retriever import DefaultEpisodeRetriever
from core.memory.episodic.episode_validator import DefaultEpisodeValidator
from core.memory.episodic.episode_scorer import DefaultEpisodeScorer
from core.memory.episodic.episode_writer import DefaultEpisodeWriter
from core.memory.episodic.memory_controller import EpisodicMemoryController

@pytest.fixture
def memory_controller():
    store = InMemoryEpisodeStore()
    index = InMemoryEpisodeIndex()
    similarity = StructuralSimilarityEngine()
    retriever = DefaultEpisodeRetriever(store, index, similarity)
    validator = DefaultEpisodeValidator()
    scorer = DefaultEpisodeScorer()
    writer = DefaultEpisodeWriter(validator, store, index)
    
    return EpisodicMemoryController(store, index, similarity, retriever, writer, validator, scorer)

def create_raw_episode(domain: str, intent: str, columns: list, time_sec: int, success: float) -> dict:
    return {
        "user_id": "test_user",
        "workspace_id": "ws_1",
        "dataset_id": "ds_1",
        "dataset_fingerprint": {
            "columns": columns,
            "column_types": {c: "str" for c in columns},
            "missing_value_ratio": 0.0,
            "dataset_shape": [1000, len(columns)],
            "business_domain": domain,
            "target_variable": columns[-1] if columns else None
        },
        "dataset_profile": {},
        "business_domain": domain,
        "user_goal": f"Solve {intent} for {domain}",
        "detected_intent": intent,
        "questions_generated": ["Is this classification?"],
        "hypotheses_generated": ["Use random forest"],
        "evidence_summary": {},
        "chosen_hypothesis": "1",
        "confidence_score": 80.0,
        "workflow_plan": [{"step": "train"}],
        "engines_used": ["PythonEngine"],
        "llms_used": [],
        "capabilities_used": [],
        "execution_metrics": {
            "execution_time_sec": time_sec,
            "memory_usage_mb": 100.0,
            "success_score": success
        },
        "privacy_flags": ["Low"],
        "outcome": "SUCCESS" if success > 50 else "FAILED"
    }

def test_record_experience_and_privacy(memory_controller):
    raw_data = create_raw_episode("Healthcare", "predict patient risk", ["age", "bp", "risk"], 10, 95.0)
    # add sensitive raw data to test validator
    raw_data["raw_data"] = "patient_name=john"
    
    with pytest.raises(ValueError):
        memory_controller.record_experience(raw_data)
        
    # remove raw data
    del raw_data["raw_data"]
    episode = memory_controller.record_experience(raw_data)
    assert episode.business_domain == "Healthcare"

def test_similarity_search_and_reuse(memory_controller):
    # Seed 1: Healthcare classification, successful
    memory_controller.record_experience(create_raw_episode("Healthcare", "classify disease", ["age", "disease"], 10, 95.0))
    # Seed 2: Retail regression, failed
    memory_controller.record_experience(create_raw_episode("Retail", "forecast sales", ["date", "sales"], 120, 40.0))
    # Seed 3: Retail classification, successful
    memory_controller.record_experience(create_raw_episode("Retail", "classify churn", ["visits", "churn"], 5, 90.0))
    
    # Query: new retail dataset for classification
    fingerprint = DatasetFingerprint(
        columns=["visits", "churn"], column_types={"visits": "int", "churn": "int"},
        missing_value_ratio=0.0, dataset_shape=[500, 2], business_domain="Retail", target_variable="churn"
    )
    
    recommendations = memory_controller.recall_experiences(fingerprint, "classify churn")
    
    assert len(recommendations) > 0
    top_rec = recommendations[0]
    
    # It should match Seed 3 (Retail classification, high success)
    assert top_rec.episode.business_domain == "Retail"
    assert top_rec.episode.detected_intent == "classify churn"
    assert top_rec.similarity_score > 0.5
    assert "successful" in top_rec.adaptation_reasoning.lower()
