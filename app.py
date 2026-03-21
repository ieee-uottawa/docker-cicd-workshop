import os
import requests
from flask import Flask, jsonify, request


app = Flask(__name__)

DEFAULT_MESSAGE = "Docker + CI/CD workshop server"
DEFAULT_IPIFY_URL = "https://api.ipify.org?format=json"
DEFAULT_IPIFY_TIMEOUT = 5
DEFAULT_SECRET_FILE = "/run/secrets/demo_secret"


def get_env_int(name, default):
    value = os.getenv(name, str(default))
    try:
        return int(value)
    except ValueError:
        return default


def get_secret_status():
    secret_file = os.getenv("DEMO_SECRET_FILE", DEFAULT_SECRET_FILE)
    return os.path.exists(secret_file)


def get_ip():
    try:
        ipify_url = os.getenv("IPIFY_URL", DEFAULT_IPIFY_URL)
        ipify_timeout = get_env_int("IPIFY_TIMEOUT", DEFAULT_IPIFY_TIMEOUT)
        data = requests.get(ipify_url, timeout=ipify_timeout).json()
        return data["ip"], None
    except Exception as e:
        return None, str(e)


def add(a, b):
    return a + b


@app.get("/")
def home():
    message = os.getenv("APP_MESSAGE", DEFAULT_MESSAGE)
    return jsonify({"message": message})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/config")
def config():
    return jsonify(
        {
            "app_message": os.getenv("APP_MESSAGE", DEFAULT_MESSAGE),
            "ipify_url": os.getenv("IPIFY_URL", DEFAULT_IPIFY_URL),
            "has_demo_secret": get_secret_status(),
        }
    )


@app.get("/ip")
def ip_address():
    ip, error = get_ip()
    if error:
        return jsonify({"error": error}), 502
    return jsonify({"ip": ip})


@app.get("/add")
def add_numbers():
    try:
        first = int(request.args.get("a", ""))
        second = int(request.args.get("b", ""))
    except ValueError:
        return jsonify({"error": "Params a and b must be integers"}), 400
    return jsonify({"result": add(first, second)})


if __name__ == "__main__":
    app_port = get_env_int("APP_PORT", 8000)
    app.run(host="0.0.0.0", port=app_port)
