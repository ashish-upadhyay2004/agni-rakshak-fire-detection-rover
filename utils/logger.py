import os
import sys
from datetime import datetime

class TeeLogger:
    def __init__(self, logfile_path):
        self.terminal = sys.stdout
        self.log = open(logfile_path, "w", encoding="utf-8", buffering=1)

    def write(self, message):
        try:
            self.terminal.write(message)
        except Exception:
            pass

        try:
            self.log.write(message)
        except UnicodeEncodeError:
            # Fallback: strip unsupported chars
            safe = message.encode("utf-8", errors="replace").decode("utf-8")
            self.log.write(safe)

    def flush(self):
        self.terminal.flush()
        self.log.flush()


def setup_run_logger():
    os.makedirs("logs", exist_ok=True)

    existing = [
        f for f in os.listdir("logs")
        if f.startswith("run_") and f.endswith(".log")
    ]
    run_number = len(existing) + 1
    log_path = f"logs/run_{run_number}.log"

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"Fire Rover Log – Run {run_number}\n")
        f.write(f"Started at: {datetime.now()}\n")
        f.write("=" * 60 + "\n\n")

    logger = TeeLogger(log_path)
    sys.stdout = logger
    sys.stderr = logger

    print(f"[LOGGER] Logging to {log_path}")
