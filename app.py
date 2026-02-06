import json
import subprocess
import signal
import sys
from functools import wraps
from threading import Thread

from flask import (
    Flask, render_template, request,
    redirect, session, url_for, Response
)
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET"
processes = []

USERS_FILE = "users.json"

def load_users():
    with open(USERS_FILE) as f:
        return json.load(f)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()
        username = request.form["username"]
        password = request.form["password"]

        if username in users and check_password_hash(
            users[username]["password"], password
        ):
            session["user"] = username
            session["role"] = users[username]["role"]
            return redirect("/controlboard")

        return "Invalid credentials", 403

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/controlboard")
@login_required
def controlboard():
    return render_template("controlboard.html", user=session["user"])

@app.route("/proxy/<path:target>")
@login_required
def proxy(target):
    # Simple auth gate before proxying
    if not target.startswith(("http://", "https://")):
        target = "https://" + target

    import requests
    try:
        r = requests.get(target, timeout=10)
        return Response(r.content, r.status_code)
    except Exception as e:
        return Response(str(e), 502)

def start_mitmproxy():
    p = subprocess.Popen(
        ["mitmweb", "-p", "8081", "--web-port", "8082"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    processes.append(p)

def shutdown(signum, frame):
    for p in processes:
        p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

if __name__ == "__main__":
    Thread(target=start_mitmproxy, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
