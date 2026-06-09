# test_flow_sensor.py

import time
from sensors.flow_sensor import FlowSensor

# ---------------- MOCK ESP32 CONNECTION ---------------- #
class MockESP32:
    def __init__(self):
        self.flow_value = 123.45  # Example fixed value

    def send_command(self, command):
        if command == "GET FLOW":
            # Simulate ESP32 response format
            return f"FLOW: {self.flow_value}\nOK\n"
        return "UNKNOWN COMMAND\n"

# ---------------- TEST SCRIPT ---------------- #
if __name__ == "__main__":
    # Create mock ESP32
    esp32 = MockESP32()

    # Create FlowSensor instance
    flow_sensor = FlowSensor(esp32)

    print("=== Flow Sensor Test ===")
    for i in range(5):
        flow_ml = flow_sensor.read_flow()
        print(f"Test {i+1}: Flow = {flow_ml:.2f} mL")
        time.sleep(0.5)  # simulate polling interval
