from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional

from fastapi.middleware.cors import CORSMiddleware

from .database import db
from .schemas import Business, BusinessCreate, BusinessUpdate
from .lead_scoring import calculate_lead_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/businesses", response_model=List[Business])
def list_businesses(
    neighborhood: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_lead_score: Optional[float] = Query(None),
):
    businesses = db.list_businesses()

    if neighborhood:
        businesses = [b for b in businesses if (b.neighborhood or "").lower() == neighborhood.lower()]
    if category:
        businesses = [b for b in businesses if (b.category or "").lower() == category.lower()]
    if min_lead_score is not None:
        businesses = [b for b in businesses if b.lead_score >= min_lead_score]

    return businesses

@app.post("/businesses", response_model=Business)
def create_business(payload: BusinessCreate):
    business = db.create_business(payload)
    business.lead_score = calculate_lead_score(business)
    return business

@app.get("/businesses/{business_id}", response_model=Business)
def get_business(business_id: int):
    business = db.get_business(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@app.put("/businesses/{business_id}", response_model=Business)
def update_business(business_id: int, payload: BusinessUpdate):
    business = db.update_business(business_id, payload)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    business.lead_score = calculate_lead_score(business)
    return business

@app.delete("/businesses/{business_id}")
def delete_business(business_id: int):
    deleted = db.delete_business(business_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Business not found")
    return {"deleted": True}
