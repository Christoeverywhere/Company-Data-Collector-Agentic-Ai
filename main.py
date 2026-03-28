import json
from research_agent import ResearchAgent
from transform_agent import TransformAgent
from validation_gate import validate_final_output


def main():
    company_name = input("Enter company name: ").strip()

    research_agent = ResearchAgent()
    research_outputs = research_agent.run(company_name)

    print("\n" + "=" * 80)
    print("AGENT 1 OUTPUTS (3 LLM RESEARCH RESULTS)")
    print("=" * 80)

    for provider, result in research_outputs.items():
        print(f"\n--- {provider.upper()} OUTPUT ---")
        print(json.dumps(result, indent=4))

    print("\n" + "=" * 80)
    print("RUNNING AGENT 2 (LLM TRANSFORMATION / CONSOLIDATION)")
    print("=" * 80)

    transform_agent = TransformAgent()
    final_output = transform_agent.run(company_name, research_outputs)

    print("\n" + "=" * 80)
    print("RUNNING FINAL VALIDATION GATE (PYTEST RULES)")
    print("=" * 80)

    try:
        validate_final_output(final_output)
        print("✅ Final consolidated output passed validation gate")
    except Exception as e:
        print(f"❌ Final consolidated output failed validation gate: {e}")
        return

    print("\n" + "=" * 80)
    print("FINAL TRANSFORMED OUTPUT")
    print("=" * 80)
    print(json.dumps(final_output, indent=4))


if __name__ == "__main__":
    main()