import os
import pytest
from research_agent import ResearchAgent
from transform_agent import TransformAgent
from validation_gate import validate_final_output


@pytest.mark.live
def test_final_consolidated_output_from_agent2():
    company_name = os.getenv("TEST_COMPANY", "Google")

    research_agent = ResearchAgent()
    transform_agent = TransformAgent()

    research_outputs = research_agent.run(company_name)

    assert isinstance(research_outputs, dict)
    assert set(research_outputs.keys()) == {"gemini", "groq", "cerebras"}

    valid_outputs = [v for v in research_outputs.values() if isinstance(v, dict) and len(v) > 0]
    assert len(valid_outputs) >= 1, "Agent 1 must return at least one valid provider output"

    final_output = transform_agent.run(company_name, research_outputs)

    assert validate_final_output(final_output) is True