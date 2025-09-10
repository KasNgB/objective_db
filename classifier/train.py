from pathlib import Path
from ultralytics import YOLO

HERE = Path(__file__).parent
data_yaml = HERE / "apples.yaml"              # lives next to train.py
weights = HERE / "yolo11n.pt"

model = YOLO(weights)
results = model.train(
    data=str(data_yaml),
    epochs=100, imgsz=512, device=0, batch=32, workers=2,
    deterministic=True, cache='disk'
)
