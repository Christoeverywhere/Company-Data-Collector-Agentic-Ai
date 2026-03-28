from schema import CompanySchemaPartial


def validate_final_output(final_output: dict) -> bool:
    if not isinstance(final_output, dict):
        raise AssertionError("Final output must be a dictionary")

    if len(final_output) == 0:
        raise AssertionError("Final output must not be empty")

    validated = CompanySchemaPartial(**final_output)

    if validated.company_name is None:
        raise AssertionError("Final output must include company_name")

    if validated.short_name is None:
        raise AssertionError("Final output must include short_name")

    if validated.category is None:
        raise AssertionError("Final output must include category")

    if validated.nature_of_company is None:
        raise AssertionError("Final output must include nature_of_company")

    if validated.profitability_status is None:
        raise AssertionError("Final output must include profitability_status")

    if validated.sales_motion is None:
        raise AssertionError("Final output must include sales_motion")

    if validated.year_of_incorporation is not None:
        if not (1800 <= validated.year_of_incorporation <= 2100):
            raise AssertionError("year_of_incorporation must be between 1800 and 2100")

    if validated.website_url is not None:
        if not str(validated.website_url).startswith("http"):
            raise AssertionError("website_url must start with http")

    if validated.countries_operating_in is not None and not isinstance(validated.countries_operating_in, list):
        raise AssertionError("countries_operating_in must be a list")

    if validated.focus_sectors_industries is not None and not isinstance(validated.focus_sectors_industries, list):
        raise AssertionError("focus_sectors_industries must be a list")

    if validated.services_offerings_products is not None and not isinstance(validated.services_offerings_products, list):
        raise AssertionError("services_offerings_products must be a list")

    if validated.key_competitors is not None and not isinstance(validated.key_competitors, list):
        raise AssertionError("key_competitors must be a list")

    if validated.technology_partners is not None and not isinstance(validated.technology_partners, list):
        raise AssertionError("technology_partners must be a list")

    if validated.key_business_leaders is not None and not isinstance(validated.key_business_leaders, list):
        raise AssertionError("key_business_leaders must be a list")

    if validated.interesting_facts is not None and not isinstance(validated.interesting_facts, list):
        raise AssertionError("interesting_facts must be a list")

    if validated.strategic_priorities is not None and not isinstance(validated.strategic_priorities, list):
        raise AssertionError("strategic_priorities must be a list")

    if validated.social_media_followers_combined is not None:
        if validated.social_media_followers_combined < 0:
            raise AssertionError("social_media_followers_combined cannot be negative")

    return True