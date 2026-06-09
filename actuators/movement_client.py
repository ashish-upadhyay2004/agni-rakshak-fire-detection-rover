class MovementClient:
    def __init__(self, esp32_connection):
        """
        esp32_connection: shared ESP32Connection instance
        """
        self.esp32 = esp32_connection

    # =====================
    # MOVEMENT COMMANDS
    # =====================
    def forward(self):
        return self.esp32.send_command("MOVE FWD")

    def backward(self):
        return self.esp32.send_command("MOVE REV")

    def turn_left(self):
        return self.esp32.send_command("TURN LEFT")

    def turn_right(self):
        return self.esp32.send_command("TURN RIGHT")

    def stop(self):
        return self.esp32.send_command("STOP")

    # =====================
    # SAFETY
    # =====================
    def emergency_stop(self):
        """
        Hard stop, used in failsafe situations.
        """
        try:
            return self.stop()
        except Exception:
            return None
