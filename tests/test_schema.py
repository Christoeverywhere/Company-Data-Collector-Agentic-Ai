from schema import CompanySchemaPartial


def test_valid_minimal_schema():
    data = {
        "company_name": "Sample Company",
        "short_name": "Sample",
        "category": "Enterprise",
        "nature_of_company": "Public",
        "profitability_status": "Profitable",
        "sales_motion": "Hybrid"
    }

    obj = CompanySchemaPartial(**data)

    assert obj.company_name == "Sample Company"
    assert obj.category == "Enterprise"
    assert obj.nature_of_company == "Public"


def test_employee_size_range_with_commas():
    data = {
        "company_name": "Sample Company",
        "employee_size": "150,000-200,000"
    }

    obj = CompanySchemaPartial(**data)

    assert obj.employee_size == "150000-200000"


def test_social_media_followers_with_plus():
    data = {
        "company_name": "Sample Company",
        "social_media_followers_combined": "150,000,000+"
    }

    obj = CompanySchemaPartial(**data)

    assert obj.social_media_followers_combined == 150000000


def test_office_count_hundreds_becomes_none():
    data = {
        "company_name": "Sample Company",
        "number_of_offices_beyond_hq": "Hundreds"
    }

    obj = CompanySchemaPartial(**data)

    assert obj.number_of_offices_beyond_hq is None