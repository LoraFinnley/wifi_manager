#!/bin/bash
# install all dependencies for wifi manager

set -e  # Beende bei Fehler

echo "Starte Setup für WiFi Manager..."

echo "Aktualisiere Paketlisten..."
sudo apt update

echo "Installiere benötigte Pakete..."
sudo apt install -y \
    network-manager \
    python3 \
    python3-pip \
    hostapd \
    dnsmasq \
    git

echo "Installiere Python-Abhängigkeiten..."
pip3 install flask

echo "✅ Setup abgeschlossen."