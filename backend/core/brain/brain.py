from typing import Any, Dict
from core.brain.interfaces import (
    IPerception, IUnderstanding, IReasoning,
    IPlanning, IDecision, IExecution, ILearning
)
from core.brain.deliberation.deliberation_controller import DeliberationController
from core.brain.core_components import (
    BrainController, BrainState, BrainContext,
    BrainMemory, BrainEvents, BrainLogger
)
from core.memory.episodic.types import DatasetFingerprint
from core.memory.procedural.strategy_builder.interfaces import IStrategyRepository, IStrategyBuilder
from core.memory.procedural.strategy_recommendation.interfaces import IStrategyRecommendationEngine
from core.memory.procedural.strategy_recommendation.types import RecommendationAction
from core.memory.procedural.strategy_learning.interfaces import IStrategyLearningEngine
from core.memory.procedural.strategy_mining.strategy_miner import StrategyMiner

class AgentixBrain:
    """
    The main public interface of the Cognitive Engine.
    All components are tightly encapsulated. The only exposed method is process().
    """
    def __init__(
        self,
        perception: IPerception,
        understanding: IUnderstanding,
        reasoning: IReasoning,
        planning: IPlanning,
        decision: IDecision,
        execution: IExecution,
        learning: ILearning
    ):
        # Initialize submodules
        self._perception = perception
        self._understanding = understanding
        self._reasoning = reasoning
        self._planning = planning
        self._decision = decision
        self._execution = execution
        self._learning = learning

        # Initialize internal infrastructure
        self._logger = BrainLogger()
        self._events = BrainEvents()
        self._memory = BrainMemory()
        
        # Initialize internal Deliberation Layer
        self._deliberation = DeliberationController()
        
        # Note: In a real system, episodic memory controller dependencies would be injected.
        # We leave it optional to inject but instantiate defaults here for testing if not provided.
        self._episodic_memory = None
        self._strategy_repository: IStrategyRepository = None
        self._strategy_recommender: IStrategyRecommendationEngine = None
        self._strategy_learner: IStrategyLearningEngine = None
        self._strategy_miner: StrategyMiner = None
        self._strategy_builder: IStrategyBuilder = None

    def set_episodic_memory(self, episodic_memory):
        self._episodic_memory = episodic_memory
        
    def set_procedural_memory(
        self, 
        strategy_repo: IStrategyRepository, 
        recommender: IStrategyRecommendationEngine, 
        learner: IStrategyLearningEngine = None,
        miner: StrategyMiner = None,
        builder: IStrategyBuilder = None
    ):
        self._strategy_repository = strategy_repo
        self._strategy_recommender = recommender
        self._strategy_learner = learner
        self._strategy_miner = miner
        self._strategy_builder = builder

    def optimize_procedural_memory(self):
        """
        Runs the offline Strategy Mining and Building cycle.
        Analyzes Episodic Memory to discover and validate new active strategies.
        """
        if not self._episodic_memory or not self._strategy_miner or not self._strategy_builder:
            self._logger.log_thought("SYSTEM", "Procedural memory dependencies not fully injected. Skipping optimization.")
            return

        self._logger.log_thought("SYSTEM", "Starting offline Procedural Memory Optimization.")
        episodes = self._episodic_memory.store.get_all()
        candidates = self._strategy_miner.mine_strategies(episodes)
        
        built_strategies = []
        for candidate in candidates:
            strategy = self._strategy_builder.build_from_candidate(candidate)
            if strategy:
                built_strategies.append(strategy)
                
        self._logger.log_thought("SYSTEM", f"Optimization complete. Built {len(built_strategies)} new strategies.")
        return built_strategies

    def process(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        The singular entry point for the Cognitive Brain.
        Executes the full cognitive loop sequentially.
        """
        # 1. Initialization
        state = BrainState()
        context = BrainContext(raw_input)
        controller = BrainController(state, context, self._memory, self._events, self._logger)

        self._logger.log_thought("INIT", "Brain woke up and received input.")

        try:
            # 2. Perception Phase
            state.transition("PERCEPTION")
            self._logger.log_thought("PERCEPTION", "Observing environment and raw inputs.")
            perception_obj = self._perception.observe(raw_input)

            # 3. Understanding Phase
            state.transition("UNDERSTANDING")
            self._logger.log_thought("UNDERSTANDING", "Interpreting observations into intent.")
            understanding_obj = self._understanding.interpret(perception_obj)

            # 3.5 Deliberation Phase
            state.transition("DELIBERATION")
            self._logger.log_thought("DELIBERATION", "Generating hypotheses and assessing alternatives internally.")
            deliberation_result = self._deliberation.deliberate(understanding_obj)

            # 3.8 Episodic Memory Retrieval
            recommendations = []
            strategy_rec = None
            if self._episodic_memory:
                state.transition("MEMORY_RETRIEVAL")
                self._logger.log_thought("MEMORY_RETRIEVAL", "Have I seen something similar before?")
                meta = understanding_obj.perception.dataset_metadata
                fingerprint = DatasetFingerprint(
                    columns=meta.get("columns", []),
                    column_types={},
                    missing_value_ratio=meta.get("missing_values", 0) / max(meta.get("rows", 1), 1),
                    dataset_shape=[meta.get("rows", 0), len(meta.get("columns", []))],
                    business_domain=understanding_obj.domain,
                    target_variable=None
                )
                recommendations = self._episodic_memory.recall_experiences(fingerprint, understanding_obj.user_intent)
                
                if self._strategy_repository and self._strategy_recommender:
                    self._logger.log_thought("MEMORY_RETRIEVAL", "Do I already know a Strategy?")
                    active_strategy = self._strategy_repository.get_latest_version(understanding_obj.domain, understanding_obj.user_intent)
                    strategy_rec = self._strategy_recommender.recommend(
                        current_fingerprint=fingerprint,
                        user_intent=understanding_obj.user_intent,
                        active_strategy=active_strategy,
                        episodic_recommendations=recommendations
                    )

            # 4. Reasoning Phase
            state.transition("REASONING")
            self._logger.log_thought("REASONING", "Deducing what should happen based on deliberation and memory.")
            # Inject recommendations into reasoning (or deliberation result) so planning can consume it
            reasoning_obj = self._reasoning.reason(deliberation_result)
            reasoning_obj.episode_recommendations = recommendations
            reasoning_obj.strategy_recommendation = strategy_rec

            # 5. Planning Phase
            state.transition("PLANNING")
            self._logger.log_thought("PLANNING", "Generating execution plans.")
            execution_plan = self._planning.plan(reasoning_obj)

            # 6. Decision Phase
            state.transition("DECISION")
            self._logger.log_thought("DECISION", "Choosing the best plan and routing paths.")
            # Note: The IDecision interface expects a list of plans. We wrap the single plan here for signature matching.
            decision_obj = self._decision.decide([execution_plan], reasoning_obj)

            # 7. Execution Phase
            state.transition("EXECUTION")
            self._logger.log_thought("EXECUTION", "Coordinating engines and monitoring task.")
            result = self._execution.execute(decision_obj)

            # 8. Learning Phase
            state.transition("LEARNING")
            self._logger.log_thought("LEARNING", "Storing telemetry and execution success.")
            self._learning.record_outcome(decision_obj, result)

            if self._episodic_memory:
                self._logger.log_thought("LEARNING", "Writing new Episode to long-term memory.")
                ep_data = {
                    "user_id": context.raw_input.get("user_id", "system"),
                    "workspace_id": context.raw_input.get("workspace_id", "default"),
                    "dataset_id": context.raw_input.get("dataset_id", "unknown"),
                    "dataset_fingerprint": fingerprint.dict() if self._episodic_memory else {},
                    "dataset_profile": {},
                    "business_domain": understanding_obj.domain,
                    "user_goal": understanding_obj.business_problem,
                    "detected_intent": understanding_obj.user_intent,
                    "questions_generated": [q.text for q in deliberation_result.questions],
                    "hypotheses_generated": [h.description for h in deliberation_result.hypotheses],
                    "evidence_summary": deliberation_result.evidence_summary,
                    "chosen_hypothesis": decision_obj.chosen_plan.plan_id,
                    "confidence_score": decision_obj.reasoning.deliberation.rationale.confidence_score,
                    "workflow_plan": [{"step": s.action} for s in decision_obj.chosen_plan.steps],
                    "engines_used": [s.engine for s in decision_obj.chosen_plan.steps],
                    "llms_used": [],
                    "capabilities_used": [],
                    "execution_metrics": {
                        "execution_time_sec": decision_obj.chosen_plan.total_estimated_time_sec,
                        "memory_usage_mb": 100.0,
                        "success_score": 100.0 if result.get("status") == "success" else 0.0
                    },
                    "privacy_flags": [deliberation_result.risk_assessment],
                    "outcome": "SUCCESS" if result.get("status") == "success" else "FAILED"
                }
                episode = self._episodic_memory.record_experience(ep_data)

                # 8.1 Procedural Strategy Learning
                if self._strategy_repository and self._strategy_learner and strategy_rec:
                    # If we recommended REUSE or MODIFY, it implies the strategy was active and influenced planning.
                    if strategy_rec.strategy_id and strategy_rec.action != RecommendationAction.IGNORE:
                        active_strategy = self._strategy_repository.get_by_id(strategy_rec.strategy_id)
                        if active_strategy:
                            self._logger.log_thought("LEARNING", f"Updating Strategy {active_strategy.strategy_id} with new episode metrics.")
                            self._strategy_learner.learn_from_episode(active_strategy, episode, self._strategy_repository)
                            
            self._logger.log_thought("COMPLETE", "Cognitive cycle completed successfully.")
            
            return {
                "status": "success",
                "final_state": state.current_phase,
                "result": result
            }

        except Exception as e:
            self._logger.log_thought("ERROR", f"Brain encountered a fatal error: {str(e)}")
            failed_phase = state.current_phase
            state.transition("FAILED")
            return {
                "status": "error",
                "error": str(e),
                "phase_failed": failed_phase
            }
