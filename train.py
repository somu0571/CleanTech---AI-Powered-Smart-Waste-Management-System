from ultralytics import YOLO

def main():
    model = YOLO("yolov8n.pt")

    model.train(
    data="data.yaml",
    epochs=20,
    imgsz=224,
    batch=8,
    workers=0,   # 🔥 VERY IMPORTANT NOW
    device=0
)

if __name__ == "__main__":
    main()