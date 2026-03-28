RESEARCH_FIELDS = [
    "company_name",
    "short_name",
    "logo",
    "category",
    "year_of_incorporation",
    "overview_of_the_company",
    "nature_of_company",
    "company_headquarters",
    "countries_operating_in",
    "number_of_offices_beyond_hq",
    "employee_size",
    "pain_points_being_addressed",
    "focus_sectors_industries",
    "services_offerings_products",
    "core_value_proposition",
    "vision",
    "mission",
    "unique_differentiators",
    "competitive_advantages",
    "key_challenges_and_unmet_needs",
    "key_competitors",
    "technology_partners",
    "interesting_facts",
    "website_url",
    "social_media_followers_combined",
    "ceo_name",
    "key_business_leaders",
    "profitability_status",
    "sales_motion",
    "strategic_priorities"
]


def build_research_prompt(company_name: str) -> str:
    fields_text = "\n".join([f"- {field}" for field in RESEARCH_FIELDS])

    return f"""
You are a company research analyst.

ROLE:
You are an expert B2B market intelligence analyst tasked with collecting structured company information.

CONTEXT:
You will be given a company name. You must return ONLY structured JSON for the specified schema fields.
If information is unavailable, return null for that field.
Do not guess aggressively. Prefer null over hallucination.

GOAL:
Return a valid JSON object containing the following 30 fields for the company.

STRICT ENUM RULES:
- category must be EXACTLY one of: "Startup", "MSME", "SMB", "Enterprise", "Investor", "VC", "Conglomerate"
- nature_of_company must be EXACTLY one of: "Private", "Public", "Subsidiary", "Partnership", "Non-Profit", "Govt"
- profitability_status must be EXACTLY one of: "Profitable", "Break-even", "Loss-making"
- sales_motion must be EXACTLY one of: "PLG", "Product-Led", "Sales-Led", "Field Sales", "Channel", "Hybrid"

CONSTRAINTS:
- Return ONLY valid JSON
- Do not include markdown
- Do not include explanations
- Do not include any text before or after the JSON
- For list fields, return JSON arrays
- For URLs, return full valid URLs starting with https://
- For unknown values, use null
- If you are unsure about an enum field, return null instead of inventing a new category
- employee_size must be either a number string like "250" or range like "50-200"
- company_headquarters should be in format "City, Country" or "City, State, Country"

SCHEMA FIELDS:
{fields_text}

COMPANY NAME:
{company_name}
""".strip()