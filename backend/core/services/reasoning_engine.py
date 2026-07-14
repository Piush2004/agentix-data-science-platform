import time
import os
import json
import psutil
from typing import List, Dict, Any, Set
from core.services.intent_router import intent_router_service

class DependencyGraph:
    def __init__(self):
        # Defines the strict directed acyclic graph of agent dependencies.
        # Format: { "Agent": ["DependsOn1", "DependsOn2"] }
        self.dependencies = {
            "Dataset": [],
            "Metadata": ["Dataset"],
            "Cleaning": ["Dataset"],
            "Feature Engineering": ["Cleaning"],
            "EDA": ["Dataset"],  # EDA can run parallel or after Dataset
            "AutoML": ["Feature Engineering"],
            "Explainability": ["AutoML"],
            "Visualization": ["EDA", "Explainability"],
            "Context Builder": ["Metadata", "EDA", "AutoML", "Explainability"],
            "AI Analyst": ["Context Builder"],
            "Report": ["AI Analyst"]
        }
        
    def get_dependencies(self, target_agent: str, resolved: Set[str] = None) -> List[str]:
        if resolved is None:
            resolved = set()
            
        deps = self.dependencies.get(target_agent, [])
        plan = []
        for dep in deps:
            if dep not in resolved:
                sub_plan = self.get_dependencies(dep, resolved)
                plan.extend(sub_plan)
                plan.append(dep)
                resolved.add(dep)
                
        return plan

class TaskPlanner:
    def __init__(self):
        # Maps generic intents to the terminal node required.
        self.intent_to_target = {
            "pandas": "Metadata",
            "sql": "Cleaning",
            "eda": "EDA",
            "visualization": "Visualization",
            "python": "Feature Engineering",
            "llm": "Report"
        }
        
        # High-priority keyword overrides to pinpoint exact required models.
        self.keyword_to_target = {
            "train": "AutoML",
            "model": "AutoML",
            "predict": "AutoML",
            "explain": "Explainability",
            "shap": "Explainability",
            "evaluate": "Explainability",
            "report": "Report",
            "insight": "AI Analyst",
            "cleaning": "Cleaning",
            "missing": "Metadata"
        }
        
    def determine_target_agent(self, question: str, intent: str) -> str:
        q_lower = question.lower()
        for kw, target in self.keyword_to_target.items():
            if kw in q_lower:
                return target
        return self.intent_to_target.get(intent, "Report")

class ExecutionPlanner:
    def __init__(self, dependency_graph: DependencyGraph):
        self.graph = dependency_graph
        
    def build_plan(self, target_agent: str, cached_agents: Set[str] = None) -> Dict[str, Any]:
        """
        Builds a linear execution array eliminating any agents whose outputs
        are already present in memory (cached), ensuring optimal LLM & CPU load.
        """
        if cached_agents is None:
            cached_agents = set()
            
        full_deps = self.graph.get_dependencies(target_agent)
        
        execution_plan = []
        # Reconstruct execution DAG order while subtracting cached hits
        for agent in full_deps:
            if agent not in cached_agents:
                execution_plan.append(agent)
                cached_agents.add(agent)
                
        if target_agent not in cached_agents:
            execution_plan.append(target_agent)
            
        return {
            "target_agent": target_agent,
            "agents": execution_plan
        }

class AgentScheduler:
    def execute_plan(self, execution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the dynamically generated plan sequentially, recording telemetry.
        """
        logs = []
        process = psutil.Process(os.getpid())
        
        agents_to_run = execution_plan.get("agents", [])
        
        for agent in agents_to_run:
            start_time = time.time()
            mem_before = process.memory_info().rss
            
            # Simulate execution constraint blocks
            time.sleep(0.05) 
            
            mem_after = process.memory_info().rss
            elapsed = time.time() - start_time
            
            # Artificial costing (LLMs burn tokens; data agents burn CPU)
            cost = 0.05 if agent in ["AI Analyst", "Report"] else 0.001
            tokens = 1500 if agent in ["AI Analyst", "Report"] else 0
            
            logs.append({
                "agent": agent,
                "execution_time_sec": round(elapsed, 4),
                "memory_used_mb": round(max(0, (mem_after - mem_before)) / (1024 * 1024), 4),
                "cost_usd": cost,
                "tokens": tokens
            })
            
        return {
            "status": "Success",
            "executed_agents": agents_to_run,
            "telemetry_logs": logs
        }

class ReasoningEngine:
    def __init__(self):
        self.graph = DependencyGraph()
        self.task_planner = TaskPlanner()
        self.exec_planner = ExecutionPlanner(self.graph)
        self.scheduler = AgentScheduler()
        
    def process_request(self, question: str, cached_agents: Set[str] = None) -> Dict[str, Any]:
        """
        Main orchestration endpoint that processes natural language requests,
        intelligently trims the workflow via dependency resolution, and schedules agents.
        """
        # 1. Infer intent
        intent = intent_router_service.classifier.classify(question)
        
        # 2. Assign terminal target node
        target_agent = self.task_planner.determine_target_agent(question, intent)
        
        # 3. Create optimized topology plan
        plan = self.exec_planner.build_plan(target_agent, cached_agents)
        
        # 4. Schedule parallel/sequential runs and fetch telemetry
        result = self.scheduler.execute_plan(plan)
        
        response = {
            "question": question,
            "intent": intent,
            "target_agent": target_agent,
            "execution_plan": plan,
            "execution_logs": result["telemetry_logs"]
        }
        
        # Optionally dump to local telemetry store
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../reasoning_engine_logs.json")
        with open(log_path, "a") as f:
            f.write(json.dumps(response) + "\n")
            
        return response

reasoning_engine = ReasoningEngine()
