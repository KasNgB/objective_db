from ultralytics import YOLO
from pathlib import Path


def yolo_analysis(file_path, conf):
    weights = Path(__file__).parent.parent / "runs/detect/train/weights/best.pt"
    file = file_path

    model = YOLO(weights)
    model.predict(
        source=str(file),
        device=0,        # use GPU
        imgsz=512,       # bump to 640 if smooth
        conf=conf,
        vid_stride=2,    # skip frames for speed (2–5 is fine)
        save=True,       # writes ONE annotated .mp4
        save_frames=False,  # ensure it doesn’t dump per-frame JPGs
        project=Path(__file__).parent.parent / "runs/detect/predictions"
        )

