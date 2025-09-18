import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GdkPixbuf, GLib
import cv2
import numpy as np
import threading
import time
from ultralytics import YOLO
import queue


class YOLODetectorGUI:
    def __init__(self):
        self.model = None
        self.detection_thread = None
        self.running = False
        self.frame_queue = queue.Queue(maxsize=2)  # Small queue to prevent lag
        
        # Create the main window
        self.window = Gtk.Window()
        self.window.set_title("YOLO Human Detection")
        self.window.set_default_size(800, 600)
        self.window.connect("destroy", self.on_window_destroy)
        
        # Create main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_left(10)
        main_box.set_margin_right(10)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        
        # URL input section
        url_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        url_label = Gtk.Label("RTSP URL:")
        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("rtsp://192.168.1.50:8554/live")
        self.url_entry.set_hexpand(True)
        url_box.pack_start(url_label, False, False, 0)
        url_box.pack_start(self.url_entry, True, True, 0)
        
        # Display option
        self.show_video_check = Gtk.CheckButton("Show video display")
        self.show_video_check.set_active(True)
        
        # Control buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.start_button = Gtk.Button("Start Detection")
        self.start_button.connect("clicked", self.on_start_clicked)
        self.stop_button = Gtk.Button("Stop Detection")
        self.stop_button.connect("clicked", self.on_stop_clicked)
        self.stop_button.set_sensitive(False)
        
        button_box.pack_start(self.start_button, True, True, 0)
        button_box.pack_start(self.stop_button, True, True, 0)
        
        # Status section
        status_frame = Gtk.Frame(label="Status")
        status_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        status_box.set_margin_left(10)
        status_box.set_margin_right(10)
        status_box.set_margin_top(5)
        status_box.set_margin_bottom(10)
        
        self.connection_label = Gtk.Label("Connection: Disconnected")
        self.fps_label = Gtk.Label("FPS: 0.0")
        self.detection_label = Gtk.Label("Humans detected: 0")
        
        status_box.pack_start(self.connection_label, False, False, 0)
        status_box.pack_start(self.fps_label, False, False, 0)
        status_box.pack_start(self.detection_label, False, False, 0)
        status_frame.add(status_box)
        
        # Video display
        self.image_widget = Gtk.Image()
        self.image_widget.set_size_request(640, 480)
        
        # Pack everything
        main_box.pack_start(url_box, False, False, 0)
        main_box.pack_start(self.show_video_check, False, False, 0)
        main_box.pack_start(button_box, False, False, 0)
        main_box.pack_start(status_frame, False, False, 0)
        main_box.pack_start(self.image_widget, True, True, 0)
        
        self.window.add(main_box)
        
        # Setup periodic GUI updates
        GLib.timeout_add(33, self.update_display)  # ~30 FPS display update

    def on_human_detected(self, count, frame):
        """
        Callback hook for when humans are detected.
        Override this method or connect to it for custom logic.
        
        Args:
            count (int): Number of humans detected in current frame
            frame (numpy.ndarray): Current frame with detections drawn
        """
        # This is where you can add your custom logic for car sensor responses
        # For now, just update the GUI
        GLib.idle_add(self.update_detection_count, count)
        
        # Example: You could add logic here like:
        # if count > 0:
        #     print(f"WARNING: {count} humans detected!")
        #     # Send signal to car system, play sound, etc.

    def on_start_clicked(self, button):
        url = self.url_entry.get_text().strip()
        if not url:
            dialog = Gtk.MessageDialog(
                transient_for=self.window,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Please enter an RTSP URL"
            )
            dialog.run()
            dialog.destroy()
            return
        
        # Load model if not already loaded
        if self.model is None:
            try:
                GLib.idle_add(self.update_connection_status, "Loading model...")
                self.model = YOLO("./best_openvino_model")
                GLib.idle_add(self.update_connection_status, "Model loaded")
            except Exception as e:
                GLib.idle_add(self.update_connection_status, f"Model load error: {str(e)}")
                return
        
        # Start detection thread
        self.running = True
        self.detection_thread = threading.Thread(
            target=self.detection_worker, 
            args=(url, self.show_video_check.get_active())
        )
        self.detection_thread.daemon = True
        self.detection_thread.start()
        
        # Update UI
        self.start_button.set_sensitive(False)
        self.stop_button.set_sensitive(True)
        self.url_entry.set_sensitive(False)
        self.show_video_check.set_sensitive(False)

    def on_stop_clicked(self, button):
        self.running = False
        if self.detection_thread and self.detection_thread.is_alive():
            self.detection_thread.join(timeout=2.0)
        
        # Update UI
        self.start_button.set_sensitive(True)
        self.stop_button.set_sensitive(False)
        self.url_entry.set_sensitive(True)
        self.show_video_check.set_sensitive(True)
        
        GLib.idle_add(self.update_connection_status, "Disconnected")
        GLib.idle_add(self.update_fps, 0.0)

    def detection_worker(self, source, show_video):
        """Background thread for YOLO detection"""
        try:
            GLib.idle_add(self.update_connection_status, "Connecting...")
            
            # FPS tracking
            t_prev = time.time()
            ema = None
            
            # Start YOLO prediction stream
            for i, result in enumerate(
                self.model.predict(
                    source=source,
                    stream=True,
                    imgsz=512,
                    conf=0.4,
                    vid_stride=2,
                    max_det=300,
                    verbose=False,
                    task="detect",
                )
            ):
                if not self.running:
                    break
                
                if i == 0:  # First frame received
                    GLib.idle_add(self.update_connection_status, "Connected")
                
                frame = result.plot()
                
                # Count humans (assuming class 0 is person in COCO dataset)
                human_count = 0
                if result.boxes is not None:
                    for box in result.boxes:
                        if box.cls == 0:  # Person class
                            human_count += 1
                
                # Trigger human detection callback
                if human_count > 0:
                    self.on_human_detected(human_count, frame)
                else:
                    GLib.idle_add(self.update_detection_count, 0)
                
                # Calculate FPS
                now = time.time()
                inst = 1.0 / (now - t_prev)
                t_prev = now
                ema = inst if ema is None else (0.9 * ema + 0.1 * inst)
                
                # Add FPS to frame
                cv2.putText(
                    frame,
                    f"FPS: {ema:.1f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )
                
                # Update GUI
                GLib.idle_add(self.update_fps, ema)
                
                # Queue frame for display if video is enabled
                if show_video:
                    try:
                        self.frame_queue.put_nowait(frame)
                    except queue.Full:
                        # Skip frame if queue is full to prevent lag
                        try:
                            self.frame_queue.get_nowait()  # Remove old frame
                            self.frame_queue.put_nowait(frame)  # Add new frame
                        except queue.Empty:
                            pass
                            
        except Exception as e:
            GLib.idle_add(self.update_connection_status, f"Error: {str(e)}")
        finally:
            GLib.idle_add(self.update_connection_status, "Disconnected")

    def update_display(self):
        """Update video display (called periodically)"""
        if not self.frame_queue.empty():
            try:
                frame = self.frame_queue.get_nowait()
                
                # Convert OpenCV frame (BGR) to RGB for GTK
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channels = rgb_frame.shape
                
                # Create GdkPixbuf from frame
                pixbuf = GdkPixbuf.Pixbuf.new_from_data(
                    rgb_frame.tobytes(),
                    GdkPixbuf.Colorspace.RGB,
                    False,
                    8,
                    width,
                    height,
                    width * channels
                )
                
                # Scale to fit widget while maintaining aspect ratio
                widget_width = self.image_widget.get_allocated_width()
                widget_height = self.image_widget.get_allocated_height()
                
                if widget_width > 0 and widget_height > 0:
                    scaled_pixbuf = pixbuf.scale_simple(
                        widget_width,
                        widget_height,
                        GdkPixbuf.InterpType.BILINEAR
                    )
                    self.image_widget.set_from_pixbuf(scaled_pixbuf)
                    
            except queue.Empty:
                pass
        
        return True  # Continue periodic updates

    def update_connection_status(self, status):
        self.connection_label.set_text(f"Connection: {status}")

    def update_fps(self, fps):
        self.fps_label.set_text(f"FPS: {fps:.1f}")

    def update_detection_count(self, count):
        self.detection_label.set_text(f"Humans detected: {count}")

    def on_window_destroy(self, widget):
        self.running = False
        if self.detection_thread and self.detection_thread.is_alive():
            self.detection_thread.join(timeout=2.0)
        Gtk.main_quit()

    def run(self):
        self.window.show_all()
        Gtk.main()


if __name__ == "__main__":
    app = YOLODetectorGUI()
    app.run()
