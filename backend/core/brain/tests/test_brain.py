import pytest
from unittest.mock import Mock, MagicMock
from core.brain.brain import AgentixBrain
from core.brain.types import (
    PerceptionObject, UnderstandingObject, ReasoningObject,
    ExecutionPlan, DecisionObject, LearningRecord
)

@pytest.fixture
def mock_modules():
    return {
        'perception': MagicMock(),
        'understanding': MagicMock(),
        'reasoning': MagicMock(),
        'planning': MagicMock(),
        'decision': MagicMock(),
        'execution': MagicMock(),
        'learning': MagicMock()
    }

def test_brain_process_success(mock_modules):
    # Setup Mocks
    mock_perception_obj = PerceptionObject(user_goal="Test Goal", current_state="Init")
    mock_understanding_obj = UnderstandingObject(
        perception=mock_perception_obj, business_problem="Test", domain="Test",
        data_quality_assessment="Good", user_intent="Test"
    )
    from core.brain.deliberation.types import DeliberationResult, DeliberationRationale, RankedHypothesis, DeliberationHypothesis, HypothesisEvaluation, ConfidenceScore
    mock_deliberation_result = DeliberationResult(
        questions=[], hypotheses=[], evidence_summary={}, alternatives=[],
        chosen_hypothesis=RankedHypothesis(
            hypothesis=DeliberationHypothesis(id="1", question_id="1", description="Test", expected_outcome="Test", required_evidence=[]),
            evaluation=HypothesisEvaluation(hypothesis_id="1", advantages=[], disadvantages=[], execution_cost=0, estimated_time_sec=0, memory_impact="Low", risk_level="Low", privacy_impact="None", llm_usage_required=False),
            confidence=ConfidenceScore(hypothesis_id="1", score=100.0, reason="Test", supporting_evidence_keys=[]),
            rank=1
        ),
        rationale=DeliberationRationale(decision_summary="Test", reason="Test", evidence_summary="Test", confidence_score=100.0, expected_outcome="Test"),
        risk_assessment="Low", recommended_next_action="Test", estimated_cost=0, estimated_time=0
    )
    mock_reasoning_obj = ReasoningObject(
        deliberation=mock_deliberation_result, what_should_happen=[], what_should_not_happen=[],
        reusable_knowledge_keys=[], required_engines=[], required_agents=[], can_use_deterministic_computation=True
    )
    mock_plan = ExecutionPlan(plan_id="1", steps=[], total_estimated_time_sec=0, total_estimated_cost=0.0)
    mock_decision_obj = DecisionObject(
        reasoning=mock_reasoning_obj, chosen_plan=mock_plan, best_engine="Test",
        best_agent="Test", best_model="Test", best_workflow="Test"
    )
    
    mock_modules['perception'].observe.return_value = mock_perception_obj
    mock_modules['understanding'].interpret.return_value = mock_understanding_obj
    mock_modules['reasoning'].reason.return_value = mock_reasoning_obj
    mock_modules['planning'].plan.return_value = mock_plan
    mock_modules['decision'].decide.return_value = mock_decision_obj
    mock_modules['execution'].execute.return_value = {"output": "success"}

    # Initialize Brain
    brain = AgentixBrain(
        perception=mock_modules['perception'],
        understanding=mock_modules['understanding'],
        reasoning=mock_modules['reasoning'],
        planning=mock_modules['planning'],
        decision=mock_modules['decision'],
        execution=mock_modules['execution'],
        learning=mock_modules['learning']
    )

    # Override the internal deliberation controller for this test
    mock_deliberation_controller = MagicMock()
    mock_deliberation_controller.deliberate.return_value = mock_deliberation_result
    brain._deliberation = mock_deliberation_controller

    # Execute
    raw_input = {"input": "do something"}
    result = brain.process(raw_input)

    # Assertions
    assert result["status"] == "success"
    assert result["final_state"] == "LEARNING"
    assert result["result"] == {"output": "success"}

    # Verify chain of calls
    mock_modules['perception'].observe.assert_called_once_with(raw_input)
    mock_modules['understanding'].interpret.assert_called_once_with(mock_perception_obj)
    # Note: we bypass testing the internal deliberation controller call here 
    # since we would mock it, but we assert reasoning gets called.
    mock_modules['reasoning'].reason.assert_called_once()
    mock_modules['planning'].plan.assert_called_once_with(mock_reasoning_obj)
    mock_modules['decision'].decide.assert_called_once_with([mock_plan], mock_reasoning_obj)
    mock_modules['execution'].execute.assert_called_once_with(mock_decision_obj)
    mock_modules['learning'].record_outcome.assert_called_once_with(mock_decision_obj, {"output": "success"})

def test_brain_process_failure_in_reasoning(mock_modules):
    # Setup Mocks to fail during Reasoning
    mock_modules['reasoning'].reason.side_effect = ValueError("Reasoning Engine Failed")
    
    # We must also mock the deliberation output so it doesn't crash on mocked understanding
    from core.brain.deliberation.types import DeliberationResult
    mock_modules['deliberation'] = MagicMock()
    mock_modules['deliberation'].deliberate.return_value = MagicMock(spec=DeliberationResult)

    # Initialize Brain
    brain = AgentixBrain(
        perception=mock_modules['perception'],
        understanding=mock_modules['understanding'],
        reasoning=mock_modules['reasoning'],
        planning=mock_modules['planning'],
        decision=mock_modules['decision'],
        execution=mock_modules['execution'],
        learning=mock_modules['learning']
    )
    # Override the internal deliberation controller for this test
    brain._deliberation = mock_modules['deliberation']

    # Execute
    result = brain.process({"input": "test"})

    # Assertions
    assert result["status"] == "error"
    assert result["phase_failed"] == "REASONING"
    assert "Reasoning Engine Failed" in result["error"]
    
    # Ensure downstream wasn't called
    mock_modules['planning'].plan.assert_not_called()
    mock_modules['execution'].execute.assert_not_called()

def test_brain_optimize_procedural_memory(mock_modules):
    brain = AgentixBrain(
        perception=mock_modules['perception'],
        understanding=mock_modules['understanding'],
        reasoning=mock_modules['reasoning'],
        planning=mock_modules['planning'],
        decision=mock_modules['decision'],
        execution=mock_modules['execution'],
        learning=mock_modules['learning']
    )
    
    mock_episodic = MagicMock()
    mock_episodic.store.get_all.return_value = ['ep1', 'ep2']
    
    mock_miner = MagicMock()
    mock_miner.mine_strategies.return_value = ['cand1']
    
    mock_builder = MagicMock()
    mock_builder.build_from_candidate.return_value = 'strategy1'
    
    brain.set_episodic_memory(mock_episodic)
    brain.set_procedural_memory(
        strategy_repo=MagicMock(), recommender=MagicMock(),
        learner=MagicMock(), miner=mock_miner, builder=mock_builder
    )
    
    strategies = brain.optimize_procedural_memory()
    
    assert len(strategies) == 1
    assert strategies[0] == 'strategy1'
    mock_episodic.store.get_all.assert_called_once()
    mock_miner.mine_strategies.assert_called_once_with(['ep1', 'ep2'])
    mock_builder.build_from_candidate.assert_called_once_with('cand1')
