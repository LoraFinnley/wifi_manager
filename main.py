# starting point: check connection, start AP

from ap_mode import AccessPointManager
from web_server import run_web_server
from wifi_control import WifiManager

import os
import subprocess
import sys
import time

# creates .venv, if not exists
venv_path = os.path.join(os.path.dirname(__file__), ".venv")
venv_python = os.path.join(venv_path, "bin", "python")

if not os.path.exists(venv_python):
    print("[SETUP] Erstelle virtuelle Umgebung...")
    subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
    print("[SETUP] Installiere requirements...")
    subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("[SETUP] Venv eingerichtet. Bitte neu starten.")
    sys.exit(0)

# wifi manager
wifi = WifiManager()
ap = AccessPointManager()

if not wifi.is_connected_to_internet(): 
    print("Keine Internetverbindung – starte Access Point...")
    ap.start_access_point()
    run_web_server()
else:
    print("Internetverbindung erkannt.")

    while True:
        time.sleep(60)