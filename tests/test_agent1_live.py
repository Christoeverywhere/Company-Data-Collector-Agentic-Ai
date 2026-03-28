import os
import pytest
from research_agent import ResearchAgent


@pytest.mark.live
def test_agent1_live_generic():
    company_name = os.getenv("TEST_COMPANY", "Google")

    agent = ResearchAgent()
    result = agent.run(company_name)

    assert isinstance(result, dict)
    assert set(result.keys()) == {"gemini", "groq", "cerebras"}

    valid_outputs = [v for v in result.values() if isinstance(v, dict) and len(v) > 0]
    assert len(valid_outputs) >= 1, "At least one provider must return a valid structured output"

    for output in valid_outputs:
        assert output.get("company_name"), "company_name should not be empty"
        assert output.get("category"), "category should not be empty"
        assert output.get("nature_of_company"), "nature_of_company should not be empty"
        assert output.get("profitability_status"), "profitability_status should not be empty"
        assert output.get("sales_motion"), "sales_motion should not be empty"