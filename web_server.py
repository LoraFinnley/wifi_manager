# Flask UI for SSID+ and password input

from flask import Flask, request, render_template_string
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
    body {
      font-family: sans-serif;
      background-color: #f4f4f4;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .container {
      background: white;
      padding: 2em;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
      max-width: 400px;
      width: 100%;
    }
    h1 {
      text-align: center;
      color: #333;
    }
    form {
      display: flex;
      flex-direction: column;
    }
    input[type="text"],
    input[type="password"] {
      padding: 0.5em;
      margin-bottom: 1em;
      border: 1px solid #ccc;
      border-radius: 5px;
      font-size: 1em;
    }
    input[type="submit"] {
      padding: 0.5em;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 1em;
      cursor: pointer;
    }
    input[type="submit"]:hover {
      background-color: #0056b3;
    }
    .message {
      margin-top: 1em;
      text-align: center;
      color: #333;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Verbinde mit einem WLAN</h1>
    <form method="post">
      <label>SSID:
        <input type="text" name="ssid" required>
      </label>
      <label>Passwort:
        <input type="password" name="password" required>
      </label>
      <input type="submit" value="Verbinden">
    </form>
    {% if message %}
      <div class="message"><strong>{{ message }}</strong></div>
    {% endif %}
  </div>
</body>
</html>
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
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    run_web_server()