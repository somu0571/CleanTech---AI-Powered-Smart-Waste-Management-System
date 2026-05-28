"""
CleanTech AI Backend (Optimized Version)
Run: uvicorn main:app --reload --port 8000
"""

from pathlib import Path
from datetime import datetime, date
from typing import List

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import init_db, get_db, User, Complaint, EcoActivity
from auth import (
    hash_password, verify_password,
    create_access_token, get_current_user
)

# ─────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────
app = FastAPI(title="CleanTech AI", version="Optimized")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.on_event("startup")
def startup():
    print("🚀 Backend started...")
    init_db()


# ─────────────────────────────────────
# BASIC ROUTES
# ─────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Backend running ✅"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ─────────────────────────────────────
# AUTH
# ─────────────────────────────────────
@app.post("/register")
def register(req: dict, db: Session = Depends(get_db)):
    if req["password"] != req["confirm_pass"]:
        raise HTTPException(400, "Passwords do not match")

    if db.query(User).filter(User.username == req["username"]).first():
        raise HTTPException(409, "Username exists")

    user = User(
        username=req["username"],
        password=hash_password(req["password"]),
        role=req["role"].lower(),
        eco_points=0
    )

    db.add(user)
    db.commit()

    return {"message": "Registered successfully"}


@app.post("/login")
def login(req: dict, db: Session = Depends(get_db)):
    print("🔐 Login attempt:", req["username"])

    user = db.query(User).filter(User.username == req["username"]).first()

    if not user or not verify_password(req["password"], user.password):
        raise HTTPException(401, "Invalid credentials")

    # Daily reward
    today = date.today()
    if user.last_reward_date != today:
        user.eco_points += 2
        user.last_reward_date = today

        db.add(EcoActivity(
            user_id=user.id,
            username=user.username,
            activity="Daily login reward",
            points=2
        ))

    db.commit()

    token = create_access_token({
        "sub": user.username,
        "role": user.role,
        "id": user.id
    })

    return {
        "access_token": token,
        "username": user.username,
        "role": user.role,
        "id": user.id,
        "eco_points": user.eco_points
    }


# ─────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────
@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    total_citizens = db.query(User).count()
    total_complaints = db.query(Complaint).count()

    resolved = db.query(Complaint).filter(Complaint.status == "assigned").count()
    pending = db.query(Complaint).filter(Complaint.status == "pending").count()

    return {
        "total_citizens": total_citizens,
        "total_complaints": total_complaints,
        "resolved": resolved,
        "pending": pending,
        "co2_saved": total_complaints * 2,
        "waste_tracked": round(total_complaints * 1.5, 2),
        "segregation_score": 75 if total_complaints > 0 else 0
    }

# ─────────────────────────────────────
# USER ACTIVITIES (FIX)
# ─────────────────────────────────────
@app.get("/my-activities")
def my_activities(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.get(User, current_user["id"])

    activities = db.query(EcoActivity).filter(
        EcoActivity.user_id == user.id
    ).order_by(EcoActivity.id.desc()).all()

    return {
        "eco_points": user.eco_points,
        "activities": [
            {
                "activity": a.activity,
                "points": a.points,
                "date": str(getattr(a, "created_at", ""))
            }
            for a in activities
        ]
    }


# ─────────────────────────────────────
# COMPLAINTS
# ─────────────────────────────────────
@app.post("/complaint")
def create_complaint(req: dict,
                     db: Session = Depends(get_db),
                     current_user: dict = Depends(get_current_user)):

    comp = Complaint(
        user_id=current_user["id"],
        username=current_user["username"],
        location=req["location"],
        description=req["description"],
        status="pending",
        created_at=datetime.utcnow()
    )

    db.add(comp)

    user = db.get(User, current_user["id"])
    user.eco_points += 20

    db.add(EcoActivity(
        user_id=user.id,
        username=user.username,
        activity=f"Complaint at {req['location']}",
        points=20
    ))

    db.commit()

    return {"message": "Complaint filed", "eco_points_earned": 20}


@app.get("/complaints")
def get_complaints(db: Session = Depends(get_db)):
    data = db.query(Complaint).order_by(Complaint.id.desc()).all()

    return [
        {
            "id": c.id,
            "location": c.location,
            "description": c.description,
            "status": c.status,
            "username": c.username,
            "timestamp": str(c.created_at)
        }
        for c in data
    ]


# ─────────────────────────────────────
# AI FEATURES (LAZY LOADING)
# ─────────────────────────────────────
@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    from model import predict  # ✅ Lazy import

    path = UPLOAD_DIR / file.filename
    with open(path, "wb") as f:
        f.write(await file.read())

    return predict(str(path))


@app.get("/heatmap")
def heatmap():
    from forecasting import get_heatmap_data
    return get_heatmap_data()


@app.get("/predict")
def predict():
    from forecasting import get_predictions
    return get_predictions()


@app.get("/route")
def route():
    from routing import get_optimised_route
    from forecasting import get_heatmap_data

    return get_optimised_route(get_heatmap_data())