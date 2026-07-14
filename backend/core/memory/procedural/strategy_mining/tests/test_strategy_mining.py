import pytest
from core.memory.episodic.types import Episode, DatasetFingerprint, ExecutionMetrics
from core.memory.procedural.strategy_mining.strategy_miner import StrategyMiner

@pytest.fixture
def miner():
    return StrategyMiner()

def create_episode(ep_id: str, domain: str, intent: str, target: str, steps: list, engines: list, success: float) -> Episode:
    return Episode(
        episode_id=ep_id,
        user_id="u1",
        workspace_id="w1",
        dataset_id="d1",
        dataset_fingerprint=DatasetFingerprint(
            columns=["col1", "col2", target],
            column_types={"col1": "int", "col2": "int", target: "float"},
            missing_value_ratio=0.0,
            dataset_shape=[100, 3],
            business_domain=domain,
            target_variable=target
        ),
        dataset_profile={},
        business_domain=domain,
        user_goal=f"Test {intent}",
        detected_intent=intent,
        questions_generated=[],
        hypotheses_generated=[],
        evidence_summary={},
        chosen_hypothesis="h1",
        confidence_score=80.0,
        workflow_plan=[{"step": s} for s in steps],
        engines_used=engines,
        llms_used=[],
        capabilities_used=[],
        execution_metrics=ExecutionMetrics(execution_time_sec=10, memory_usage_mb=50.0, success_score=success),
        privacy_flags=[],
        outcome="SUCCESS" if success > 50 else "FAILED",
        lessons_learned=[]
    )

def test_mine_strategies_from_recurring_patterns(miner):
    episodes = [
        create_episode("1", "Retail", "forecast", "sales", ["clean", "train"], ["PythonEngine"], 95.0),
        create_episode("2", "Retail", "forecast", "sales", ["clean", "train"], ["PythonEngine"], 90.0),
        create_episode("3", "Retail", "forecast", "sales", ["train"], ["PythonEngine"], 40.0), # different pattern, failed
        create_episode("4", "Healthcare", "classify", "disease", ["clean", "train"], ["PythonEngine"], 99.0) # different cluster
    ]
    
    candidates = miner.mine_strategies(episodes)
    
    # We should only find a candidate for Retail-forecast-sales since Healthcare is isolated (1 episode)
    assert len(candidates) == 1
    candidate = candidates[0]
    
    assert candidate.cluster_key.business_domain == "retail"
    assert candidate.cluster_key.detected_intent == "forecast"
    assert candidate.cluster_key.target_variable == "sales"
    assert candidate.pattern.workflow_steps == ["clean", "train"]
    assert candidate.pattern.engines_used == ["PythonEngine"]
    
    # Frequency: 2 out of 3 retail episodes = 66.6%
    assert abs(candidate.frequency - 66.6) < 1.0
    # Average success for this pattern: (95+90)/2 = 92.5
    assert candidate.average_success == 92.5
    assert candidate.confidence > 50.0
