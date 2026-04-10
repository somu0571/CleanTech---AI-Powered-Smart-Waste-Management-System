import os
import shutil
from sklearn.model_selection import train_test_split

# Classes in your dataset
classes = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

# Paths (based on your CleanTech structure)
base_path = "waste-classified"
output_path = "waste-classified/yolo_dataset"

# Create YOLO folders
for split in ["train", "val"]:
    os.makedirs(f"{output_path}/images/{split}", exist_ok=True)
    os.makedirs(f"{output_path}/labels/{split}", exist_ok=True)

# Process each class
for class_id, class_name in enumerate(classes):
    class_path = os.path.join(base_path, class_name)
    images = os.listdir(class_path)

    train, val = train_test_split(images, test_size=0.2, random_state=42)

    for split, data in zip(["train", "val"], [train, val]):
        for img in data:
            src = os.path.join(class_path, img)
            dst = f"{output_path}/images/{split}/{img}"
            shutil.copy(src, dst)

            # Create label file
            label_file = img.rsplit(".", 1)[0] + ".txt"
            label_path = f"{output_path}/labels/{split}/{label_file}"

            with open(label_path, "w") as f:
                f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")

print("✅ Conversion Done!")