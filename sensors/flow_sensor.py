class FlowSensor:
    def __init__(self, esp32_connection):
        """
        esp32_connection: shared ESP32Connection instance
        """
        self.esp32 = esp32_connection

    def read_flow(self):
        """
        Returns:
            float: milliliters of water used since last pump start
        """
        try:
            response = self.esp32.send_command("GET FLOW")
            print("[DEBUG] Raw FLOW response from ESP32:", repr(response))

            # Look for a line that starts with FLOW:
            for line in response.splitlines():
                if line.startswith("FLOW:"):
                    flow_part = line.split("FLOW:")[1].strip()
                    ml_used = float(flow_part)

                    print("[DEBUG] Parsed flow value (mL):", ml_used)
                    return ml_used

            # Default if no FLOW line found
            return 0.0

        except Exception as e:
            print("[ERROR] Failed to read flow sensor:", e)
            return 0.0
