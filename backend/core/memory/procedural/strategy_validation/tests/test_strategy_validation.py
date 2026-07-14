import pytest
from core.memory.procedural.strategy_mining.types import StrategyCandidate, EpisodeClusterKey, ExecutionPattern
from core.memory.procedural.strategy_builder.types import ProceduralStrategy, StrategyConditions
from core.memory.procedural.strategy_validation.types import ValidationStatus
from core.memory.procedural.strategy_validation.strategy_validator import DeterministicStrategyValidator

@pytest.fixture
def validator():
    return DeterministicStrategyValidator(min_episodes=3, min_success_rate=70.0, min_confidence=60.0)

def create_candidate(success_rate: float, confidence: float, num_episodes: int = 5) -> StrategyCandidate:
    return StrategyCandidate(
        candidate_id="c1",
        cluster_key=EpisodeClusterKey(business_domain="retail", detected_intent="forecast", target_variable="sales"),
        pattern=ExecutionPattern(pattern_hash="hash1", workflow_steps=["clean", "train"], engines_used=["PythonEngine"]),
        supporting_episode_ids=[f"ep{i}" for i in range(num_episodes)],
        frequency=100.0,
        average_success=success_rate,
        confidence=confidence
    )

def create_strategy(domain: str, intent: str, success: float, workflow: list) -> ProceduralStrategy:
    return ProceduralStrategy(
        domain=domain,
        intent=intent,
        conditions=StrategyConditions(target_variable_required=True, required_columns=[], dataset_shape_constraints={}),
        workflow=workflow,
        capabilities=["PythonEngine"],
        expected_outcome="Success",
        success_rate=success,
        failure_rate=100.0-success,
        confidence=90.0,
        is_active=True,
        source_candidate_id="c_old"
    )

def test_validation_approved(validator):
    candidate = create_candidate(90.0, 80.0, 5)
    report = validator.validate_candidate(candidate, [])
    assert report.status == ValidationStatus.APPROVED
    assert len(report.reasons) == 0

def test_validation_requires_more_data(validator):
    candidate = create_candidate(90.0, 80.0, 2)
    report = validator.validate_candidate(candidate, [])
    assert report.status == ValidationStatus.REQUIRES_MORE_DATA
    assert "Requires more data" in report.reasons[0]

def test_validation_weak(validator):
    candidate = create_candidate(65.0, 80.0, 5)
    report = validator.validate_candidate(candidate, [])
    assert report.status == ValidationStatus.REJECTED
    assert any("Weak" in r for r in report.reasons)

def test_validation_conflicting(validator):
    candidate = create_candidate(75.0, 80.0, 5)
    # Existing strategy has much higher success
    existing = create_strategy("retail", "forecast", 95.0, ["train_only"])
    report = validator.validate_candidate(candidate, [existing])
    assert report.status == ValidationStatus.REJECTED
    assert any("Conflicting" in r for r in report.reasons)

def test_validation_duplicate(validator):
    candidate = create_candidate(90.0, 80.0, 5)
    # Existing strategy has exact same workflow
    existing = create_strategy("retail", "forecast", 88.0, ["clean", "train"])
    report = validator.validate_candidate(candidate, [existing])
    assert report.status == ValidationStatus.REJECTED
    assert any("Duplicate" in r for r in report.reasons)
