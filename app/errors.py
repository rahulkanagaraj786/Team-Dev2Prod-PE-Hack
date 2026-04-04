from flask import jsonify


def error_response(code, message, status_code, details=None):
    payload = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    if details is not None:
        payload["error"]["details"] = details
    return jsonify(payload), status_code


def register_error_handlers(app):
    @app.errorhandler(404)
    def handle_not_found(error):
        return error_response(
            "route_not_found",
            "That route does not exist.",
            404,
        )

    @app.errorhandler(500)
    def handle_internal_error(error):
        return error_response(
            "internal_error",
            "Something went wrong on our side.",
            500,
        )
