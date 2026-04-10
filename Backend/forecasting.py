"""
forecasting.py – Predictive Waste Analytics
Uses ARIMA (statsmodels) with LSTM fallback simulation.
Generates / reads from data/dataset.csv.
"""

import os
import random
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data" / "dataset.csv"

ZONES = ["Zone A – North", "Zone B – East", "Zone C – South",
         "Zone D – West", "Zone E – Central"]


# ── Data generation ───────────────────────────────────────────────────────────

def _ensure_dataset():
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DATA_PATH.exists():
        return

    rng = np.random.default_rng(42)
    dates = pd.date_range("2023-01-01", periods=365, freq="D")
    records = []
    for zone in ZONES:
        base  = rng.uniform(40, 120)
        trend = rng.uniform(0.05, 0.2)
        noise = rng.normal(0, 5, len(dates))
        season = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)   # weekly
        amounts = base + trend * np.arange(len(dates)) + season + noise
        amounts = np.clip(amounts, 10, None)
        for d, a in zip(dates, amounts):
            records.append({"date": d.date(), "zone": zone,
                            "waste_kg": round(a, 2)})

    pd.DataFrame(records).to_csv(DATA_PATH, index=False)


# ── ARIMA forecast ────────────────────────────────────────────────────────────

def _arima_forecast(series: pd.Series, steps: int = 30):
    try:
        from statsmodels.tsa.arima.model import ARIMA
        model = ARIMA(series, order=(2, 1, 2))
        fit   = model.fit()
        fc    = fit.forecast(steps=steps)
        return fc.tolist()
    except Exception as e:
        print(f"[ARIMA] {e}")
        return None


def _fallback_forecast(series: pd.Series, steps: int = 30):
    """Simple linear extrapolation with noise."""
    last   = series.iloc[-1]
    slope  = (series.iloc[-1] - series.iloc[0]) / max(len(series), 1)
    result = []
    for i in range(steps):
        val = last + slope * (i + 1) + random.gauss(0, 3)
        result.append(round(max(val, 5), 2))
    return result


# ── Public API ────────────────────────────────────────────────────────────────

def get_predictions(zone: str = None, steps: int = 30) -> dict:
    """
    Returns:
        {
            "zone":        str,
            "historical":  [{date, waste_kg}],
            "forecast":    [{date, waste_kg}],
            "peak_day":    str,
            "high_zones":  [str],
            "method":      str
        }
    """
    _ensure_dataset()
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])

    target_zone = zone or ZONES[0]
    zdf = df[df["zone"] == target_zone].sort_values("date")
    series = zdf.set_index("date")["waste_kg"]

    # Forecast
    fc = _arima_forecast(series, steps)
    method = "ARIMA"
    if fc is None:
        fc = _fallback_forecast(series, steps)
        method = "Linear extrapolation"

    # Forecast dates
    last_date = series.index[-1]
    fc_dates  = [last_date + timedelta(days=i + 1) for i in range(steps)]

    # Historical (last 60 days)
    hist = [{"date": str(d.date()), "waste_kg": round(v, 2)}
            for d, v in series.tail(60).items()]
    fcast = [{"date": str(d.date()), "waste_kg": round(v, 2)}
             for d, v in zip(fc_dates, fc)]

    # Peak day
    peak_idx  = int(np.argmax(fc))
    peak_day  = str(fc_dates[peak_idx].date())

    # High-waste zones (last 7 days avg)
    zone_avg = (
        df[df["date"] >= df["date"].max() - timedelta(days=7)]
        .groupby("zone")["waste_kg"].mean()
        .sort_values(ascending=False)
    )
    high_zones = zone_avg.head(3).index.tolist()

    return {
        "zone":       target_zone,
        "all_zones":  ZONES,
        "historical": hist,
        "forecast":   fcast,
        "peak_day":   peak_day,
        "high_zones": high_zones,
        "method":     method,
    }


def get_heatmap_data() -> list[dict]:
    """Returns per-zone geo-centroid + waste level for map rendering."""
    _ensure_dataset()
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    recent = df[df["date"] >= df["date"].max() - timedelta(days=7)]
    zone_avg = recent.groupby("zone")["waste_kg"].mean().reset_index()

    # Simulated city centroids (Mumbai area)
    centroids = {
        "Zone A – North":   (19.22, 72.85),
        "Zone B – East":    (19.08, 72.92),
        "Zone C – South":   (18.92, 72.83),
        "Zone D – West":    (19.10, 72.78),
        "Zone E – Central": (19.07, 72.87),
    }
    result = []
    for _, row in zone_avg.iterrows():
        lat, lon = centroids.get(row["zone"], (19.07, 72.87))
        result.append({
            "zone":     row["zone"],
            "lat":      lat + random.uniform(-0.01, 0.01),
            "lon":      lon + random.uniform(-0.01, 0.01),
            "waste_kg": round(row["waste_kg"], 2),
        })
    return result