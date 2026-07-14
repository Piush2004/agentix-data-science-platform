from typing import List
from core.brain.types import UnderstandingObject
from core.brain.deliberation.interfaces import IEvidenceCollector
from core.brain.deliberation.types import DeliberationEvidence

class DefaultEvidenceCollector(IEvidenceCollector):
    def collect(self, understanding: UnderstandingObject) -> List[DeliberationEvidence]:
        evidence = []
        
        # Extract deterministic metadata from the perception object
        meta = understanding.perception.dataset_metadata
        if meta:
            evidence.append(DeliberationEvidence(
                source="DatasetMetadata",
                data={
                    "rows": meta.get("rows", 0),
                    "columns": meta.get("columns", 0),
                    "size_bytes": meta.get("size_bytes", 0),
                    "missing_values_count": meta.get("missing_values", 0),
                    "duplicate_rows": meta.get("duplicates", 0),
                    "has_pii": meta.get("has_pii", False)
                },
                reliability_score=1.0
            ))
            
        # Domain evidence
        evidence.append(DeliberationEvidence(
            source="DomainProfile",
            data={"domain": understanding.domain},
            reliability_score=0.9
        ))
        
        # Goal evidence
        evidence.append(DeliberationEvidence(
            source="UserGoal",
            data={"intent": understanding.user_intent, "problem": understanding.business_problem},
            reliability_score=1.0
        ))
        
        return evidence
