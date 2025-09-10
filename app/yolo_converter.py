import glob
import os
import xml.etree.ElementTree as ET
import random
import shutil

# Paths
IMAGE_DIR = os.path.expanduser('~/workstation/objective_db/classifier/JPEGImages/')
XML_DIR = os.path.expanduser('~/workstation/objective_db/classifier/bounding_boxes/')
OUTPUT_DIR = os.path.expanduser('~/workstation/objective_db/classifier/yolo/')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Create YOLOv8 directory structure
for split in ['train', 'val']:
    os.makedirs(os.path.join(OUTPUT_DIR, 'images', split), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'labels', split), exist_ok=True)

# Classes
classes = ['apple']

# Split percentage
split_pct = 10  # 10% for validation

# 1️⃣ Get all images and shuffle
all_images = glob.glob(os.path.join(IMAGE_DIR, '*.jpg'))
random.shuffle(all_images)

# 2️⃣ Split into train and validation
split_index = int(len(all_images) * split_pct / 100)
val_images = all_images[:split_index]
train_images = all_images[split_index:]

# 3️⃣ Function to convert bounding boxes to YOLO format
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return x*dw, y*dh, w*dw, h*dh

# 4️⃣ Convert XML annotation to YOLO .txt
def convert_annotation(image_path, label_out_dir):
    basename = os.path.basename(image_path)
    name_no_ext = os.path.splitext(basename)[0]

    xml_file = os.path.join(XML_DIR, name_no_ext + '.xml')
    txt_file = os.path.join(label_out_dir, name_no_ext + '.txt')

    if not os.path.exists(xml_file):
        print(f"Warning: XML file not found: {xml_file}")
        return

    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    with open(txt_file, 'w') as out_file:
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (
                float(xmlbox.find('xmin').text),
                float(xmlbox.find('xmax').text),
                float(xmlbox.find('ymin').text),
                float(xmlbox.find('ymax').text)
            )
            bb = convert((w, h), b)
            out_file.write(f"{cls_id} " + " ".join([str(a) for a in bb]) + '\n')

# 5️⃣ Process and copy images + labels to YOLOv8 format
def process_split(images, split):
    img_out_dir = os.path.join(OUTPUT_DIR, 'images', split)
    lbl_out_dir = os.path.join(OUTPUT_DIR, 'labels', split)

    for img in images:
        # Copy image
        shutil.copy(img, img_out_dir)
        # Convert and save label
        convert_annotation(img, lbl_out_dir)

# Process train and val splits
process_split(train_images, 'train')
process_split(val_images, 'val')

print("✅ YOLOv8 dataset created successfully!")
print(f"Train images: {len(train_images)}, Validation images: {len(val_images)}")
print(f"Dataset saved to: {OUTPUT_DIR}")
