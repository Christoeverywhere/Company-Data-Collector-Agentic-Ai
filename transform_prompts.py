def build_transform_prompt(company_name: str, research_outputs: dict) -> str:
    return f"""
You are a company data consolidation and transformation agent.

ROLE:
You are given up to 3 structured JSON outputs about the same company from multiple LLM research agents.
Your task is to consolidate them into ONE final best-quality JSON object.

GOAL:
Return ONLY one final JSON object with the exact same 30 schema fields.

INSTRUCTIONS:
- Compare all provided source outputs carefully
- Prefer values that are:
  1. More specific
  2. More complete
  3. More realistic
  4. Consistent across multiple sources
- If two sources conflict:
  - choose the more credible / specific value
- If a field is missing in one source but available in another, use the available value
- For list fields:
  - merge useful non-duplicate items
  - remove duplicates
  - keep concise and relevant items only
- For long text fields:
  - produce a clean, concise, high-quality merged version
- For enum fields, STRICTLY follow allowed values only
- If unsure, return null rather than inventing
- Return ONLY valid JSON
- No markdown
- No explanations
- No extra text

STRICT ENUM RULES:
- category must be EXACTLY one of: "Startup", "MSME", "SMB", "Enterprise", "Investor", "VC", "Conglomerate"
- nature_of_company must be EXACTLY one of: "Private", "Public", "Subsidiary", "Partnership", "Non-Profit", "Govt"
- profitability_status must be EXACTLY one of: "Profitable", "Break-even", "Loss-making"
- sales_motion must be EXACTLY one of: "PLG", "Product-Led", "Sales-Led", "Field Sales", "Channel", "Hybrid"

COMPANY:
{company_name}

SOURCE OUTPUTS:
{research_outputs}
""".strip()