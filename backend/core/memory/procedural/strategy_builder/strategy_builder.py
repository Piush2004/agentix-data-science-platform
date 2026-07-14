import logging
from typing import List, Optional
from core.memory.procedural.strategy_mining.types import StrategyCandidate
from core.memory.procedural.strategy_builder.types import ProceduralStrategy, StrategyConditions
from core.memory.procedural.strategy_builder.interfaces import (
    IStrategyBuilder, IStrategyRepository, IStrategyVersioning
)
from core.memory.procedural.strategy_validation.interfaces import IStrategyValidationEngine
from core.memory.procedural.strategy_builder.strategy_repository import InMemoryStrategyRepository
from core.memory.procedural.strategy_builder.strategy_versioning import DefaultStrategyVersioning
from core.memory.procedural.strategy_validation.strategy_validator import DeterministicStrategyValidator
from core.memory.procedural.strategy_validation.types import ValidationStatus

class StrategyBuilderFacade(IStrategyBuilder):
    """Facade that converts StrategyCandidates into active, versioned ProceduralStrategies."""
    
    def __init__(
        self,
        repository: IStrategyRepository = None,
        versioning: IStrategyVersioning = None,
        validator: IStrategyValidationEngine = None
    ):
        self.repository = repository or InMemoryStrategyRepository()
        self.versioning = versioning or DefaultStrategyVersioning()
        self.validator = validator or DeterministicStrategyValidator()
        self.logger = logging.getLogger("Agentix.Memory.StrategyBuilder")

    def build_from_candidate(self, candidate: StrategyCandidate) -> Optional[ProceduralStrategy]:
        self.logger.info(f"Building strategy from candidate {candidate.candidate_id}")
        
        # 1. Map Candidate to basic Strategy object
        strategy = ProceduralStrategy(
            domain=candidate.cluster_key.business_domain,
            intent=candidate.cluster_key.detected_intent,
            conditions=StrategyConditions(
                target_variable_required=(candidate.cluster_key.target_variable != "none"),
                required_columns=[],
                dataset_shape_constraints={}
            ),
            workflow=candidate.pattern.workflow_steps,
            capabilities=candidate.pattern.engines_used,
            expected_outcome="Success based on historical patterns",
            success_rate=candidate.average_success,
            failure_rate=100.0 - candidate.average_success,
            confidence=candidate.confidence,
            source_candidate_id=candidate.candidate_id
        )
        
        # 2. Validate
        history = self.repository.get_history(strategy.domain, strategy.intent)
        report = self.validator.validate_candidate(candidate, history)
        
        if report.status != ValidationStatus.APPROVED:
            self.logger.warning(f"Candidate {candidate.candidate_id} failed validation: {report.reasons}")
            return None
            
        # Strategy passes validation, mark as active
        strategy.is_active = True
            
        # 3. Versioning
        history = self.repository.get_history(strategy.domain, strategy.intent)
        strategy = self.versioning.resolve_version(strategy, history)
        
        # 4. Save
        saved_strategy = self.repository.save(strategy)
        self.logger.info(f"Successfully built and activated Strategy {saved_strategy.strategy_id} (v{saved_strategy.version})")
        
        return saved_strategy
