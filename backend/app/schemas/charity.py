from pydantic import BaseModel, Field


class CharityCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    category: str = Field(min_length=2, max_length=120)
    country: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=5)
    featured: bool = False


class CharityUpdateRequest(BaseModel):
    name: str | None = None
    category: str | None = None
    country: str | None = None
    description: str | None = None
    featured: bool | None = None


class CharityOut(BaseModel):
    id: int
    name: str
    category: str
    country: str
    description: str
    featured: bool

    model_config = {"from_attributes": True}


class DonationRequest(BaseModel):
    charity_id: int
    amount: float = Field(ge=1)
