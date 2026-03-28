from typing import Optional, List, Union, Literal
from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator
from datetime import datetime
import re


CURRENT_YEAR = datetime.now().year


def _normalize_text(value) -> Optional[str]:
    if value is None:
        return None

    # If model returns a list for a text field, join it
    if isinstance(value, list):
        flattened = []
        for item in value:
            if isinstance(item, list):
                flattened.extend([str(x) for x in item if str(x).strip()])
            else:
                flattened.append(str(item))
        value = " ".join(flattened)

    value = str(value).strip()
    return value if value else None

def _split_comma_separated(value) -> Optional[List[str]]:
    if value is None:
        return None

    # If already a list, flatten safely
    if isinstance(value, list):
        cleaned = []
        for v in value:
            if isinstance(v, list):
                cleaned.extend([str(x).strip() for x in v if str(x).strip()])
            else:
                item = str(v).strip()
                if item:
                    cleaned.append(item)
        return cleaned or None

    # If string, split by comma
    parts = [part.strip() for part in str(value).split(",") if part.strip()]
    return parts or None


def _is_valid_range_string(value: str) -> bool:
    return bool(re.fullmatch(r"\d+|\d+\s*-\s*\d+", value.strip()))


class CompanySchemaBase(BaseModel):
    company_name: Optional[str] = Field(None, min_length=2, max_length=255)
    short_name: Optional[str] = Field(None, min_length=2, max_length=100)
    logo: Optional[HttpUrl] = None

    category: Optional[Literal[
        "Startup", "MSME", "SMB", "Enterprise", "Investor", "VC", "Conglomerate"
    ]] = None

    year_of_incorporation: Optional[int] = None

    overview_of_the_company: Optional[str] = Field(None, min_length=20, max_length=5000)

    nature_of_company: Optional[Literal[
        "Private", "Public", "Subsidiary", "Partnership", "Non-Profit", "Govt"
    ]] = None

    company_headquarters: Optional[str] = Field(None, min_length=5, max_length=255)

    countries_operating_in: Optional[List[str]] = None

    number_of_offices_beyond_hq: Optional[int] = Field(None, ge=0)

    employee_size: Optional[str] = Field(None, min_length=1, max_length=20)

    pain_points_being_addressed: Optional[str] = Field(None, min_length=10, max_length=2000)

    focus_sectors_industries: Optional[List[str]] = None

    services_offerings_products: Optional[List[str]] = None

    core_value_proposition: Optional[str] = Field(None, min_length=10, max_length=2000)

    vision: Optional[str] = Field(None, min_length=5, max_length=500)

    mission: Optional[str] = Field(None, min_length=5, max_length=500)

    unique_differentiators: Optional[str] = Field(None, min_length=5, max_length=2000)

    competitive_advantages: Optional[str] = Field(None, min_length=5, max_length=2000)

    key_challenges_and_unmet_needs: Optional[str] = Field(None, min_length=5, max_length=2000)

    key_competitors: Optional[List[str]] = None

    technology_partners: Optional[List[str]] = None

    interesting_facts: Optional[List[str]] = None

    website_url: Optional[HttpUrl] = None

    social_media_followers_combined: Optional[int] = Field(None, ge=0)

    ceo_name: Optional[str] = Field(None, min_length=2, max_length=100)

    key_business_leaders: Optional[List[str]] = None

    profitability_status: Optional[Literal[
        "Profitable", "Break-even", "Loss-making"
    ]] = None

    sales_motion: Optional[Literal[
        "PLG", "Product-Led", "Sales-Led", "Field Sales", "Channel", "Hybrid"
    ]] = None

    strategic_priorities: Optional[List[str]] = None

    @field_validator(
        "company_name",
        "short_name",
        "overview_of_the_company",
        "company_headquarters",
        "pain_points_being_addressed",
        "core_value_proposition",
        "vision",
        "mission",
        "unique_differentiators",
        "competitive_advantages",
        "key_challenges_and_unmet_needs",
        "ceo_name",
        mode="before"
    )
    @classmethod
    def normalize_text_fields(cls, v):
        return _normalize_text(v)

    @field_validator(
        "countries_operating_in",
        "focus_sectors_industries",
        "services_offerings_products",
        "key_competitors",
        "technology_partners",
        "interesting_facts",
        "key_business_leaders",
        "strategic_priorities",
        mode="before"
    )
    @classmethod
    def normalize_list_fields(cls, v):
        return _split_comma_separated(v)

    @field_validator("year_of_incorporation", mode="before")
    @classmethod
    def validate_year_of_incorporation(cls, v):
        if v is None:
            return v
        try:
            v = int(v)
        except Exception:
            raise ValueError("year_of_incorporation must be an integer")
        if v < 1800 or v > CURRENT_YEAR:
            raise ValueError(f"year_of_incorporation must be between 1800 and {CURRENT_YEAR}")
        return v

    @field_validator("number_of_offices_beyond_hq", mode="before")
    @classmethod
    def validate_number_of_offices_beyond_hq(cls, v):
        if v is None:
            return v

        if isinstance(v, int):
            return v

        text = str(v).strip().lower()

        vague_values = {
            "numerous", "many", "multiple", "various", "several",
            "global", "worldwide", "hundreds", "dozens"
        }
        if text in vague_values:
            return None

        match = re.search(r"\d+", text)
        if match:
            return int(match.group())

        raise ValueError("number_of_offices_beyond_hq must be an integer or contain a numeric value")

    @field_validator("social_media_followers_combined", mode="before")
    @classmethod
    def validate_social_media_followers_combined(cls, v):
        if v is None:
            return v

        if isinstance(v, int):
            return v

        text = str(v).replace(",", "").strip()
        match = re.search(r"\d+", text)

        if match:
            return int(match.group())

        raise ValueError("social_media_followers_combined must be an integer or contain a numeric value")

    @field_validator("employee_size", mode="before")
    @classmethod
    def validate_employee_size(cls, v):
        if v is None:
            return v

        v = _normalize_text(v)
        v = v.replace(",", "").replace(" ", "")

        if not _is_valid_range_string(v):
            raise ValueError("employee_size must be an integer string or range like '50-200'")

        if "-" in v:
            start, end = [int(x.strip()) for x in v.split("-")]
            if start >= end:
                raise ValueError("employee_size range must have min < max")

        return v

    @field_validator("ceo_name")
    @classmethod
    def validate_ceo_name(cls, v):
        if v is None:
            return v
        if not re.fullmatch(r"[A-Za-z\s.\-']+", v):
            raise ValueError("ceo_name contains invalid characters")
        return v

    @field_validator("company_headquarters")
    @classmethod
    def validate_company_headquarters(cls, v):
        if v is None:
            return v
        if "," not in v:
            raise ValueError("company_headquarters should include at least City, Country")
        return v

    @field_validator("key_business_leaders")
    @classmethod
    def validate_key_business_leaders(cls, v):
        if v is None:
            return v
        if len(v) == 0:
            raise ValueError("key_business_leaders cannot be an empty list")
        return v

    @field_validator("strategic_priorities")
    @classmethod
    def validate_strategic_priorities(cls, v):
        if v is None:
            return v
        if len(v) == 0:
            raise ValueError("strategic_priorities cannot be empty")
        return v


