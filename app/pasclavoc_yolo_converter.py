import glob
import os
import xml.etree.ElementTree as ET
import random

# Paths
IMAGE_DIR = os.path.expanduser('~/workstation/objective_db/classifier/JPEGImages/')
XML_DIR = os.path.expanduser('~/workstation/objective_db/classifier/bounding_boxes/')
OUTPUT_DIR = os.path.expanduser('~/workstation/objective_db/classifier/yolo/')
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

# 3️⃣ Write train.txt and val.txt
with open(os.path.expanduser('~/workstation/objective_db/classifier/train.txt'), 'w') as f:
    for img in train_images:
        f.write(img + '\n')

with open(os.path.expanduser('~/workstation/objective_db/classifier/val.txt'), 'w') as f:
    for img in val_images:
        f.write(img + '\n')

# 4️⃣ Function to convert bounding boxes to YOLO format
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return x*dw, y*dh, w*dw, h*dh

# 5️⃣ Convert XML annotation to YOLO .txt
def convert_annotation(image_path):
    basename = os.path.basename(image_path)
    name_no_ext = os.path.splitext(basename)[0]

    xml_file = os.path.join(XML_DIR, name_no_ext + '.xml')
    txt_file = os.path.join(OUTPUT_DIR, name_no_ext + '.txt')

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

# 6️⃣ Convert all images
for img in all_images:
    convert_annotation(img)

print("✅ YOLO annotations created successfully!")
print(f"Train images: {len(train_images)}, Validation images: {len(val_images)}")
