import subprocess

class WifiManager:
    def run_nmcli(self, args):
        try:
            result = subprocess.run(
                ["nmcli"] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Fehler: {result.stderr.strip()}"
        except Exception as e:
            return f"Exception: {str(e)}"

    
    # lists all saved connections
    def list_saved_connections(self):
        return self.run_nmcli(["connection", "show"])

    # shows current wifi status
    def get_connection_status(self):
        return self.run_nmcli(["device", "status"])

    # shows available wifi networks
    def list_available_networks(self, interface="wlan0"):
        return self.run_nmcli(["device", "wifi", "list", "ifname", interface])

    # connects to a new wifi network
    def connect_to_network(self, ssid, password, interface="wlan0"):
        return self.run_nmcli([
            "device", "wifi", "connect", ssid,
            "password", password,
            "ifname", interface
        ])

    # updates a saved connection
    def edit_connection(self, ssid, new_password):
        return self.run_nmcli([
            "connection", "modify", ssid,
            "wifi-sec.key-mgmt", "wpa-psk",
            "wifi-sec.psk", new_password
        ])

    # checks connection to the internet
    def is_connected_to_internet(self):
        # try to ping google's public DNS server
        # if the ping is successful, we assume the device is connected to the internet
        try:
            subprocess.check_call(
                ["ping", "-c", "1", "8.8.8.8"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except subprocess.CalledProcessError:
            # if the ping fails, we assume the device is not connected to the internet
            return False
        except FileNotFoundError:
            # if the ping command is not found, we assume the device is not connected to the internet
            return False
