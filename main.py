import argparse
import datetime
import time
import cv2
from ultralytics import YOLO
from sql.insert_test import insert_run


def parse_args():
    p = argparse.ArgumentParser(description="YOLO + OpenVINO on iPhone RTSP")
    p.add_argument(
        "--source",
        required=True,
        help="RTSP/HTTP URL from your iPhone (e.g., rtsp://192.168.1.50:8554/live) "
        "or use a GStreamer pipeline string with --gst",
    )
    p.add_argument(
        "--gst",
        action="store_true",
        help="Treat --source as a GStreamer pipeline string",
    )
    p.add_argument("--noshow", action="store_true", help="Don’t open a display window")
    return p.parse_args()


def main():
    args = parse_args()

    # Load OpenVINO-exported model. Passing the export folder or .xml both work.
    model = YOLO("./best_openvino_model")

    # If you checked the “GStreamer” box, pass the string as-is; otherwise OpenCV/ffmpeg will consume rtsp/http URL.
    source = args.source

    # Warm start the FPS counter
    t_prev = time.time()
    ema = None

    # Ultralytics returns a generator when stream=True
    for i, result in enumerate(
        model.predict(
            source=source,
            stream=True,
            imgsz=512,
            conf=0.4,
            vid_stride=2,
            max_det=300,
            # classes=[0, 1, 2],
            verbose=False,
            task="detect",
        )
    ):
        frame = result.plot()

        # FPS (EMA-smoothed)
        now = time.time()
        inst = 1.0 / (now - t_prev)
        t_prev = now
        ema = inst if ema is None else (0.9 * ema + 0.1 * inst)

        cv2.putText(
            frame,
            f"FPS: {ema:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        if not args.noshow:
            cv2.imshow("YOLO (OpenVINO AUTO) - iPhone RTSP", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    start = datetime.datetime.now()
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted - shutting down")
    finally:
        end = datetime.datetime.now()
        insert_run(start_time=start, end_time=end)
