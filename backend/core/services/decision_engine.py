import hashlib
import time
import os
import psutil
import json
import asyncio
from typing import Dict, Any, List

class ExecutionGraph:
    """
    Constructs the DAG for execution after approval.
    """
    def __init__(self):
        # Topological edges mapping dependencies
        self.edges = {
            "Metadata Agent": [],
            "Cleaning Agent": ["Metadata Agent"],
            "EDA Agent": ["Cleaning Agent"],
            "Feature Engineering Agent": ["Cleaning Agent"],
            "AutoML Agent": ["Feature Engineering Agent"],
            "SHAP Agent": ["AutoML Agent"],
            "Report Agent": ["AutoML Agent", "SHAP Agent", "EDA Agent"],
            "LLM Agent": ["Metadata Agent"]
        }
        
    def sort_dag(self, approved_agents: List[str]) -> List[str]:
        """
        Sorts approved agents topologically so dependencies always execute first.
        """
        in_degree = {u: 0 for u in approved_agents}
        adj = {u: [] for u in approved_agents}
        
        for u in approved_agents:
            for v in self.edges.get(u, []):
                if v in approved_agents:
                    adj[v].append(u)
                    in_degree[u] += 1
                    
        queue = [u for u in approved_agents if in_degree[u] == 0]
        sorted_plan = []
        
        while queue:
            node = queue.pop(0)
            sorted_plan.append(node)
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        # Fallback if there are cycles or disconnected nodes
        if len(sorted_plan) != len(approved_agents):
            return approved_agents
            
        return sorted_plan

class ResourceScheduler:
    """
    Optimizes execution timing to minimize CPU/RAM peaks.
    """
    async def schedule(self, agent: str):
        # Simulated allocation
        if agent == "AutoML Agent":
            # Wait for RAM to clear up if CPU is high
            while psutil.cpu_percent() > 90:
                await asyncio.sleep(1)
        return True

class ExecutionCache:
    """
    Prevents recomputation of identical states using Redis (with file fallback).
    """
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        
    def _hash(self, agent: str, dataset: str) -> str:
        s = f"{agent}_{dataset}".encode('utf-8')
        return hashlib.md5(s).hexdigest()
        
    def check_hit(self, agent: str, dataset: str) -> bool:
        """
        Check if the artifact for this agent/dataset already exists via Redis Session Cache.
        """
        try:
            from core.redis_client import get_redis
            redis = get_redis()
            if redis:
                if redis.exists(f"execution_cache:{dataset}:{agent}") == 1:
                    return True
        except:
            pass
            
        base = dataset.split(".")[0]
        if agent == "Cleaning Agent":
            return os.path.exists(os.path.join(self.data_dir, f"{base}_cleaned.csv"))
        elif agent == "EDA Agent":
            return os.path.exists(os.path.join(self.data_dir, f"{base}_eda.json"))
        return False

    def mark_executed(self, agent: str, dataset: str):
        try:
            from core.redis_client import get_redis
            redis = get_redis()
            if redis:
                redis.setex(f"execution_cache:{dataset}:{agent}", 86400, "1")
        except:
            pass

class DecisionIntelligenceEngine:
    """
    Executes the approved workflow while minimizing compute footprints and preventing re-work.
    """
    def __init__(self, data_dir: str = "data"):
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../../{data_dir}")
        self.graph = ExecutionGraph()
        self.scheduler = ResourceScheduler()
        self.cache = ExecutionCache(self.data_dir)
        self.logs_path = os.path.join(self.data_dir, "execution_logs.json")
        
    async def execute_approved_plan(self, dataset_name: str) -> Dict[str, Any]:
        """
        Reads the user_approved plan and executes the DAG intelligently.
        """
        base_name = dataset_name.split(".")[0]
        plan_path = os.path.join(self.data_dir, f"{base_name}_workflow_plan.json")
        
        if not os.path.exists(plan_path):
            return {"status": "ERROR", "message": "No workflow plan found."}
            
        with open(plan_path, "r") as f:
            plan = json.load(f)
            
        if plan.get("status") != "USER_APPROVED":
            return {"status": "BLOCKED", "message": "Plan is not approved by user."}
            
        approved_agents = plan.get("execution_order", [])
        
        # 1. Topological Optimization
        sorted_dag = self.graph.sort_dag(approved_agents)
        
        execution_results = []
        process = psutil.Process(os.getpid())
        
        for agent in sorted_dag:
            start_time = time.time()
            mem_before = process.memory_info().rss
            
            # 2. Check Cache
            if self.cache.check_hit(agent, dataset_name):
                execution_results.append({
                    "agent": agent,
                    "status": "SKIPPED_CACHE_HIT",
                    "execution_time_sec": 0,
                    "ram_delta_mb": 0
                })
                continue
                
            # 3. Schedule Resources
            await self.scheduler.schedule(agent)
            
            # 4. Simulated Execution Wait (Mocking real agent compute)
            # In a full system, this would call the Event Bus to trigger the actual agent microservice
            await asyncio.sleep(0.1)
            
            mem_after = process.memory_info().rss
            exec_time = time.time() - start_time
            
            # 5. Monitor and Log
            result = {
                "agent": agent,
                "status": "COMPLETED",
                "execution_time_sec": round(exec_time, 4),
                "ram_delta_mb": round((mem_after - mem_before) / (1024 * 1024), 4)
            }
            execution_results.append(result)
            self._store_log(dataset_name, result)
            
        return {
            "status": "SUCCESS",
            "dataset_name": dataset_name,
            "optimized_dag": sorted_dag,
            "execution_trace": execution_results
        }
        
    def _store_log(self, dataset: str, entry: Dict[str, Any]):
        entry["dataset"] = dataset
        entry["timestamp"] = time.time()
        try:
            with open(self.logs_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

decision_engine = DecisionIntelligenceEngine()
