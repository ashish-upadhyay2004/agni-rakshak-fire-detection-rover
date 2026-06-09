class PumpClient:
    def __init__(self, esp32_connection):
        """
        esp32_connection: shared ESP32Connection instance
        """
        self.esp32 = esp32_connection

    # =====================
    # PUMP COMMANDS
    # =====================
    def on(self):
        return self.esp32.send_command("PUMP ON")

    def off(self):
        return self.esp32.send_command("PUMP OFF")

    # =====================
    # SAFETY
    # =====================
    def emergency_off(self):
        """
        Force the pump to stop in failsafe situations.
        """
        try:
            return self.off()
        except Exception:
            return None
