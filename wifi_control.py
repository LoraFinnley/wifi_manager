import subprocess
import time
import threading

class WifiManager:
    def __init__(self):
        self._network_cache = []
        self._scan_thread = None
        self._stop_scanning = False
        self._interface = "wlan0"

        if not self.is_connected_to_internet():
            self._start_scanning_loop()

    def _start_scanning_loop(self):
        def scan():
            while not self._stop_scanning:
                self._scan_networks()
                time.sleep(10)
        self._scan_thread = threading.Thread(target=scan, daemon=True)
        self._scan_thread.start()

    def stop_scanning(self):
        self._stop_scanning = True
        if self._scan_thread:
            self._scan_thread.join()

    def _scan_networks(self):
        subprocess.run(["nmcli", "device", "wifi", "rescan"])
        output = self.run_nmcli(["-t", "-f", "SSID", "device", "wifi", "list", "ifname", self._interface])
        # Filter leere SSIDs und doppelte Einträge
        self._network_cache = list({line.strip() for line in output if line.strip()})

    def get_cached_networks(self):
        return self._network_cache

    def run_nmcli(self, args):
        try:
            result = subprocess.run(
                ["nmcli"] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip().splitlines()
            else:
                return []
        except Exception:
            return []

    def list_saved_connections(self):
        return self.run_nmcli(["--terse", "--fields", "NAME,TYPE", "connection", "show"])

    def get_connection_status(self):
        return self.run_nmcli(["device", "status"])

    def connect_to_network(self, ssid, password):
        result = subprocess.run(
            ["nmcli", "device", "wifi", "connect", ssid,
             "password", password, "ifname", self._interface],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return f"✅ Verbunden mit '{ssid}'"
        else:
            return f"❌ Fehler beim Verbinden mit '{ssid}': {result.stderr.strip()}"

    def get_current_connection(self):
        lines = self.run_nmcli(["-t", "-f", "active,ssid", "device", "wifi"])
        for line in lines:
            if line.startswith("yes:"):
                return line.split(":", 1)[1]
        return None


    def edit_connection(self, ssid, new_password):
        return self.run_nmcli([
            "connection", "modify", ssid,
            "wifi-sec.key-mgmt", "wpa-psk",
            "wifi-sec.psk", new_password
        ])

    def delete_saved_connection(self, ssid):
        return self.run_nmcli(["connection", "delete", ssid])

    def is_connected_to_internet(self):
        try:
            subprocess.check_call(
                ["ping", "-c", "1", "8.8.8.8"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
