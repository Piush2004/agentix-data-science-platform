import pandas as pd
import json
import os
from typing import Dict, Any

class DomainDetectionAgent:
    """
    Classifies the business sector or domain of a dataset natively via taxonomy heuristics.
    """
    def __init__(self, output_dir: str = "data"):
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../../{output_dir}")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Taxonomy Lexicon mapped to specific business domains
        self.domain_signatures = {
            "Healthcare": ["patient", "doctor", "diagnosis", "blood", "medical", "treatment", "hospital", "disease", "symptom", "heart", "glucose", "bmi"],
            "Finance": ["transaction", "balance", "account", "credit", "debit", "loan", "interest", "bank", "currency", "stock", "portfolio", "fraud", "card"],
            "Retail": ["product", "sales", "store", "customer", "revenue", "discount", "order", "item", "category", "inventory", "price", "cart", "basket"],
            "HR": ["employee", "salary", "department", "manager", "attrition", "hire", "performance", "tenure", "role", "leave", "payroll", "job"],
            "Education": ["student", "grade", "school", "teacher", "course", "exam", "score", "university", "attendance", "degree", "class"],
            "Marketing": ["campaign", "click", "impression", "conversion", "lead", "ad", "cpc", "roi", "audience", "engagement", "reach"],
            "Manufacturing": ["machine", "sensor", "factory", "production", "defect", "assembly", "yield", "temperature", "pressure", "maintenance"],
            "Insurance": ["policy", "claim", "premium", "coverage", "insured", "deductible", "accident", "damage", "payout", "actuary"],
            "Supply Chain": ["shipment", "freight", "warehouse", "logistics", "supplier", "delivery", "transit", "route", "cargo", "vendor"],
            "Telecommunications": ["churn", "plan", "call", "minutes", "data_usage", "roaming", "network", "broadband", "subscriber", "sim"],
            "Agriculture": ["crop", "yield", "soil", "weather", "harvest", "fertilizer", "rainfall", "farm", "pest", "irrigation"]
        }
        
    def analyze(self, df: pd.DataFrame, dataset_name: str) -> Dict[str, Any]:
        """
        Scans columns against internal taxonomy lexicons to declare a domain profile.
        """
        columns = [str(c).lower() for c in df.columns]
        
        domain_scores = {d: 0.0 for d in self.domain_signatures}
        matched_keywords = {d: [] for d in self.domain_signatures}
        
        # 1. Lexical Scoring Engine
        for col in columns:
            for domain, keywords in self.domain_signatures.items():
                for kw in keywords:
                    # Token match check
                    if kw in col:
                        domain_scores[domain] += 1.0
                        matched_keywords[domain].append(col)
                        
        # 2. Ranking and Extraction
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        
        primary_domain = "General/Agnostic"
        secondary_domain = "None"
        confidence = 0.50
        reasoning = "No strong domain signatures detected. Analyzing as a generic analytical dataset."
        
        # 3. Confidence Calculation
        if sorted_domains[0][1] > 0:
            primary_domain = sorted_domains[0][0]
            score = sorted_domains[0][1]
            total_cols = len(columns)
            
            # Confidence approaches 99% if density of recognized keywords is extremely high
            density = score / (total_cols + 1e-5)
            confidence = min(0.99, 0.40 + (density * 1.5))
            
            if sorted_domains[1][1] > 0:
                secondary_domain = sorted_domains[1][0]
                
            unique_matches = list(set(matched_keywords[primary_domain]))
            reasoning = f"Detected high correlation with {primary_domain} taxonomy. Key matched columns: {', '.join(unique_matches)}."
            
        # 4. Profile Assembly
        report = {
            "dataset_name": dataset_name,
            "primary_domain": primary_domain,
            "secondary_domain": secondary_domain,
            "confidence": round(confidence, 2),
            "reasoning": reasoning,
            "domain_scores": domain_scores,
            "matched_keywords": matched_keywords
        }
        
        # 5. Serialization
        report_filename = f"{dataset_name.split('.')[0]}_domain_profile.json"
        report_path = os.path.join(self.output_dir, report_filename)
        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)
            
        return {
            "primary_domain": primary_domain,
            "secondary_domain": secondary_domain,
            "confidence": round(confidence, 2),
            "reasoning": reasoning,
            "report_path": report_path,
            "report_data": report
        }
