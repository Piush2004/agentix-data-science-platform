import pytest
from core.services.intent_router import IntentClassifier, IntentRouterService

def test_intent_classifier():
    classifier = IntentClassifier()
    
    # Pandas
    assert classifier.classify("How many rows in the dataset?") == "pandas_math"
    assert classifier.classify("What are the missing values?") == "pandas_cleaning"
    assert classifier.classify("Calculate the mean of age") == "pandas_math"
    
    # EDA
    assert classifier.classify("Show correlation between age and income") == "python_correlation"
    assert classifier.classify("Are there any outliers?") == "python_eda"
    
    # Visualization
    assert classifier.classify("Plot a histogram of salaries") == "matplotlib_visualization"
    assert classifier.classify("Show me a bar chart") == "matplotlib_visualization"
    
    # SQL
    assert classifier.classify("Select id, name where age > 30") == "sql_query"
    assert classifier.classify("Group by country and order by id") == "sql_query"
    
    # Python
    assert classifier.classify("Write a python script to process this") == "python_script"
    
    # LLM (Keyword matching)
    assert classifier.classify("Generate business insights for next quarter") == "llm"
    assert classifier.classify("Why did sales drop?") == "llm"
    
    # LLM (Default fallback)
    assert classifier.classify("What is the meaning of life?") == "llm"

def test_execution_router():
    service = IntentRouterService()
    
    result = service.process_query("Plot a trend line", "test.csv")
    assert result["intent"] == "matplotlib_visualization"
    assert "Matplotlib_visualization Engine" in result["formatted_response"]
    
    result = service.process_query("Why is my churn rate so high?", "churn.csv")
    assert result["intent"] == "llm"
    assert "LLM as a last resort" in result["formatted_response"]
