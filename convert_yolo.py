import os
import shutil
import random

SOURCE_DIR = "waste dataset"
DEST_DIR = "yolo_dataset"

CLASSES = {
    "Hazardous": 0,
    "Non-Recyclable": 1,
    "Organic": 2,
    "Recyclable": 3
}

# Create folders
for split in ["train", "val"]:
    os.makedirs(os.path.join(DEST_DIR, "images", split), exist_ok=True)
    os.makedirs(os.path.join(DEST_DIR, "labels", split), exist_ok=True)

split_ratio = 0.8

for class_name, class_id in CLASSES.items():
    class_path = os.path.join(SOURCE_DIR, class_name)

    # 🔥 Walk through ALL subfolders
    all_images = []
    for root, dirs, files in os.walk(class_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                all_images.append(os.path.join(root, file))

    random.shuffle(all_images)
    split_index = int(len(all_images) * split_ratio)

    train_imgs = all_images[:split_index]
    val_imgs = all_images[split_index:]

    for split, img_list in [("train", train_imgs), ("val", val_imgs)]:
        for img_path in img_list:
            img_name = os.path.basename(img_path)

            dst_img = os.path.join(DEST_DIR, "images", split, img_name)
            shutil.copy(img_path, dst_img)

            label_name = os.path.splitext(img_name)[0] + ".txt"
            label_path = os.path.join(DEST_DIR, "labels", split, label_name)

            with open(label_path, "w") as f:
                f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")

print("✅ Conversion completed successfully!")