import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Pack, QuoteRequest, Consultation

app = FastAPI(title="Sponsorisily API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Sponsorisily API running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from Sponsorisily backend!"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Fallback packs used when database has no entries yet
DEFAULT_PACKS = [
    {
        "platform": "Facebook & Instagram",
        "logo": "https://cdn.simpleicons.org/meta/ffffff",
        "name": "Pack Starter",
        "price_DA": "15,000 DA",
        "duration": "7 jours",
        "results": ["+5k vues", "+300 clics", "+50 leads"],
        "advantages": ["Ciblage basique", "Créa 1 visuel"],
        "objective": "Trafic"
    },
    {
        "platform": "Facebook & Instagram",
        "logo": "https://cdn.simpleicons.org/meta/ffffff",
        "name": "Pack Boost",
        "price_DA": "30,000 DA",
        "duration": "14 jours",
        "results": ["+15k vues", "+1k clics", "+150 leads"],
        "advantages": ["A/B test créa", "Ciblage lookalike"],
        "objective": "Conversions"
    },
    {
        "platform": "TikTok",
        "logo": "https://cdn.simpleicons.org/tiktok/ffffff",
        "name": "Pack Viral",
        "price_DA": "25,000 DA",
        "duration": "10 jours",
        "results": ["+50k vues", "+2k interactions"],
        "advantages": ["Spark Ads", "UGC conseillé"],
        "objective": "Reach"
    },
    {
        "platform": "YouTube",
        "logo": "https://cdn.simpleicons.org/youtube/ffffff",
        "name": "Pack Viewers",
        "price_DA": "20,000 DA",
        "duration": "7 jours",
        "results": ["+10k vues", "+60% VTR"],
        "advantages": ["InStream Skippable"],
        "objective": "Branding"
    },
    {
        "platform": "Google Ads",
        "logo": "https://cdn.simpleicons.org/googleads/ffffff",
        "name": "Pack Search",
        "price_DA": "35,000 DA",
        "duration": "14 jours",
        "results": ["CPC optimisé", "+200 conversions"],
        "advantages": ["Extensions d’annonces", "Remarketing"],
        "objective": "Leads"
    },
    {
        "platform": "LinkedIn",
        "logo": "https://cdn.simpleicons.org/linkedin/ffffff",
        "name": "Pack Pro",
        "price_DA": "40,000 DA",
        "duration": "14 jours",
        "results": ["+50 prospects B2B"],
        "advantages": ["Ciblage par poste", "Lead Gen Forms"],
        "objective": "Prospection"
    }
]

# Packs endpoints
@app.post("/api/packs", response_model=dict)
def create_pack(pack: Pack):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    inserted_id = create_document("pack", pack)
    return {"id": inserted_id}

@app.get("/api/packs", response_model=List[dict])
def list_packs():
    if db is None:
        # If database is not configured, still return defaults so frontend shows multiple packs
        return DEFAULT_PACKS
    docs = get_documents("pack")
    if not docs:
        # return defaults when empty (no seeding to DB to keep it idempotent)
        return DEFAULT_PACKS
    # Convert ObjectId
    for d in docs:
        d["id"] = str(d.pop("_id", ""))
    return docs

# Quote requests (devis)
@app.post("/api/quotes", response_model=dict)
def create_quote(quote: QuoteRequest):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    inserted_id = create_document("quoterequest", quote)
    return {"id": inserted_id}

# Consultations
@app.post("/api/consultations", response_model=dict)
def create_consultation(consultation: Consultation):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    inserted_id = create_document("consultation", consultation)
    return {"id": inserted_id}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
