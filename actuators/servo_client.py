class ServoClient:
    def __init__(self, esp32_connection):
        """
        esp32_connection: shared ESP32Connection instance
        """
        self.esp32 = esp32_connection

        # =====================
        # SERVO CONSTANTS
        # =====================
        # Must match ESP32 firmware
        self.CAMERA_CENTER_US = 1500
        self.WATER_CENTER_US = 1500

        # Internal state tracking (software truth)
        self._camera_us = self.CAMERA_CENTER_US

    # =====================
    # CAMERA SERVO (MICROSECONDS)
    # =====================
    def set_camera_us(self, microseconds: int):
        """
        Set camera servo PWM in microseconds
        """
        self._camera_us = microseconds
        return self.esp32.send_command(f"CAMERA ANGLE {microseconds}")

    def center_camera(self):
        """
        Center the camera servo
        """
        return self.set_camera_us(self.CAMERA_CENTER_US)

    def get_camera_center(self) -> int:
        return self.CAMERA_CENTER_US

    # =====================
    # CAMERA SERVO (LEGACY / DEBUG)
    # =====================
    def scan_left(self):
        self._camera_us = None
        return self.esp32.send_command("SCAN LEFT")

    def scan_right(self):
        self._camera_us = None
        return self.esp32.send_command("SCAN RIGHT")

    def scan_center(self):
        self._camera_us = self.CAMERA_CENTER_US
        return self.esp32.send_command("SCAN CENTER")

    def is_camera_centered(self) -> bool:
        """
        Returns True if camera is logically centered.
        """
        return self._camera_us == self.CAMERA_CENTER_US

    # =====================
    # WATER NOZZLE SERVO
    # =====================
    def set_water_us(self, microseconds: int):
        """
        Set water nozzle PWM in microseconds
        """
        return self.esp32.send_command(f"WATER ANGLE {microseconds}")

    def center_water(self):
        return self.set_water_us(self.WATER_CENTER_US)

    def get_water_center(self) -> int:
        return self.WATER_CENTER_US

    # =====================
    # SAFETY
    # =====================
    def reset(self):
        """
        Reset all servos to safe state
        """
        try:
            self.center_camera()
            self.center_water()
        except Exception:
            pass
