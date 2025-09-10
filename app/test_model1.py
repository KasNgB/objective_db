import argparse
from ultralytics import YOLO
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser(description="Specify to run on CPU or GPU",)
    p.add_argument("--device", help="0 for GPU, -1 for CPU")
    return p.parse_args()

args = parse_args()
weights = Path("runs/detect/train/weights/best.pt")  # your trained model
src     = Path("classifier/video/apple_short3.mp4")  # the file you just downloaded

if "gpu" in args.device.lower():
    model = YOLO(weights)
    model.predict(
        source=str(src),
        device=0,        # use GPU
        imgsz=512,       # bump to 640 if smooth
        conf=0.5,
        vid_stride=2,    # skip frames for speed (2–5 is fine)
        save=True,       # writes ONE annotated .mp4
        save_frames=False,  # ensure it doesn’t dump per-frame JPGs
        project="runs/predict",
        name="apples_short",
    )
elif "cpu" in args.device.lower():
    model = YOLO(weights)
    model.predict(
        source=str(src),
        device="cpu",        # use CPU
        imgsz=512,
        conf=0.5,
        vid_stride=2,
        save=True,
        save_frames=False,
        project="runs/predict",
        name="apples_short",
    )
else:
    print("Please specify --device as 'cpu' or 'gpu'")