class CompanySchemaPartial(CompanySchemaBase):
    pass


class CompanySchemaStrict(CompanySchemaBase):
    company_name: str = Field(..., min_length=2, max_length=255)
    logo: HttpUrl
    category: Literal["Startup", "MSME", "SMB", "Enterprise", "Investor", "VC", "Conglomerate"]
    year_of_incorporation: int
    overview_of_the_company: str = Field(..., min_length=20, max_length=5000)
    nature_of_company: Literal["Private", "Public", "Subsidiary", "Partnership", "Non-Profit", "Govt"]
    company_headquarters: str = Field(..., min_length=5, max_length=255)
    employee_size: str = Field(..., min_length=1, max_length=20)
    pain_points_being_addressed: str = Field(..., min_length=10, max_length=2000)
    focus_sectors_industries: List[str]
    services_offerings_products: List[str]
    core_value_proposition: str = Field(..., min_length=10, max_length=2000)
    key_competitors: List[str]
    website_url: HttpUrl
    ceo_name: str = Field(..., min_length=2, max_length=100)
    key_business_leaders: List[str]
    profitability_status: Literal["Profitable", "Break-even", "Loss-making"]
    sales_motion: Literal["PLG", "Product-Led", "Sales-Led", "Field Sales", "Channel", "Hybrid"]
    strategic_priorities: List[str]

    @model_validator(mode="after")
    def validate_required_lists_non_empty(self):
        required_lists = {
            "focus_sectors_industries": self.focus_sectors_industries,
            "services_offerings_products": self.services_offerings_products,
            "key_competitors": self.key_competitors,
            "key_business_leaders": self.key_business_leaders,
            "strategic_priorities": self.strategic_priorities,
        }

        for field_name, field_value in required_lists.items():
            if not field_value or len(field_value) == 0:
                raise ValueError(f"{field_name} must contain at least one item")

        return self


class CompanySchemaPatch(CompanySchemaBase):
    pass