from esp32_connection import ESP32Connection
from decisions import FireRoverDecision
from utils.logger import setup_run_logger


def main():
    setup_run_logger()
    # -----------------------------
    # Setup ESP32 connection
    # -----------------------------
    esp_ip = "192.168.4.1"
    esp_port = 3333
    esp = ESP32Connection(ip=esp_ip, port=esp_port)

    try:
        esp.connect()
        print(f"[INFO] Connected to ESP32 at {esp_ip}:{esp_port}")
    except Exception as e:
        print(f"[ERROR] Failed to connect to ESP32: {e}")
        return

    # -----------------------------
    # Initialize Decision System
    # -----------------------------
    rover = FireRoverDecision(esp32_connection=esp, camera_source=0)

    print("[INFO] Starting Fire Rover Decision System")
    print("Press Ctrl+C to terminate manually\n")

    # -----------------------------
    # Run state machine
    # -----------------------------
    rover.run()
    try:
        rover.shutdown()  # ensure everything stops
    except Exception:
        pass

    # -----------------------------
    # Shutdown
    # -----------------------------
    try:
        esp.disconnect()
        print("[INFO] ESP32 disconnected successfully")
    except Exception as e:
        print(f"[WARN] Error during ESP32 disconnect: {e}")

    print("[INFO] System shutdown complete")

if __name__ == "__main__":
    main()
