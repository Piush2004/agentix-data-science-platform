import pytest
from core.memory.procedural.strategy_mining.types import StrategyCandidate, EpisodeClusterKey, ExecutionPattern
from core.memory.procedural.strategy_builder.strategy_builder import StrategyBuilderFacade

@pytest.fixture
def builder():
    return StrategyBuilderFacade()

def create_candidate(success_rate: float, confidence: float, workflow_steps: list = None) -> StrategyCandidate:
    workflow_steps = workflow_steps or ["clean", "train"]
    return StrategyCandidate(
        candidate_id="c1",
        cluster_key=EpisodeClusterKey(business_domain="retail", detected_intent="forecast", target_variable="sales"),
        pattern=ExecutionPattern(pattern_hash="hash1", workflow_steps=workflow_steps, engines_used=["PythonEngine"]),
        supporting_episode_ids=["ep1", "ep2", "ep3", "ep4", "ep5"],
        frequency=100.0,
        average_success=success_rate,
        confidence=confidence
    )

def test_build_successful_strategy_with_versioning(builder):
    # Initial build
    candidate1 = create_candidate(success_rate=95.0, confidence=80.0)
    strategy1 = builder.build_from_candidate(candidate1)
    
    assert strategy1 is not None
    assert strategy1.version == 1
    assert strategy1.is_active is True
    assert strategy1.domain == "retail"
    
    # Second build from same logical context (causes version bump)
    # Using a different workflow to avoid duplicate rejection
    candidate2 = create_candidate(success_rate=98.0, confidence=85.0, workflow_steps=["clean", "train", "eval"])
    strategy2 = builder.build_from_candidate(candidate2)
    
    assert strategy2 is not None
    assert strategy2.version == 2
    assert strategy2.success_rate == 98.0
    
    # Verify history
    history = builder.repository.get_history("retail", "forecast")
    assert len(history) == 2
    
    latest = builder.repository.get_latest_version("retail", "forecast")
    assert latest.version == 2

def test_reject_low_confidence_strategy(builder):
    # Fails validation
    candidate = create_candidate(success_rate=40.0, confidence=30.0)
    strategy = builder.build_from_candidate(candidate)
    
    assert strategy is None
