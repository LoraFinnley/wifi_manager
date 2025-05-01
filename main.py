# starting point: check connection, start AP

from ap_mode import AccessPointManager
from web_server import run_web_server
from wifi_control import WifiManager

wifi = WifiManager()
ap = AccessPointManager()

if not wifi.is_connected_to_internet(): 
    print("Keine Internetverbindung – starte Access Point...")
    ap.start_access_point()
    run_web_server()
else:
    print("Internetverbindung erkannt.")
