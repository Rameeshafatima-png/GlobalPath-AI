from pydantic import BaseModel, Field
from typing import Optional

class StudentProfile(BaseModel):
    country: str = Field(min_length=2, max_length=80)
    degree: str = Field(min_length=2, max_length=80)
    budget: float = Field(gt=0)
    currency: str = "USD"
    budget_type: str = "annual"
    field: str = Field(min_length=2, max_length=100)
    academic_score: Optional[str] = None
    english_test: Optional[str] = None
    intake: Optional[str] = None
