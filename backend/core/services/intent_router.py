import re
from typing import Dict, Any

class IntentClassifier:
    def __init__(self):
        # Ordered by specificity, LLM triggers last.
        self.intent_patterns = {
            "pandas_math": [
                r"\b(how many rows|count|number of rows|rows|columns|math|calculate|add|subtract|multiply|divide|sum|average|mean|median|mode)\b"
            ],
            "scipy_statistics": [
                r"\b(stats|statistics|p-value|t-test|anova|distribution|variance|standard deviation|std)\b"
            ],
            "matplotlib_visualization": [
                r"\b(plot|chart|graph|histogram|scatter|bar chart|pie chart|visualize|show me a|trend)\b"
            ],
            "pandas_cleaning": [
                r"\b(clean|missing|null|nan|na|empty|drop column|drop row|drop na|drop duplicates|fill|impute|remove duplicates)\b"
            ],
            "sklearn_feature_engineering": [
                r"\b(feature|encode|scale|normalize|standardize|pca|one-hot|dummy variables)\b"
            ],
            "python_eda": [
                r"\b(outliers|anomalies|spread of|describe|summary stats|shape)\b"
            ],
            "python_correlation": [
                r"\b(correlation|corr|matrix|relationship between)\b"
            ],
            "python_script": [
                r"\b(python|script|function to|regex|clean the data|format column)\b"
            ],
            "sql_query": [
                r"\b(select|join|where|order by|sql query|query)\b"
            ],
            "automl_prediction": [
                r"\b(predict|forecast|classify|regression|train|model|automl)\b"
            ],
            "workflow_planning": [
                r"\b(plan|workflow|pipeline|orchestrate|sequence)\b"
            ],
            "llm": [
                r"\b(insight|generate|explain|why|suggest|recommend|business|summary|report|interpret|what does this mean)\b"
            ]
        }
        
    def classify(self, question: str) -> str:
        q_lower = question.lower()
        
        # We check in order of specificity to ensure LLM is the LAST option
        order_of_precedence = [
            "pandas_math", "scipy_statistics", "matplotlib_visualization", 
            "pandas_cleaning", "sklearn_feature_engineering", "python_eda", 
            "python_correlation", "python_script", "sql_query", "automl_prediction", 
            "workflow_planning", "llm"
        ]
        
        for intent in order_of_precedence:
            patterns = self.intent_patterns[intent]
            for pattern in patterns:
                if re.search(pattern, q_lower):
                    return intent
                    
        return "llm"  # Default to LLM if nothing else matches

class ExecutionRouter:
    def __init__(self):
        self.tokens_saved = 0
        
    def _estimate_tokens(self, df_shape: tuple) -> int:
        """Estimates token footprint of a dataset context to quantify savings."""
        rows, cols = df_shape
        # Rough heuristic: 1 token per cell + overhead
        return (rows * cols) + 500

    def route(self, intent: str, question: str, dataset_name: str, df_shape: tuple = (0,0)) -> Dict[str, Any]:
        """
        Routes to the appropriate engine based on intent, saving API tokens.
        """
        engine_map = {
            "pandas_math": "Pandas Statistics Engine",
            "scipy_statistics": "Scipy Stats Engine",
            "matplotlib_visualization": "Python Visualization Engine",
            "pandas_cleaning": "Pandas Cleaning Engine",
            "sklearn_feature_engineering": "Scikit-Learn Engine",
            "python_eda": "Python EDA Engine",
            "python_correlation": "Python Math Engine",
            "python_script": "Python Code Execution Engine",
            "sql_query": "SQL Query Engine",
            "automl_prediction": "AutoML Engine",
            "workflow_planning": "Agentix Brain",
            "llm": "LLM Business Reasoner"
        }
        
        target_engine = engine_map.get(intent, "LLM Business Reasoner")
        
        # Calculate tokens saved if we bypass the LLM
        tokens_saved = 0
        if intent != "llm":
            tokens_saved = self._estimate_tokens(df_shape)
            self.tokens_saved += tokens_saved
            
        return {
            "intent": intent,
            "engine_invoked": target_engine,
            "status": "routed",
            "question": question,
            "dataset_name": dataset_name,
            "tokens_saved": tokens_saved,
            "total_tokens_saved": self.tokens_saved
        }

class ResponseFormatter:
    def format_response(self, execution_result: Dict[str, Any]) -> str:
        intent = execution_result.get("intent", "unknown")
        engine = execution_result.get("engine_invoked", "Unknown Engine")
        saved = execution_result.get("tokens_saved", 0)
        
        response = f"✅ Query successfully routed to **{engine}**.\n"
        response += f"**Intent Detected**: {intent.upper()}\n"
        response += f"**Original Question**: {execution_result.get('question', '')}\n"
        
        if intent != "llm" and saved > 0:
            response += f"**Optimization**: Bypassed LLM inference. Est. tokens saved: {saved}\n"
        
        if intent == "llm":
            response += "\n*Note: This query required complex reasoning and was routed to the LLM as a last resort.*"
            
        return response

class IntentRouterService:
    def __init__(self):
        self.classifier = IntentClassifier()
        self.router = ExecutionRouter()
        self.formatter = ResponseFormatter()
        
    def process_query(self, question: str, dataset_name: str, df_shape: tuple = (0,0)) -> Dict[str, Any]:
        intent = self.classifier.classify(question)
        exec_result = self.router.route(intent, question, dataset_name, df_shape)
        formatted_resp = self.formatter.format_response(exec_result)
        
        return {
            "intent": intent,
            "execution_result": exec_result,
            "formatted_response": formatted_resp
        }

intent_router_service = IntentRouterService()
