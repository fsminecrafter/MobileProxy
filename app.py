import subprocess
import signal
import sys
from threading import Thread
from flask import Flask, render_template

app = Flask(__name__)
processes = []

@app.route("/controlboard")
def controlboard():
    return render_template("controlboard.html")

def start_mitmproxy():
    print("🔐 Starting mitmproxy on port 8081...")
    p = subprocess.Popen(
        ["mitmweb", "-p", "8081", "--web-port", "8082"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    processes.append(p)

def start_flask():
    print("🌐 Starting Flask controlboard on port 8080...")
    app.run(host="0.0.0.0", port=8080)

def shutdown(signum, frame):
    print("\n🛑 Shutting down...")
    for p in processes:
        p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

if __name__ == "__main__":
    Thread(target=start_mitmproxy, daemon=True).start()
    start_flask()
