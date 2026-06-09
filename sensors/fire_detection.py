import cv2
import torch
from ultralytics import YOLO
from pathlib import Path

class FireDetector:
    """
    Fire detection using YOLOv8.
    This class provides ONLY raw fire detection.
    All temporal confirmation and decision logic
    must be handled in decisions.py.
    """

    # ---- Detection thresholds (tune later if needed) ----
    CONF_THRESHOLD = 0.6        # Minimum YOLO confidence
    MIN_FIRE_AREA = 2000        # Minimum bounding box area (pixels)
    FIRE_CLASS_ID = 0           # Change if your model uses a different class ID

    def __init__(self, device="cuda"):
        """
        device: 'cpu' or 'cuda'
        """

        # Path to best.pt in the SAME directory as this file
        model_path = Path(__file__).resolve().parent / "best.pt"

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")

        # Load YOLO model
        self.model = YOLO(str(model_path))

        # Select device safely
        if device == "cuda" and torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"

    def detect_fire(self, frame):
        """
        Detect fire in a given frame.

        Returns:
            detected (bool): True only if detection is confident and valid
            center_x (int): X-coordinate of detected fire center
            frame_width (int): Width of the frame
        """

        frame_height, frame_width = frame.shape[:2]

        # Run YOLO inference
        results = self.model(frame, device=self.device, verbose=False)

        # No detections at all
        if not results or len(results[0].boxes) == 0:
            return False, frame_width // 2, frame_width

        best_box = None
        best_area = 0

        # Iterate through all detected boxes
        for box in results[0].boxes:
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())

            # Filter non-fire classes
            if cls_id != self.FIRE_CLASS_ID:
                continue

            # Filter low-confidence detections
            if conf < self.CONF_THRESHOLD:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            area = (x2 - x1) * (y2 - y1)

            # Filter small detections and keep the largest valid one
            if area >= self.MIN_FIRE_AREA and area > best_area:
                best_area = area
                best_box = (x1, y1, x2, y2)

        # No valid fire detected after filtering
        if best_box is None:
            return False, frame_width // 2, frame_width

        x1, _, x2, _ = best_box
        center_x = (x1 + x2) // 2

        return True, center_x, frame_width