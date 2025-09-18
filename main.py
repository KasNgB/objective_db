import argparse, time, cv2
from ultralytics import YOLO

def parse_args():
    p = argparse.ArgumentParser(description="YOLO + OpenVINO on iPhone RTSP")
    p.add_argument("--model", required=False,
                   help="Path to OpenVINO export dir or the .xml file (e.g., ./your_model_openvino or ./your_model_openvino/your_model.xml)")
    p.add_argument("--source", required=True,
                   help="RTSP/HTTP URL from your iPhone (e.g., rtsp://192.168.1.50:8554/live) "
                        "or use a GStreamer pipeline string with --gst")
    p.add_argument("--imgsz", type=int, default=640, help="Inference size (416–640 is a good range)")
    p.add_argument("--conf", type=float, default=0.35, help="Confidence threshold")
    p.add_argument("--stride", type=int, default=1, help="Process every Nth frame for extra headroom")
    p.add_argument("--gst", action="store_true",
                   help="Treat --source as a GStreamer pipeline string")
    p.add_argument("--noshow", action="store_true", help="Don’t open a display window")
    return p.parse_args()

def main():
    args = parse_args()

    # Load OpenVINO-exported model. Passing the export folder or .xml both work.
    model = YOLO("./openvino_model")

    # If you checked the “GStreamer” box, pass the string as-is; otherwise OpenCV/ffmpeg will consume rtsp/http URL.
    source = args.source

    # Warm start the FPS counter
    t_prev = time.time()
    ema = None

    # Ultralytics returns a generator when stream=True
    for i, result in enumerate(model.predict(
            source=source,
            stream=True,
            imgsz=512,
            conf=0.6,
            vid_stride=args.stride,
            verbose=False)):
        frame = result.plot()

        # FPS (EMA-smoothed)
        now = time.time()
        inst = 1.0 / (now - t_prev)
        t_prev = now
        ema = inst if ema is None else (0.9 * ema + 0.1 * inst)

        cv2.putText(frame, f"FPS: {ema:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if not args.noshow:
            cv2.imshow("YOLO (OpenVINO AUTO) - iPhone RTSP", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
