import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

services = [
    ("task_service.main:app", 8000),
    ("notification_service.main:app", 8001),
]

procs = []
for app_path, port in services:
    procs.append(subprocess.Popen(
        [sys.executable, "-m", "uvicorn", app_path, "--port", str(port), "--reload"],
        cwd=ROOT,
    ))

try:
    for p in procs:
        p.wait()
except KeyboardInterrupt:
    for p in procs:
        p.terminate()