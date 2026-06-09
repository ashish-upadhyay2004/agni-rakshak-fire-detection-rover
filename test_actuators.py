import time
from esp32_connection import ESP32Connection
from actuators.movement_client import MovementClient
from actuators.pump_client import PumpClient
from actuators.servo_client import ServoClient

def main():
    # -----------------------------
    # Setup
    # -----------------------------
    esp = ESP32Connection(ip="192.168.4.1", port=3333)
    try:
        esp.connect()
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    # Initialize clients
    movement = MovementClient(esp)
    pump = PumpClient(esp)
    servo = ServoClient(esp)

    # -----------------------------
    # Manual test loop
    # -----------------------------
    print("\nManual actuator test started. Commands:")
    print("  Movement: fwd, rev, left, right, stop")
    print("  Pump: on, off")
    print("  Servo: cam_left, cam_right, cam_center, nozzle <us>")
    print("  exit: quit test\n")

    while True:
        cmd = input("Enter command: ").strip().lower()

        if cmd == "exit":
            print("Exiting test...")
            break

        # Movement commands
        elif cmd == "fwd":
            print(movement.forward())
        elif cmd == "rev":
            print(movement.backward())
        elif cmd == "left":
            print(movement.turn_left())
        elif cmd == "right":
            print(movement.turn_right())
        elif cmd == "stop":
            print(movement.stop())

        # Pump commands
        elif cmd == "on":
            print(pump.on())
        elif cmd == "off":
            print(pump.off())

        # Servo commands
        elif cmd == "cam_left":
            print(servo.camera_left())
        elif cmd == "cam_right":
            print(servo.camera_right())
        elif cmd == "cam_center":
            print(servo.camera_center())
        elif cmd.startswith("nozzle"):
            try:
                us = int(cmd.split()[1])
                print(servo.water_angle(us))
            except Exception:
                print("Invalid nozzle command. Usage: nozzle <microseconds>")
        else:
            print("Unknown command")

    # -----------------------------
    # Cleanup
    # -----------------------------
    esp.disconnect()
    print("Test completed.")

if __name__ == "__main__":
    main()
