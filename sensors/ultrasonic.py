class UltrasonicSensor:
    def __init__(self, esp32_connection):
        """
        esp32_connection: shared ESP32Connection instance
        """
        self.esp32 = esp32_connection

    def get_distance(self):
        """
        Requests distance from ESP32 HC-SR04 sensor.
        Returns:
            float: Distance in cm, -1 if invalid
        """
        try:
            response = self.esp32.send_command("GET DIST")
            # Expected response: "DIST:<value>"
            if response.startswith("DIST:"):
                dist_str = response.split(":")[1]
                return float(dist_str)
            return -1
        except Exception:
            return -1
