import pytest
import pandas as pd
from core.services.real_ai_analyst import RealAIAnalyst, SQLExecutor, PythonExecutor

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "score": [85.5, 92.0, 78.5]
    })

def test_python_executor(sample_df):
    executor = PythonExecutor()
    code = "result = df['score'].max()"
    res = executor.execute(sample_df, code)
    assert res["error"] is None
    assert res["result"] == 92.0

def test_python_executor_error(sample_df):
    executor = PythonExecutor()
    code = "result = df['missing_column'].max()"
    res = executor.execute(sample_df, code)
    assert res["error"] is not None
    assert "KeyError" in res["error"]

def test_sql_executor(sample_df):
    executor = SQLExecutor()
    query = "SELECT name FROM dataset WHERE score > 80"
    res = executor.execute(sample_df, query)
    assert res["error"] is None
    assert len(res["result"]) == 2
    assert "Alice" in res["result"]["name"].values

def test_real_ai_analyst(sample_df):
    analyst = RealAIAnalyst()
    
    # 1. SQL Route
    res_sql = analyst.analyze("Can you write a SQL query to get 5 rows?", sample_df)
    assert "SQL" in res_sql["trace"][0]
    assert "rows and" in res_sql["answer"]
    
    # 2. Python Visual Route
    res_plot = analyst.analyze("Generate a plot of the scores.", sample_df)
    assert "Visualization" in res_plot["trace"][0]
    assert "matplotlib" in res_plot["answer"]
    
    # 3. Python Calculate Route
    res_calc = analyst.analyze("Calculate the mean score.", sample_df)
    assert "calculation" in res_calc["trace"][0].lower()
    assert "2.00" in res_calc["answer"]
