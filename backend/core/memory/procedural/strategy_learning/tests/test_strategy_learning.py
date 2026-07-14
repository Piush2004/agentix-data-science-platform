import pytest
from core.memory.episodic.types import Episode, ExecutionMetrics, DatasetFingerprint
from core.memory.procedural.strategy_builder.types import ProceduralStrategy, StrategyConditions
from core.memory.procedural.strategy_builder.strategy_repository import InMemoryStrategyRepository
from core.memory.procedural.strategy_learning.types import EvolutionStatus
from core.memory.procedural.strategy_learning.strategy_learner import DeterministicStrategyLearner

@pytest.fixture
def repo():
    return InMemoryStrategyRepository()

@pytest.fixture
def learner():
    return DeterministicStrategyLearner()

def create_strategy(success: float, conf: float, count: int, version: int = 1) -> ProceduralStrategy:
    return ProceduralStrategy(
        strategy_id="s1",
        domain="retail",
        intent="forecast",
        conditions=StrategyConditions(target_variable_required=True, required_columns=[], dataset_shape_constraints={}),
        workflow=["clean", "train"],
        capabilities=[],
        expected_outcome="",
        success_rate=success,
        failure_rate=100.0-success,
        confidence=conf,
        usage_count=count,
        average_execution_time=10.0,
        is_active=True,
        version=version,
        source_candidate_id="c1"
    )

def create_episode(success_score: float, time_sec: float) -> Episode:
    fp = DatasetFingerprint(
        columns=["a"], column_types={"a": "int"}, missing_value_ratio=0.0,
        dataset_shape=[1,1], business_domain="retail", target_variable=None
    )
    return Episode(
        episode_id="e1",
        user_id="u1", workspace_id="w1", dataset_id="d1", dataset_fingerprint=fp, dataset_profile={},
        business_domain="retail", user_goal="forecast", detected_intent="forecast", questions_generated=[],
        hypotheses_generated=[], evidence_summary={}, chosen_hypothesis="h1", confidence_score=90.0,
        workflow_plan=[], engines_used=[], llms_used=[], capabilities_used=[],
        execution_metrics=ExecutionMetrics(execution_time_sec=time_sec, memory_usage_mb=10, success_score=success_score),
        privacy_flags=[], outcome="SUCCESS" if success_score > 50 else "FAILED", lessons_learned=[]
    )

def test_learn_maintain(learner, repo):
    strategy = create_strategy(success=80.0, conf=80.0, count=2)
    episode = create_episode(success_score=80.0, time_sec=10.0)
    
    updated, report = learner.learn_from_episode(strategy, episode, repo)
    
    assert updated.version == 2
    assert updated.usage_count == 3
    assert updated.success_rate == 80.0
    assert report.status == EvolutionStatus.MAINTAINED
    assert updated.is_active is True

def test_learn_promote(learner, repo):
    strategy = create_strategy(success=95.0, conf=90.0, count=4)
    episode = create_episode(success_score=100.0, time_sec=10.0) # pushes count to 5
    
    updated, report = learner.learn_from_episode(strategy, episode, repo)
    
    assert updated.usage_count == 5
    assert updated.success_rate > 90.0
    assert report.status == EvolutionStatus.PROMOTED

def test_learn_retire_due_to_failure(learner, repo):
    strategy = create_strategy(success=60.0, conf=70.0, count=2)
    episode = create_episode(success_score=10.0, time_sec=10.0)
    
    updated, report = learner.learn_from_episode(strategy, episode, repo)
    
    # New avg: (60*2 + 10)/3 = 43.33 -> < 50, so retires
    assert updated.success_rate < 50.0
    assert report.status == EvolutionStatus.RETIRED
    assert updated.is_active is False
