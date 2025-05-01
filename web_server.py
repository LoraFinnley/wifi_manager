# Flask UI for SSID+ and password input

from flask import Flask, request, render_template_string
from wifi_control import WifiManager

app = Flask(__name__)
wifi = WifiManager()

HTML_FORM = """
<!doctype html>
<title>WiFi Setup</title>
<h1>Verbinde mit einem WLAN</h1>
<form method=post>
  SSID: <input type=text name=ssid><br>
  Passwort: <input type=password name=password><br>
  <input type=submit value=Verbinden>
</form>
{% if message %}
<p><strong>{{ message }}</strong></p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def wifi_setup():
    message = ""
    if request.method == "POST":
        ssid = request.form.get("ssid")
        password = request.form.get("password")
        if ssid and password:
            result = wifi.connect_to_network(ssid, password)
            message = result
        else:
            message = "Bitte SSID und Passwort eingeben."
    return render_template_string(HTML_FORM, message=message)

def run_web_server():
    app.run(host="0.0.0.0", port=80)
