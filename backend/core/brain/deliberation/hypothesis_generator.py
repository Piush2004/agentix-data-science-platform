import uuid
from typing import List
from core.brain.deliberation.interfaces import IHypothesisGenerator
from core.brain.deliberation.types import DeliberationQuestion, DeliberationEvidence, DeliberationHypothesis

class DefaultHypothesisGenerator(IHypothesisGenerator):
    def generate(self, questions: List[DeliberationQuestion], evidence: List[DeliberationEvidence]) -> List[DeliberationHypothesis]:
        hypotheses = []
        
        # Analyze evidence to inform hypotheses
        meta_ev = next((e.data for e in evidence if e.source == "DatasetMetadata"), {})
        has_missing = meta_ev.get("missing_values_count", 0) > 0
        has_dupes = meta_ev.get("duplicate_rows", 0) > 0
        
        for q in questions:
            if "cleaning" in q.text.lower() or "clean" in q.text.lower():
                if has_missing or has_dupes:
                    hypotheses.append(DeliberationHypothesis(
                        id=str(uuid.uuid4()),
                        question_id=q.id,
                        description="Cleaning is strictly required due to missing values or duplicates.",
                        expected_outcome="Dataset becomes ready for model training without null errors.",
                        required_evidence=["DatasetMetadata.missing_values_count", "DatasetMetadata.duplicate_rows"]
                    ))
                else:
                    hypotheses.append(DeliberationHypothesis(
                        id=str(uuid.uuid4()),
                        question_id=q.id,
                        description="Cleaning is unnecessary as the dataset is already pristine.",
                        expected_outcome="Skip cleaning phase to save compute time and memory.",
                        required_evidence=["DatasetMetadata.missing_values_count == 0"]
                    ))
            elif "llm" in q.text.lower():
                hypotheses.append(DeliberationHypothesis(
                    id=str(uuid.uuid4()),
                    question_id=q.id,
                    description="LLM is necessary to parse unstructured text or reasoning tasks.",
                    expected_outcome="Higher semantic understanding but higher latency.",
                    required_evidence=["UserGoal.intent requires generation or semantic search"]
                ))
                hypotheses.append(DeliberationHypothesis(
                    id=str(uuid.uuid4()),
                    question_id=q.id,
                    description="Deterministic Python/SQL computation is sufficient.",
                    expected_outcome="Low latency, 100% accurate mathematical computation.",
                    required_evidence=["UserGoal.intent involves pure aggregations or math"]
                ))
            else:
                # Generic fallback
                hypotheses.append(DeliberationHypothesis(
                    id=str(uuid.uuid4()),
                    question_id=q.id,
                    description="Proceed with standard default pipeline for this category.",
                    expected_outcome="Standard baseline execution.",
                    required_evidence=["UserGoal"]
                ))
                
        return hypotheses
