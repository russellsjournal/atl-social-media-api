from contextlib import asynccontextmanager
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import db
from .schemas import Business, BusinessCreate, BusinessUpdate
from .lead_scoring import calculate_lead_score

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


SAMPLE_BUSINESSES = [
    BusinessCreate(
        name="Little Five Coffee",
        neighborhood="Little Five Points",
        category="Cafe",
        website="https://example.com/little-five-coffee",
        has_instagram=True,
        has_facebook=True,
        reviews_count=128,
        avg_rating=4.7,
    ),
    BusinessCreate(
        name="West End Wellness",
        neighborhood="West End",
        category="Health",
        website="https://example.com/west-end-wellness",
        has_instagram=True,
        reviews_count=42,
        avg_rating=4.5,
    ),
    BusinessCreate(
        name="Grant Park Books",
        neighborhood="Grant Park",
        category="Retail",
        has_facebook=True,
        reviews_count=23,
        avg_rating=4.4,
    ),
]


def seed_demo_businesses() -> None:
    if db.list_businesses():
        return

    for payload in SAMPLE_BUSINESSES:
        business = db.create_business(payload)
        business.lead_score = calculate_lead_score(business)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    seed_demo_businesses()
    yield


app = FastAPI(title="Atlanta Business Directory", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def homepage():
    return FileResponse(STATIC_DIR / "index.html")


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
