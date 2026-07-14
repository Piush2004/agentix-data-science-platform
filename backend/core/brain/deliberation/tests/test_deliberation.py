import pytest
from core.brain.deliberation.deliberation_controller import DeliberationController
from core.brain.types import UnderstandingObject, PerceptionObject

@pytest.fixture
def controller():
    return DeliberationController()

def create_understanding(intent: str, missing: int, dupes: int, pii: bool, size: int) -> UnderstandingObject:
    return UnderstandingObject(
        perception=PerceptionObject(
            user_goal=intent,
            current_state="test",
            dataset_metadata={
                "missing_values": missing,
                "duplicates": dupes,
                "has_pii": pii,
                "size_bytes": size,
                "rows": 1000
            }
        ),
        business_problem="Solve problem",
        domain="General",
        data_quality_assessment="Poor" if missing > 0 else "Good",
        user_intent=intent
    )

def test_deliberation_perfect_small_dataset(controller):
    und = create_understanding(intent="predict sales", missing=0, dupes=0, pii=False, size=1024*10)
    result = controller.deliberate(und)
    
    assert result.chosen_hypothesis.confidence.score >= 50
    # Make sure 'unnecessary' cleaning hypothesis was generated
    assert any("unnecessary" in h.description.lower() for h in result.hypotheses)
    assert result.risk_assessment == "Low"

def test_deliberation_poor_quality_large_dataset(controller):
    und = create_understanding(intent="forecast revenue", missing=500, dupes=100, pii=False, size=1024*1024*200) # 200MB
    result = controller.deliberate(und)
    
    # Needs cleaning
    cleaning_hyps = [h for h in result.alternatives if "required" in h.hypothesis.description.lower()]
    assert len(cleaning_hyps) > 0
    # Memory impact should be High because it's > 100MB
    assert any(h.evaluation.memory_impact == "High" for h in cleaning_hyps)

def test_deliberation_pii_present(controller):
    und = create_understanding(intent="extract insights using llm", missing=0, dupes=0, pii=True, size=1024)
    result = controller.deliberate(und)
    
    # If it uses LLM, privacy risk should be high
    for alt in result.alternatives:
        if alt.evaluation.llm_usage_required:
            assert alt.evaluation.risk_level == "High"
            assert alt.evaluation.privacy_impact == "High"

def test_deliberation_deterministic_classification(controller):
    und = create_understanding(intent="classify users", missing=0, dupes=0, pii=False, size=1024*1024)
    result = controller.deliberate(und)
    
    # Should penalize LLM for classification math
    for alt in result.alternatives:
        if alt.evaluation.llm_usage_required:
            assert alt.confidence.score < 50
        else:
            assert alt.confidence.score > 50
