import socket
import threading
import time
# from utils.logger import log_info, log_error

class ESP32Connection:
    def __init__(self, ip, port=3333, timeout=5):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.lock = threading.Lock()
        self.connected = False

    # -----------------------------
    # Connection Handling
    # -----------------------------
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.ip, self.port))
            self.connected = True
            # log_info(f"Connected to ESP32 at {self.ip}:{self.port}")
        except Exception as e:
            # log_error(f"ESP32 connection failed: {e}")
            self.connected = False
            raise

    def disconnect(self):
        try:
            if self.socket:
                self.socket.close()
                # log_info("ESP32 connection closed")
        except Exception as e:
            # log_error(f"Error while closing socket: {e}")
            pass
        finally:
            self.connected = False

    # -----------------------------
    # Core Send Method (LOCKED)
    # -----------------------------
    def send_command(self, command: str, expect_response=True):
        """
        Sends a command to ESP32 in a thread-safe way.
        """
        if not self.connected:
            raise RuntimeError("ESP32 not connected")

        with self.lock:
            try:
                self.socket.sendall((command + "\n").encode())

                if not expect_response:
                    return None

                response = self.socket.recv(1024).decode().strip()
                return response

            except Exception as e:
                # log_error(f"Communication error: {e}")
                self.connected = False
                raise

    # -----------------------------
    # Receive raw telemetry (non-blocking)
    # -----------------------------
    def receive(self, buffer_size=1024):
        """
        Read raw telemetry from ESP32.
        Returns string or None.
        """
        if not self.connected:
            return None

        with self.lock:
            try:
                self.socket.settimeout(0.05)  # short timeout
                data = self.socket.recv(buffer_size)
                if data:
                    return data.decode().strip()
                return None
            except socket.timeout:
                return None
            except Exception:
                self.connected = False
                return None

    # -----------------------------
    # Health Check
    # -----------------------------
    def ping(self):
        try:
            response = self.send_command("PING")
            return response == "PONG"
        except Exception:
            self.connected = False
            return False

    # -----------------------------
    # Connection Status
    # -----------------------------
    def is_connected(self):
        return self.connected