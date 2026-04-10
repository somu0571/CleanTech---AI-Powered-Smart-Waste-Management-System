"""
db.py – Database setup and models for CleanTech AI
(FINAL WITH ADMIN + RECYCLER ID SUPPORT)
"""

from sqlalchemy import (
    create_engine, Column, Integer, String,
    DateTime, Date
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pathlib import Path

# ── Database Config ─────────────────────────────

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'cleantech.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ── Models ──────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    # roles: citizen / admin / recycler
    role = Column(String)

    # 🔐 Role-based verification
    admin_id = Column(String, nullable=True)
    recycler_id = Column(String, nullable=True)

    # 🏢 Optional (for recyclers)
    organization = Column(String, nullable=True)

    eco_points = Column(Integer, default=0)
    last_reward_date = Column(Date, nullable=True)
    streak = Column(Integer, default=0)


# ✅ ADMIN ID TABLE
class AdminID(Base):
    __tablename__ = "admin_ids"

    id = Column(Integer, primary_key=True, index=True)
    valid_admin_id = Column(String, unique=True)


# ✅ RECYCLER ID TABLE (NEW)
class RecyclerID(Base):
    __tablename__ = "recycler_ids"

    id = Column(Integer, primary_key=True, index=True)
    valid_recycler_id = Column(String, unique=True)


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)
    username = Column(String)

    location = Column(String)
    description = Column(String)

    image_path = Column(String, nullable=True)

    # Status flow: pending → assigned → picked → recycled
    status = Column(String, default="pending")

    # ♻️ Recycler tracking
    assigned_recycler_id = Column(Integer, nullable=True)
    assigned_recycler_name = Column(String, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    zone = Column(String)
    predicted_waste = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)


class EcoActivity(Base):
    __tablename__ = "eco_activities"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)
    username = Column(String)

    activity = Column(String)
    points = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)


# ── Database Functions ──────────────────────────

def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()