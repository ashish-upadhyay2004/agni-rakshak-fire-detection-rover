import time
from esp32_connection import ESP32Connection
from sensors.ir_sensor import IRSensorArray

def main():
    # -----------------------------
    # Setup connection
    # -----------------------------
    esp = ESP32Connection(ip="192.168.4.1", port=3333)
    try:
        esp.connect()
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    ir_sensor = IRSensorArray(esp)

    print("\nIR Sensor Test Started")
    print("Format: LEFT | CENTER | RIGHT")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            status = ir_sensor.read_status()
            print(
                f"LEFT: {status['left']} | "
                f"CENTER: {status['center']} | "
                f"RIGHT: {status['right']}"
            )
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopping IR test...")

    finally:
        esp.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    main()
