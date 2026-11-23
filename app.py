import os
import re
from flask import Flask, request, make_response
from markupsafe import escape

app = Flask(__name__)

NAME_PATTERN = re.compile(r"^[A-Za-z0-9 _-]{1,50}$")


@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'self'"
    )
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/hello")
def hello():
    name = request.args.get("name", "Guest")
    if not NAME_PATTERN.fullmatch(name):
        return make_response("Invalid name parameter.", 400)
    safe_name = escape(name)
    return make_response(f"Hello, {safe_name}!", 200)


if __name__ == "__main__":
    host = os.environ.get("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_RUN_PORT", "5000"))
    app.run(host=host, port=port, debug=False)
