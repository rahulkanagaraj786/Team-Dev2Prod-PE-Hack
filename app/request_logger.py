import json
import logging
import os
import time

from flask import g, request

LOG_FILE = os.environ.get("REQUEST_LOG_FILE", "/tmp/eval_requests.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(message)s",
)
logger = logging.getLogger("request_logger")

# Also print to stdout so it shows up in server output
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logger.addHandler(console)


def _safe_json(data):
    try:
        return json.loads(data) if data else None
    except Exception:
        return data.decode("utf-8", errors="replace") if isinstance(data, bytes) else data


def register_request_logger(app):
    @app.before_request
    def before():
        g._start_time = time.time()
        body = request.get_data()
        logger.info(
            json.dumps(
                {
                    "event": "request",
                    "method": request.method,
                    "path": request.full_path.rstrip("?"),
                    "headers": dict(request.headers),
                    "body": _safe_json(body),
                },
                default=str,
            )
        )

    @app.after_request
    def after(response):
        duration_ms = round((time.time() - g._start_time) * 1000, 2)
        resp_body = response.get_data()
        logger.info(
            json.dumps(
                {
                    "event": "response",
                    "status": response.status_code,
                    "duration_ms": duration_ms,
                    "path": request.full_path.rstrip("?"),
                    "body": _safe_json(resp_body),
                },
                default=str,
            )
        )
        return response
