import os
import json
import math
from typing import List, Dict, Any

class EmbeddingService:
    def __init__(self):
        pass
        
    def generate_embedding(self, text: str) -> List[float]:
        """
        Simulates generating a dense vector embedding.
        In production, replace with SentenceTransformers or OpenAI text-embedding-ada-002.
        Here we use a deterministic pseudo-random array based on character frequencies
        to ensure similar texts have closer vectors.
        """
        text = text.lower()
        vector = [0.0] * 32  # 32-dim for lightweight simulation
        for i, char in enumerate(text):
            idx = (ord(char) * (i + 1)) % 32
            vector[idx] += 1.0
            
        # Normalize
        norm = math.sqrt(sum(v**2 for v in vector))
        if norm > 0:
            vector = [v / norm for v in vector]
        return vector
        
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = math.sqrt(sum(a**2 for a in vec1))
        norm_b = math.sqrt(sum(b**2 for b in vec2))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

class VectorDB:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../data/vector_db.json")
        self.db_path = os.path.abspath(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.embeddings = []
        self._load_db()
        
    def _load_db(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.embeddings = json.load(f)
            except Exception:
                self.embeddings = []
                
    def _save_db(self):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.embeddings, f, indent=4)
            
    def insert(self, doc_id: str, vector: List[float], metadata: dict):
        for i, record in enumerate(self.embeddings):
            if record["id"] == doc_id:
                self.embeddings[i] = {"id": doc_id, "vector": vector, "metadata": metadata}
                self._save_db()
                return
        self.embeddings.append({"id": doc_id, "vector": vector, "metadata": metadata})
        self._save_db()
        
    def search(self, query_vector: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        embedding_service = EmbeddingService()
        results = []
        for record in self.embeddings:
            sim = embedding_service.cosine_similarity(query_vector, record["vector"])
            results.append({
                "id": record["id"],
                "metadata": record["metadata"],
                "score": sim
            })
            
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
        
    def clear(self):
        self.embeddings = []
        self._save_db()

class Retriever:
    def __init__(self, db_path: str = None):
        self.embedding_service = EmbeddingService()
        self.vector_db = VectorDB(db_path)
        
    def index_dataset(self, dataset_name: str, context_string: str, full_metadata: dict):
        vector = self.embedding_service.generate_embedding(context_string)
        self.vector_db.insert(doc_id=dataset_name, vector=vector, metadata=full_metadata)
        
    def retrieve(self, query: str, top_k: int = 1) -> List[Dict[str, Any]]:
        query_vector = self.embedding_service.generate_embedding(query)
        return self.vector_db.search(query_vector, top_k)

class SemanticSearchAgent:
    def __init__(self, db_path: str = None):
        self.retriever = Retriever(db_path)
        
    def index_workspace_datasets(self, workspace_id: str):
        from core.services.knowledge_memory import knowledge_memory
        ctx = knowledge_memory.get_workspace_context(workspace_id)
        datasets = ctx.get("datasets", {})
        
        for ds_name, ds_info in datasets.items():
            meta = ds_info.get("metadata", {})
            rows = meta.get("rows", 0)
            cols = meta.get("columns", 0)
            target = meta.get("Target column", "unknown")
            
            models = ds_info.get("models", [])
            best_r2 = max([m.get("r2", 0) for m in models]) if models else 0
            model_types = ", ".join([m.get("type", "") for m in models])
            
            eda = ds_info.get("eda_summary", "")
            
            text = f"Dataset {ds_name} with {rows} rows and {cols} columns. Target variable is {target}. "
            text += f"Trained models include {model_types} with a best accuracy/R2 of {best_r2}. "
            text += f"EDA findings: {eda}"
            
            full_payload = {
                "dataset_name": ds_name,
                "rows": rows,
                "best_accuracy": best_r2,
                "semantic_text": text
            }
            self.retriever.index_dataset(ds_name, text, full_payload)
            
    def answer_query(self, query: str) -> str:
        results = self.retriever.retrieve(query, top_k=1)
        if not results:
            return "I couldn't find any relevant datasets in your memory."
            
        best = results[0]
        meta = best["metadata"]
        score = best["score"]
        
        response = f"Based on your query, the most relevant dataset is **{meta['dataset_name']}** (Relevance Score: {score:.2f}).\n"
        response += f"- **Rows**: {meta['rows']}\n"
        response += f"- **Best Accuracy**: {meta['best_accuracy']}\n"
        response += f"\n*Context used: {meta['semantic_text']}*"
        
        return response

semantic_search_agent = SemanticSearchAgent()
