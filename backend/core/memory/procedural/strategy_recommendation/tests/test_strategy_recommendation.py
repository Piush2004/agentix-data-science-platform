import pytest
from core.memory.episodic.types import DatasetFingerprint, EpisodeRecommendation, Episode, ExecutionMetrics
from core.memory.procedural.strategy_builder.types import ProceduralStrategy, StrategyConditions
from core.memory.procedural.strategy_recommendation.types import RecommendationAction
from core.memory.procedural.strategy_recommendation.strategy_recommender import DeterministicStrategyRecommender

@pytest.fixture
def recommender():
    return DeterministicStrategyRecommender()

def create_fingerprint(columns: list, target: str = None) -> DatasetFingerprint:
    return DatasetFingerprint(
        columns=columns,
        column_types={c: "int" for c in columns},
        missing_value_ratio=0.0,
        dataset_shape=[100, len(columns)],
        business_domain="retail",
        target_variable=target
    )

def create_strategy(requires_target: bool, required_cols: list) -> ProceduralStrategy:
    return ProceduralStrategy(
        domain="retail",
        intent="forecast",
        conditions=StrategyConditions(
            target_variable_required=requires_target,
            required_columns=required_cols,
            dataset_shape_constraints={}
        ),
        workflow=["clean", "train"],
        capabilities=[],
        expected_outcome="",
        success_rate=95.0,
        failure_rate=5.0,
        confidence=90.0,
        is_active=True,
        source_candidate_id="c1"
    )

def test_recommend_ignore_when_no_strategy(recommender):
    fp = create_fingerprint(["a", "b"])
    rec = recommender.recommend(fp, "forecast", None, [])
    assert rec.action == RecommendationAction.IGNORE
    assert "No active strategy" in rec.reasoning

def test_recommend_reuse_when_perfect_match(recommender):
    fp = create_fingerprint(["sales", "date"], target="sales")
    strategy = create_strategy(requires_target=True, required_cols=["date"])
    
    rec = recommender.recommend(fp, "forecast", strategy, [])
    assert rec.action == RecommendationAction.REUSE
    assert len(rec.suggested_modifications) == 0

def test_recommend_modify_when_target_missing(recommender):
    fp = create_fingerprint(["sales", "date"], target=None)
    strategy = create_strategy(requires_target=True, required_cols=["date"])
    
    rec = recommender.recommend(fp, "forecast", strategy, [])
    assert rec.action == RecommendationAction.MODIFY
    assert any("target" in mod.lower() for mod in rec.suggested_modifications)

def test_recommend_modify_when_recent_failure(recommender):
    fp = create_fingerprint(["sales", "date"], target="sales")
    strategy = create_strategy(requires_target=True, required_cols=["date"])
    
    # Create an episode that used the same workflow but failed
    ep = Episode(
        user_id="u1", workspace_id="w1", dataset_id="d1",
        dataset_fingerprint=fp, dataset_profile={}, business_domain="retail",
        user_goal="forecast", detected_intent="forecast", questions_generated=[], hypotheses_generated=[],
        evidence_summary={}, chosen_hypothesis="h1", confidence_score=50.0,
        workflow_plan=[{"step": "clean"}, {"step": "train"}], # matches strategy workflow
        engines_used=[], llms_used=[], capabilities_used=[],
        execution_metrics=ExecutionMetrics(execution_time_sec=10, memory_usage_mb=10, success_score=20.0), # < 50
        privacy_flags=[], outcome="FAILED", lessons_learned=[]
    )
    ep_rec = EpisodeRecommendation(episode=ep, similarity_score=0.9, recommended_workflow=[], adaptation_reasoning="")
    
    rec = recommender.recommend(fp, "forecast", strategy, [ep_rec])
    assert rec.action == RecommendationAction.MODIFY
    assert any("failed" in mod.lower() for mod in rec.suggested_modifications)
