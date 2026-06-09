import cv2
from sensors.fire_detection import FireDetector


def main():
    # -----------------------------
    # Initialize detector
    # -----------------------------
    detector = FireDetector(device="cpu")

    # -----------------------------
    # Open webcam
    # -----------------------------
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("❌ Could not open webcam")
        return

    print("🔥 FireDetector test running")
    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        frame_height, frame_width = frame.shape[:2]

        # Run YOLO inference directly (same as detector)
        results = detector.model(frame, device=detector.device, verbose=False)

        fire_detected = False
        best_box = None
        best_area = 0

        if results and len(results[0].boxes) > 0:
            for box in results[0].boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())

                if cls_id != detector.FIRE_CLASS_ID:
                    continue
                if conf < detector.CONF_THRESHOLD:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                area = (x2 - x1) * (y2 - y1)

                if area >= detector.MIN_FIRE_AREA and area > best_area:
                    best_area = area
                    best_box = (x1, y1, x2, y2)
                    fire_detected = True
                    best_conf = conf

        # -----------------------------
        # Draw results
        # -----------------------------
        if fire_detected and best_box is not None:
            x1, y1, x2, y2 = best_box
            center_x = (x1 + x2) // 2

            # Bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # Center line
            cv2.line(frame, (center_x, 0), (center_x, frame_height), (255, 0, 0), 1)

            # Label
            label = f"FIRE {best_conf:.2f}"
            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

            print(f"🔥 FIRE detected | center_x={center_x} | area={best_area}")
        else:
            print("— No fire detected")

        # Show frame
        cv2.imshow("FireDetector Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


