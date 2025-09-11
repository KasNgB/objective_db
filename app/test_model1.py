from ultralytics import YOLO
from pathlib import Path

weights = Path("runs/detect/train/weights/best.pt")  # your trained model
src     = Path("test_pictures/apple1.jpg")  # the file you just downloaded

model = YOLO(weights)
model.predict(
    source=str(src),
    device=0,        # use GPU
    imgsz=512,       # bump to 640 if smooth
    conf=0.5,
    vid_stride=2,    # skip frames for speed (2–5 is fine)
    save=True,       # writes ONE annotated .mp4
    save_frames=False,  # ensure it doesn’t dump per-frame JPGs
    project="runs/detect/predictions")

