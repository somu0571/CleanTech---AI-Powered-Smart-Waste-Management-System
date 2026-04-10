from ultralytics import YOLO
from PIL import Image

# ✅ Load trained model (correct path)
model = YOLO("best.pt")

# Map YOLO classes → your app classes
CLASS_MAP = {
    "cardboard": "Organic",
    "paper": "Organic",
    "glass": "Plastic",
    "plastic": "Plastic",
    "metal": "Metal",
    "trash": "Hazardous"
}

# Disposal suggestions
DISPOSAL = {
    "Organic": "Use green bin or compost it 🌱",
    "Plastic": "Clean and put in recycling bin ♻️",
    "Metal": "Send to scrap dealer 🔩",
    "E-waste": "Drop at e-waste center 💻",
    "Hazardous": "Dispose via municipal service ⚠️"
}


def predict(image_file):
    img = Image.open(image_file)

    results = model(img)

    boxes = results[0].boxes

    # ❌ No detection
    if boxes is None or len(boxes) == 0:
        return {
            "class": "Unknown",
            "confidence": 0,
            "method": "YOLOv8 Detection",
            "disposal": "Try clearer image",
            "eco_points_earned": 0
        }

    # ✅ Take highest confidence detection
    box = boxes[0]
    class_id = int(box.cls[0])
    confidence = float(box.conf[0])

    raw_class = model.names[class_id]
    final_class = CLASS_MAP.get(raw_class, "Hazardous")

    return {
        "class": final_class,
        "confidence": round(confidence, 2),
        "method": "YOLOv8 Detection",
        "disposal": DISPOSAL[final_class],
        "eco_points_earned": 10
    }