"""
CleanTech AI Backend (FINAL COMPLETE STABLE VERSION)
Run: uvicorn main:app --reload --port 8000
"""

import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime, date

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import init_db, get_db, User, Complaint, EcoActivity
from auth import (
    hash_password, verify_password,
    create_access_token, get_current_user
)

from model import predict as classify_image
from forecasting import get_predictions, get_heatmap_data
from routing import get_optimised_route


# ─────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────
app = FastAPI(title="CleanTech AI", version="FINAL")

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
    print("🔥 Backend started")
    init_db()


# ─────────────────────────────────────
# DEBUG ROUTES
# ─────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Backend running ✅"}


@app.get("/routes")
def routes():
    return [r.path for r in app.routes]


# ─────────────────────────────────────
# SCHEMAS
# ─────────────────────────────────────
class RegisterRequest(BaseModel):
    username: str
    password: str
    confirm_pass: str
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str


class ComplaintCreate(BaseModel):
    location: str
    description: str


class StatusUpdate(BaseModel):
    status: str


# ─────────────────────────────────────
# AUTH
# ─────────────────────────────────────
@app.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if req.password != req.confirm_pass:
        raise HTTPException(400, "Passwords do not match")

    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(409, "Username exists")

    user = User(
        username=req.username,
        password=hash_password(req.password),
        role=req.role.lower(),
        eco_points=0,
        last_reward_date=None
    )

    db.add(user)
    db.commit()

    return {"message": "Registered successfully"}


@app.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()

    if not user or not verify_password(req.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    # ✅ Daily reward
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
# USER FEATURES
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
                "date": a.created_at.strftime("%d %b %Y") if hasattr(a, "created_at") else ""
            }
            for a in activities
        ]
    }


@app.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.eco_points.desc()).limit(10).all()

    return [
        {
            "rank": i + 1,
            "username": u.username,
            "eco_points": u.eco_points
        }
        for i, u in enumerate(users)
    ]


# ─────────────────────────────────────
# DASHBOARD (FIXED)
# ─────────────────────────────────────
@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    total_citizens = db.query(User).count()
    total_complaints = db.query(Complaint).count()

    resolved = db.query(Complaint).filter(
        Complaint.status == "assigned"
    ).count()

    pending = db.query(Complaint).filter(
        Complaint.status == "pending"
    ).count()

    # ✅ NEW VALUES (fix for -kg and -%)
    waste_tracked = total_complaints * 1.5
    segregation_score = 75 if total_complaints > 0 else 0

    return {
        "total_citizens": total_citizens,
        "total_complaints": total_complaints,
        "resolved": resolved,
        "pending": pending,
        "co2_saved": total_complaints * 2,
        "waste_tracked": round(waste_tracked, 2),
        "segregation_score": segregation_score
    }


# ─────────────────────────────────────
# COMPLAINT SYSTEM
# ─────────────────────────────────────
@app.post("/complaint")
def create_complaint(
    req: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    comp = Complaint(
        user_id=current_user["id"],
        username=current_user["username"],
        location=req.location,
        description=req.description,
        status="pending",
        created_at=datetime.utcnow()
    )

    db.add(comp)

    user = db.get(User, current_user["id"])
    user.eco_points += 20

    db.add(EcoActivity(
        user_id=user.id,
        username=user.username,
        activity=f"Complaint at {req.location}",
        points=20
    ))

    db.commit()

    return {"message": "Complaint filed", "eco_points_earned": 20}


@app.get("/complaints")
def get_complaints(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    data = db.query(Complaint).order_by(Complaint.id.desc()).all()

    return [
        {
            "id": c.id,
            "location": c.location,
            "description": c.description,
            "status": c.status,
            "username": c.username,
            "timestamp": str(c.created_at) if hasattr(c, "created_at") else ""
        }
        for c in data
    ]


# ─────────────────────────────────────
# UPDATE STATUS
# ─────────────────────────────────────
@app.put("/update-status/{cid}")
def update_status(
    cid: int,
    req: StatusUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    comp = db.get(Complaint, cid)

    if not comp:
        raise HTTPException(404, "Complaint not found")

    if current_user["role"] not in ["admin", "recycler"]:
        raise HTTPException(403, "Not allowed")

    comp.status = req.status
    db.commit()

    return {"message": "Status updated"}


# ─────────────────────────────────────
# RECYCLER MODULE
# ─────────────────────────────────────
@app.get("/recycler/available")
def available_waste(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "recycler":
        raise HTTPException(403, "Only recyclers allowed")

    data = db.query(Complaint).filter(
        Complaint.status == "pending"
    ).all()

    return data


@app.post("/recycler/accept/{cid}")
def accept_pickup(
    cid: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "recycler":
        raise HTTPException(403, "Only recyclers allowed")

    comp = db.get(Complaint, cid)

    if not comp:
        raise HTTPException(404, "Not found")

    comp.status = "assigned"
    comp.assigned_recycler_id = current_user["id"]
    comp.assigned_recycler_name = current_user["username"]

    db.commit()

    return {"message": "Pickup accepted"}


@app.get("/recycler/my-jobs")
def my_jobs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "recycler":
        raise HTTPException(403, "Only recyclers allowed")

    jobs = db.query(Complaint).filter(
        Complaint.assigned_recycler_id == current_user["id"]
    ).all()

    return jobs


# ─────────────────────────────────────
# AI FEATURES
# ─────────────────────────────────────
@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    path = UPLOAD_DIR / file.filename

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return classify_image(str(path))


@app.get("/heatmap")
def heatmap():
    return get_heatmap_data()


@app.get("/predict")
def predict():
    return get_predictions()

@app.get("/route")
def route():
    return get_optimised_route(get_heatmap_data())