# starts/stops access point (hostapd, dnsmasq)

import os
import subprocess

class AccessPointManager:
    def __init__(self, ssid="ClockPi", interface="wlan0"):
        self.ssid = ssid
        self.interface = interface
        self.hostapd_conf = "/tmp/hostapd.conf"
        self.dnsmasq_conf = "/tmp/dnsmasq.conf"

    def write_hostapd_config(self):
        config = f"""
interface={self.interface}
driver=nl80211
ssid={self.ssid}
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=1505
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
        """.strip()

        with open(self.hostapd_conf, "w") as f:
            f.write(config)

    def write_dnsmasq_config(self):
        config = f"""
interface={self.interface}
dhcp-range=10.0.0.10,10.0.0.50,255.255.255.0,24h
address=/#/10.0.0.1
        """.strip()

        with open(self.dnsmasq_conf, "w") as f:
            f.write(config)

    def configure_interface(self):
        subprocess.run(["sudo", "ip", "link", "set", self.interface, "up"])
        subprocess.run(["sudo", "ip", "addr", "add", "10.0.0.1/24", "dev", self.interface])

    def enable_nat(self):
        subprocess.run(["sudo", "sh", "-c", "echo 1 > /proc/sys/net/ipv4/ip_forward"])
        subprocess.run(["sudo", "iptables", "-t", "nat", "-A", "POSTROUTING", "-o", "eth0", "-j", "MASQUERADE"])

    def start_access_point(self):
        self.write_hostapd_config()
        self.write_dnsmasq_config()
        self.configure_interface()
        self.enable_nat()

        subprocess.Popen(["sudo", "hostapd", self.hostapd_conf])
        subprocess.Popen(["sudo", "dnsmasq", "-C", self.dnsmasq_conf])

    def stop_access_point(self):
        subprocess.run(["sudo", "pkill", "hostapd"])
        subprocess.run(["sudo", "pkill", "dnsmasq"])
        subprocess.run(["sudo", "ip", "link", "set", self.interface, "down"])
        subprocess.run(["sudo", "iptables", "-t", "nat", "-F"])

        # remove config files
        if os.path.exists(self.hostapd_conf):
            os.remove(self.hostapd_conf)
        if os.path.exists(self.dnsmasq_conf):
            os.remove(self.dnsmasq_conf)
