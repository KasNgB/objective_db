from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11s.pt")

# Train the model on COCO8
results = model.train(
    data="data.yaml",
    epochs=100,
    imgsz=512,
    batch=16,
    device=0,  # Use GPU if available
    workers=2,
    deterministic=True,
    cache='disk'
)
