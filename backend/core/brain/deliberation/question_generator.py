import uuid
from typing import List
from core.brain.types import UnderstandingObject
from core.brain.deliberation.interfaces import IQuestionGenerator
from core.brain.deliberation.types import DeliberationQuestion

class DefaultQuestionGenerator(IQuestionGenerator):
    def generate(self, understanding: UnderstandingObject) -> List[DeliberationQuestion]:
        questions = []
        # General problem questions
        questions.append(DeliberationQuestion(
            id=str(uuid.uuid4()),
            text=f"Is an LLM actually necessary to solve {understanding.business_problem}?",
            category="Methodology"
        ))
        questions.append(DeliberationQuestion(
            id=str(uuid.uuid4()),
            text="Can deterministic computation solve this faster and cheaper?",
            category="Optimization"
        ))
        
        # Data related questions
        if understanding.data_quality_assessment.lower() in ["poor", "unknown"]:
            questions.append(DeliberationQuestion(
                id=str(uuid.uuid4()),
                text="Does this dataset require intensive cleaning before proceeding?",
                category="DataQuality"
            ))
        else:
            questions.append(DeliberationQuestion(
                id=str(uuid.uuid4()),
                text="Is the dataset already clean enough to skip preprocessing?",
                category="DataQuality"
            ))
            
        # Intent related
        intent = understanding.user_intent.lower()
        if "predict" in intent or "classify" in intent or "forecast" in intent:
            questions.append(DeliberationQuestion(
                id=str(uuid.uuid4()),
                text="Is there a clearly defined target variable?",
                category="Modeling"
            ))
            
        return questions
