#BEST FINAL WORKING SCRIPT
import time
import cv2
import threading

from actuators.movement_client import MovementClient
from actuators.pump_client import PumpClient
from actuators.servo_client import ServoClient
from sensors.ir_sensor import IRSensorArray
from sensors.fire_detection import FireDetector


class FireRoverDecision:
    def __init__(self, esp32_connection, camera_source=1):
        """
        esp32_connection: ESP32Connection instance
        camera_source: USB camera index or video source
        """
        self.esp = esp32_connection

        # ---------------- ACTUATORS ---------------- #
        self.movement = MovementClient(self.esp)
        self.pump = PumpClient(self.esp)
        self.servo = ServoClient(self.esp)

        # ---------------- SENSORS ---------------- #
        self.ir_sensor = IRSensorArray(self.esp)
        self.fire_detector = FireDetector()

        # ---------------- CAMERA ---------------- #
        self.cap = cv2.VideoCapture(camera_source)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")

        # ---------------- STATE MACHINE ---------------- #
        self.state = "search"

        # ---------------- FIRE CONFIRMATION ---------------- #
        self.fire_frame_count = 0
        self.FIRE_CONFIRM_FRAMES = 3
        self.FIRE_LOST_FRAMES = 6
        self.fire_confirmed = False

        # ---------------- WATER NOZZLE ---------------- #
        self.nozzle_angle = self.servo.get_water_center()
        self.nozzle_direction = 1

        # ---------------- CAMERA SCANNING ---------------- #
        self.camera_pos = 1500
        self.scan_direction = 1
        self.scan_step = 10
        self.scan_min = 1200
        self.scan_max = 1800

        # ================= IR BACKGROUND MONITOR =================
        self.ir_center_triggered = False
        self._ir_thread_running = True
        self.ir_thread = threading.Thread(
            target=self._ir_monitor_loop,
            daemon=True
        )
        self.ir_thread.start()

        # ---------------- ALIGN FIRE RECOVERY ---------------- #
        self.align_lost_count = 0
        self.ALIGN_LOST_LIMIT = 6

        # ---------------- APPROACH PULSE MOTION ---------------- #
        self.APPROACH_MOVE_TIME = 0.15
        self.APPROACH_PAUSE_TIME = 0.10
        self._approach_last_time = time.time()
        self._approach_moving = False

    # ---------------- SAFETY ---------------- #

    def check_connection(self):
        if not self.esp.connected:
            print("[ALERT] ESP32 disconnected! Stopping everything.")
            self.shutdown()
            return False
        return True

    def shutdown(self):
        for _ in range(3):
            self.movement.stop()
            time.sleep(0.05)
        self._ir_thread_running = False
        self.pump.off()
        self.servo.reset()
        time.sleep(0.1)

    def _ir_monitor_loop(self):
        while self._ir_thread_running:
            try:
                status = self.ir_sensor.read_status()
                self.ir_center_triggered = (status.get("center", 0) == 1)
            except Exception:
                self.ir_center_triggered = False
            time.sleep(0.05)

    # ---------------- STATES ---------------- #

    def search_fire(self):
        self.camera_pos += self.scan_direction * self.scan_step

        if self.camera_pos >= self.scan_max:
            self.camera_pos = self.scan_max
            self.scan_direction = -1
        elif self.camera_pos <= self.scan_min:
            self.camera_pos = self.scan_min
            self.scan_direction = 1

        self.servo.set_camera_us(self.camera_pos)

    def align_fire(self, fire_center_x, frame_width, fire_visible):
        if not fire_visible:
            self.align_lost_count += 1
            self.movement.stop()

            if self.align_lost_count >= self.ALIGN_LOST_LIMIT:
                print("[WARN] Fire lost during align → returning to search")
                self.align_lost_count = 0
                self.state = "search"
            return False

        self.align_lost_count = 0

        FRAME_CENTER_X = frame_width // 2
        IMAGE_TOLERANCE = 80
        CAMERA_CENTER = self.servo.get_camera_center()
        CAMERA_MIN = 1300
        CAMERA_MAX = 1700
        CAMERA_TRACK_GAIN = 0.15
        CAMERA_RECENTER_GAIN = 0.05

        image_error = fire_center_x - FRAME_CENTER_X

        camera_track = int(image_error * CAMERA_TRACK_GAIN)
        self.camera_pos -= camera_track

        camera_center_error = self.camera_pos - CAMERA_CENTER
        self.camera_pos -= int(camera_center_error * CAMERA_RECENTER_GAIN)

        self.camera_pos = max(CAMERA_MIN, min(CAMERA_MAX, self.camera_pos))
        self.servo.set_camera_us(self.camera_pos)

        image_aligned = abs(image_error) <= IMAGE_TOLERANCE

        if image_aligned:
            self.movement.stop()
            print("[DEBUG] Fire aligned → starting approach")
            return True

        if image_error < 0:
            self.movement.turn_left()
        else:
            self.movement.turn_right()

        return False

    def approach_fire(self):
        """
        Move forward in controlled pulse steps:
        MOVE → STOP → MOVE → STOP
        """
        if self.ir_center_triggered:
            print("[DEBUG] IR CENTER TRIGGERED → STOPPING")
            self.movement.stop()
            return True

        now = time.time()

        # MOVE PHASE
        if self._approach_moving:
            if now - self._approach_last_time >= self.APPROACH_MOVE_TIME:
                self.movement.stop()
                self._approach_moving = False
                self._approach_last_time = now

        # PAUSE PHASE
        else:
            if now - self._approach_last_time >= self.APPROACH_PAUSE_TIME:
                self.movement.forward()
                self._approach_moving = True
                self._approach_last_time = now

        return False

    def extinguish_fire(self):
        if self.ir_center_triggered:
            self.movement.stop()
            self.pump.on()

            self.nozzle_angle += self.nozzle_direction * 150
            if self.nozzle_angle > 1600:
                self.nozzle_direction = -1
            elif self.nozzle_angle < 1400:
                self.nozzle_direction = 1

            self.servo.set_water_us(self.nozzle_angle)
        else:
            self.pump.off()
            self.servo.center_water()

    # ---------------- MAIN LOOP ---------------- #

    def run(self):
        try:
            print("[INFO] Starting Fire Rover Decision System")
            print("Press Ctrl+C or 'q' in the video window to terminate\n")

            APPROACH_ALIGN_TOLERANCE = 100

            while True:
                if not self.check_connection():
                    break

                ret, frame = self.cap.read()
                if not ret:
                    print("[ERROR] Camera frame not available")
                    time.sleep(0.1)
                    continue

                raw_fire, fire_center_x, frame_width = self.fire_detector.detect_fire(frame)

                if raw_fire:
                    self.fire_frame_count += 1
                else:
                    self.fire_frame_count -= 1

                self.fire_frame_count = max(0, min(self.fire_frame_count, 20))

                self.fire_confirmed = self.fire_frame_count >= self.FIRE_CONFIRM_FRAMES
                fire_lost = self.fire_frame_count <= self.FIRE_LOST_FRAMES

                if self.ir_center_triggered and self.fire_confirmed:
                    self.movement.stop()
                    self.state = "extinguish"

                if self.fire_confirmed:
                    cv2.line(frame, (fire_center_x, 0),
                             (fire_center_x, frame.shape[0]), (0, 0, 255), 2)
                    cv2.putText(frame, "FIRE CONFIRMED", (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.imshow("Fire Rover Vision", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    raise KeyboardInterrupt

                if self.state == "search":
                    if self.fire_confirmed:
                        self.movement.stop()
                        self.servo.set_camera_us(self.camera_pos)
                        self.state = "align"
                    else:
                        self.search_fire()

                elif self.state == "align":
                    if self.align_fire(fire_center_x, frame_width, raw_fire):
                        # Reset pulse system cleanly
                        self._approach_moving = False
                        self._approach_last_time = time.time()
                        self.movement.stop()
                        self.state = "approach"

                elif self.state == "approach":
                    if fire_lost:
                        self.movement.stop()
                        self.state = "search"

                    else:
                        frame_center_x = frame_width // 2
                        image_error = fire_center_x - frame_center_x

                        if abs(image_error) > APPROACH_ALIGN_TOLERANCE:
                            self.movement.stop()
                            self.state = "align"

                        else:
                            if self.approach_fire():
                                self.state = "extinguish"

                elif self.state == "extinguish":
                    if fire_lost:
                        self.pump.off()
                        self.servo.center_water()
                        self.state = "search"
                    else:
                        self.extinguish_fire()

                time.sleep(0.05)

        except KeyboardInterrupt:
            print("\n[INFO] Manual termination detected")

        finally:
            print("[INFO] Shutting down rover safely...")
            self.shutdown()
            self.cap.release()
            cv2.destroyAllWindows()
