import pytest
from core.services.multi_agent_collaboration import MultiAgentTeam

def test_multi_agent_team():
    team = MultiAgentTeam()
    
    query = "Analyze the churn dataset and give me recommendations."
    dataset_name = "customer_churn.csv"
    
    # Run the collaboration graph
    final_state = team.collaborate(query, dataset_name)
    
    # Verify State Mutations
    assert "CEO Directive:" in final_state["query"]
    assert len(final_state["plan"]) == 7
    assert "df.dropna" in final_state["engineering_code"]
    assert "collinearity" in final_state["eda_insights"]
    assert "XGBoost" in final_state["ml_metrics"]
    assert "ROI" in final_state["business_insights"]
    
    # Verify Final Outputs
    assert "Executive Analytics Report" in final_state["final_report"]
    assert "Approved for final delivery." in final_state["final_report"]
    assert final_state["review_status"] == "Approved"

def test_multi_agent_team_rejected():
    # If we somehow injected "Error" in the draft report, the reviewer should reject it.
    team = MultiAgentTeam()
    
    # We can test the reviewer agent directly
    from core.services.multi_agent_collaboration import reviewer_agent
    
    bad_state = {"draft_report": "There was a massive Error in the model."}
    res = reviewer_agent(bad_state)
    
    assert res["review_status"] == "Rejected"
    assert "failed" in res["final_report"]
