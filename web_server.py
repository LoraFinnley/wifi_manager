from flask import Flask, request, render_template_string, redirect, url_for
from wifi_control import WifiManager

app = Flask(__name__)
wifi = WifiManager()

HTML_FORM = """
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>WiFi Setup</title>
  <style>
    body { font-family: sans-serif; background: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .container { background: white; padding: 2em; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 400px; width: 100%; }
    h1 { text-align: center; color: #333; }
    form { display: flex; flex-direction: column; }
    label { margin-bottom: 0.5em; }
    select, input[type="password"] {
      width: 100%; padding: 0.5em; margin-bottom: 1em; border: 1px solid #ccc; border-radius: 5px; font-size: 1em;
    }
    input[type="submit"] {
      padding: 0.5em; background-color: #007bff; color: white; border: none; border-radius: 5px; font-size: 1em; cursor: pointer;
    }
    input[type="submit"]:hover { background-color: #0056b3; }
    .message { margin-top: 1em; text-align: center; color: #333; }
    .link { text-align: center; margin-top: 1em; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Verbinde mit einem WLAN</h1>
    {% if current_ssid %}
      <p class="message">Aktuell verbunden mit: <strong>{{ current_ssid }}</strong></p>
    {% endif %}
    <form method="post">
      <label>SSID:
        <select name="ssid" required>
          {% for ssid in ssids %}
          <option value="{{ ssid }}">{{ ssid }}</option>
          {% endfor %}
        </select>
      </label>
      <label>Passwort:
        <input type="password" name="password" required>
      </label>
      <input type="submit" value="Verbinden">
    </form>
    {% if message %}
      <div class="message"><strong>{{ message }}</strong></div>
    {% endif %}
    <div class="link">
      <a href="{{ url_for('show_saved') }}">Gespeicherte Netzwerke verwalten</a>
    </div>
  </div>
</body>
</html>
"""

HTML_SAVED = """
<!doctype html>
<title>Gespeicherte Netzwerke</title>
<h1>Gespeicherte Netzwerke</h1>
<ul>
{% for ssid in connections %}
  <li>{{ ssid }} <a href="{{ url_for('delete_saved', ssid=ssid) }}">[Löschen]</a></li>
{% endfor %}
</ul>
<p><a href="{{ url_for('wifi_setup') }}">Zurück</a></p>
"""

@app.route("/", methods=["GET", "POST"])
def wifi_setup():
    message = ""
    ssids = wifi.get_cached_networks()
    current_ssid = wifi.get_current_connection()
    if request.method == "POST":
        ssid = request.form.get("ssid")
        password = request.form.get("password")
        if ssid and password:
            message = wifi.connect_to_network(ssid, password)
        else:
            message = "Bitte SSID und Passwort eingeben."
    return render_template_string(HTML_FORM, ssids=sorted(ssids), message=message, current_ssid=current_ssid)

@app.route("/saved")
def show_saved():
    raw_output = wifi.list_saved_connections()
    ssids = []
    for line in raw_output:
        parts = line.split(":")
        if len(parts) == 2 and parts[1] == "wifi":
            ssids.append(parts[0])
    return render_template_string(HTML_SAVED, connections=ssids)

@app.route("/delete")
def delete_saved():
    ssid = request.args.get("ssid")
    if ssid:
        wifi.delete_saved_connection(ssid)
    return redirect(url_for('show_saved'))

def run_web_server():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    run_web_server()
