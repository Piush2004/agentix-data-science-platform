from typing import List, Optional
from core.memory.episodic.types import DatasetFingerprint, EpisodeRecommendation
from core.memory.procedural.strategy_builder.types import ProceduralStrategy
from core.memory.procedural.strategy_recommendation.types import StrategyRecommendation, RecommendationAction
from core.memory.procedural.strategy_recommendation.interfaces import IStrategyRecommendationEngine

class DeterministicStrategyRecommender(IStrategyRecommendationEngine):
    def recommend(
        self,
        current_fingerprint: DatasetFingerprint,
        user_intent: str,
        active_strategy: Optional[ProceduralStrategy],
        episodic_recommendations: List[EpisodeRecommendation]
    ) -> StrategyRecommendation:
        
        # 1. No Strategy Exists
        if not active_strategy:
            return StrategyRecommendation(
                strategy_id=None,
                action=RecommendationAction.IGNORE,
                reasoning="No active strategy exists for this domain and intent.",
                confidence=100.0
            )

        # 2. Check Conditions
        modifications = []
        
        # Check target variable
        if active_strategy.conditions.target_variable_required and not current_fingerprint.target_variable:
            modifications.append("Strategy requires a target variable, but none was provided in the dataset fingerprint. A target discovery step must be added.")
            
        # Check required columns
        missing_cols = [c for c in active_strategy.conditions.required_columns if c not in current_fingerprint.columns]
        if missing_cols:
            modifications.append(f"Dataset is missing required columns: {missing_cols}. Imputation or mapping required.")
            
        # 3. Check Recent Episodic Failures for the identical workflow
        recent_failures = False
        for ep_rec in episodic_recommendations:
            ep = ep_rec.episode
            # If the episode used the same workflow but failed heavily
            if ep.workflow_plan == [{"step": s} for s in active_strategy.workflow]:
                if ep.execution_metrics.success_score < 50.0:
                    recent_failures = True
                    modifications.append(f"Recent episodic experience (Episode {ep.episode_id}) failed using this exact strategy workflow. Adaptation required.")
                    break
        
        # 4. Formulate Action
        if not modifications and not recent_failures:
            return StrategyRecommendation(
                strategy_id=active_strategy.strategy_id,
                action=RecommendationAction.REUSE,
                reasoning="Strategy conditions perfectly match the current dataset and no recent episodic failures were detected.",
                confidence=active_strategy.confidence
            )
        else:
            return StrategyRecommendation(
                strategy_id=active_strategy.strategy_id,
                action=RecommendationAction.MODIFY,
                reasoning="Strategy applies but requires modifications due to constraint mismatches or recent failures.",
                suggested_modifications=modifications,
                confidence=active_strategy.confidence - 20.0
            )
