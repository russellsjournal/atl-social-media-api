from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class BusinessBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "ATL Coffee Co."})
    neighborhood: Optional[str] = None
    category: Optional[str] = None
    website: Optional[HttpUrl] = None
    google_maps_url: Optional[HttpUrl] = None
    has_instagram: bool = False
    has_facebook: bool = False
    reviews_count: int = 0
    avg_rating: float = 0.0


class BusinessCreate(BusinessBase):
    pass


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    neighborhood: Optional[str] = None
    category: Optional[str] = None
    website: Optional[HttpUrl] = None
    google_maps_url: Optional[HttpUrl] = None
    has_instagram: Optional[bool] = None
    has_facebook: Optional[bool] = None
    reviews_count: Optional[int] = None
    avg_rating: Optional[float] = None


class Business(BusinessBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_score: float = 0.0
