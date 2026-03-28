import pytest
from transform_agent import TransformAgent
from schema import CompanySchemaPartial


@pytest.mark.live
def test_agent2_live_transform():
    research_outputs = {
        "gemini": {
            "company_name": "Sample Company",
            "short_name": "Sample",
            "category": "Enterprise",
            "year_of_incorporation": 2000,
            "overview_of_the_company": "A sample company used for testing.",
            "nature_of_company": "Public",
            "company_headquarters": "Sample City, Country",
            "countries_operating_in": ["USA", "India"],
            "number_of_offices_beyond_hq": 10,
            "employee_size": "1000",
            "pain_points_being_addressed": "Efficiency and productivity",
            "focus_sectors_industries": ["Technology", "Software"],
            "services_offerings_products": ["Cloud Platform", "Analytics Tool"],
            "core_value_proposition": "Reliable enterprise solutions",
            "vision": "To simplify business operations",
            "mission": "To deliver scalable software solutions",
            "unique_differentiators": "Fast deployment and strong support",
            "competitive_advantages": "Brand trust and innovation",
            "key_challenges_and_unmet_needs": "Global competition",
            "key_competitors": ["Competitor A", "Competitor B"],
            "technology_partners": ["Partner A", "Partner B"],
            "interesting_facts": ["Founded by engineers", "Operates globally"],
            "website_url": "https://www.sample.com/",
            "social_media_followers_combined": 500000,
            "ceo_name": "Jane Doe",
            "key_business_leaders": ["Jane Doe", "John Smith"],
            "profitability_status": "Profitable",
            "sales_motion": "Hybrid",
            "strategic_priorities": ["Expansion", "AI", "Cloud"]
        },
        "groq": {},
        "cerebras": {}
    }

    agent = TransformAgent()
    result = agent.run("Sample Company", research_outputs)

    assert isinstance(result, dict)
    assert len(result) > 0

    validated = CompanySchemaPartial(**result)

    assert validated.company_name is not None
    assert validated.category is not None
    assert validated.nature_of_company is not None
    assert validated.profitability_status is not None
    assert validated.sales_motion is not None