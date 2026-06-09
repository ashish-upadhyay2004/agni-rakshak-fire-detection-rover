class IRSensorArray:
    def __init__(self, esp32_connection):
        """
        esp32_connection: shared ESP32Connection instance
        """
        self.esp32 = esp32_connection

    def read_status(self):
        try:
            response = self.esp32.send_command("GET IR")
            print("[DEBUG] Raw IR response from ESP32:", repr(response))
    
            # Split by any line and find the first line that starts with IR:
            for line in response.splitlines():
                if line.startswith("IR:"):
                    ir_part = line.split("IR:")[1].strip()
                    status = int(ir_part)
                    parsed = {
                        "center": (status & 0b001) >> 0,
                        "left":   (status & 0b010) >> 1,
                        "right":  (status & 0b100) >> 2
                    }
                    print("[DEBUG] Parsed IR status:", parsed)
                    return parsed
    
            # Default if no IR line found
            return {"left": 0, "center": 0, "right": 0}
    
        except Exception as e:
            print("[ERROR] Failed to read IR status:", e)
            return {"left": 0, "center": 0, "right": 0}
